"""
API Views for Equipment management.

Provides REST API endpoints for:
- Dataset CRUD operations
- CSV file upload and processing
- Analytics computation and retrieval
- PDF report generation
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.serializers import Serializer
from django.http import HttpResponse
from django.conf import settings
from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth.models import AbstractUser
import logging

from .models import Dataset, Equipment, AnalysisResult
from .serializers import (
    DatasetListSerializer, DatasetDetailSerializer, DatasetUploadSerializer,
    EquipmentSerializer, AnalysisResultSerializer
)
from .services.csv_parser import CSVParserService
from .services.analytics import AnalyticsService
from .services.pdf_generator import PDFReportService

logger = logging.getLogger(__name__)


class DatasetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing datasets.
    
    Provides CRUD operations and additional actions for:
    - CSV file upload
    - Analytics retrieval
    - PDF report generation
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self) -> QuerySet[Dataset]:
        """Return datasets for the authenticated user, ordered by most recent first."""
        return Dataset.objects.filter(uploaded_by=self.request.user).order_by('-uploaded_at')
    
    def get_serializer_class(self) -> type[Serializer]:
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return DatasetListSerializer
        elif self.action == 'retrieve':
            return DatasetDetailSerializer
        elif self.action == 'upload':
            return DatasetUploadSerializer
        return DatasetListSerializer
    
    def list(self, request: Request) -> Response:
        """List all datasets for the authenticated user."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'], url_path='dashboard')
    def dashboard(self, request: Request) -> Response:
        """
        Get combined analytics across ALL user datasets.
        
        Returns overall summary statistics, type distribution, and chart-ready data
        aggregated from all datasets.
        """
        user_datasets = self.get_queryset()
        
        if not user_datasets.exists():
            return Response({
                'success': True,
                'datasets_count': 0,
                'total_equipment': 0,
                'summary': None,
                'chart_data': None
            })
        
        # Get all equipment from all user datasets
        all_equipment = Equipment.objects.filter(dataset__in=user_datasets)
        
        if not all_equipment.exists():
            return Response({
                'success': True,
                'datasets_count': user_datasets.count(),
                'total_equipment': 0,
                'summary': None,
                'chart_data': None
            })
        
        # Compute combined analytics
        analytics_service = AnalyticsService()
        analytics_data = analytics_service.compute_analytics(all_equipment)
        summary = analytics_service.get_summary_response(analytics_data)
        chart_data = analytics_service.get_chart_data(analytics_data)
        
        return Response({
            'success': True,
            'datasets_count': user_datasets.count(),
            'total_equipment': all_equipment.count(),
            'summary': summary,
            'chart_data': chart_data
        })
    
    @action(detail=False, methods=['post'], url_path='upload')
    def upload(self, request: Request) -> Response:
        """
        Upload a new CSV file and process equipment data.
        
        Accepts multipart/form-data with:
        - file: CSV file (required)
        - name: Custom dataset name (optional)
        """
        serializer = DatasetUploadSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_file = serializer.validated_data['file']
        custom_name = serializer.validated_data.get('name', uploaded_file.name)
        
        # Parse CSV file
        parser = CSVParserService()
        df, success = parser.parse_file(uploaded_file)
        
        if not success:
            return Response({
                'success': False,
                'errors': parser.get_errors(),
                'warnings': parser.get_warnings()
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                # Create dataset
                # Reset file position for storage
                uploaded_file.seek(0)
                
                dataset = Dataset.objects.create(
                    name=custom_name,
                    file=uploaded_file,
                    uploaded_by=request.user,
                    row_count=len(df)
                )
                
                # Create equipment records
                equipment_records = parser.to_equipment_dicts(df)
                equipment_objects = [
                    Equipment(
                        dataset=dataset,
                        name=record['name'],
                        type=record['type'],
                        flowrate=record['flowrate'],
                        pressure=record['pressure'],
                        temperature=record['temperature']
                    )
                    for record in equipment_records
                ]
                Equipment.objects.bulk_create(equipment_objects)
                
                # Compute and store analytics
                analytics_service = AnalyticsService()
                analytics_data = analytics_service.compute_analytics(dataset.equipment_items.all())
                
                AnalysisResult.objects.create(
                    dataset=dataset,
                    **{k: v for k, v in analytics_data.items() 
                       if k not in ['type_distribution', 'stats_by_type']},
                    type_distribution=analytics_data['type_distribution'],
                    stats_by_type=analytics_data['stats_by_type']
                )
                
                # Enforce maximum datasets limit
                self._enforce_dataset_limit(request.user)
                
                logger.info(f"Dataset '{custom_name}' uploaded successfully with {len(df)} records")
                
                return Response({
                    'success': True,
                    'message': f'Successfully uploaded {len(df)} equipment records',
                    'dataset_id': dataset.id,
                    'dataset': DatasetListSerializer(dataset).data,
                    'warnings': parser.get_warnings()
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            logger.exception("Error processing uploaded file")
            return Response({
                'success': False,
                'errors': [f'Error processing file: {str(e)}']
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _enforce_dataset_limit(self, user: AbstractUser) -> None:
        """Remove oldest datasets if user exceeds the limit."""
        max_datasets: int = getattr(settings, 'MAX_DATASETS_PER_USER', 5)
        user_datasets = Dataset.objects.filter(uploaded_by=user).order_by('-uploaded_at')
        
        if user_datasets.count() > max_datasets:
            for old_dataset in user_datasets[max_datasets:]:
                # Delete associated file
                if old_dataset.file:
                    old_dataset.file.delete(save=False)
                old_dataset.delete()
                logger.info(f"Removed old dataset: {old_dataset.name}")
    
    @action(detail=True, methods=['get'], url_path='analytics')
    def analytics(self, request: Request, pk: int | None = None) -> Response:
        """
        Get analytics for a specific dataset.
        
        Returns summary statistics, type distribution, and chart-ready data.
        """
        dataset = self.get_object()
        
        try:
            analysis = dataset.analysis
            analytics_service = AnalyticsService()
            
            # Convert stored analytics to response format
            analytics_data = {
                'total_count': analysis.total_count,
                'avg_flowrate': analysis.avg_flowrate,
                'avg_pressure': analysis.avg_pressure,
                'avg_temperature': analysis.avg_temperature,
                'min_flowrate': analysis.min_flowrate,
                'max_flowrate': analysis.max_flowrate,
                'min_pressure': analysis.min_pressure,
                'max_pressure': analysis.max_pressure,
                'min_temperature': analysis.min_temperature,
                'max_temperature': analysis.max_temperature,
                'std_flowrate': analysis.std_flowrate,
                'std_pressure': analysis.std_pressure,
                'std_temperature': analysis.std_temperature,
                'type_distribution': analysis.type_distribution,
                'stats_by_type': analysis.stats_by_type,
            }
            
            summary = analytics_service.get_summary_response(analytics_data)
            chart_data = analytics_service.get_chart_data(analytics_data)
            
            return Response({
                'dataset_id': dataset.id,
                'dataset_name': dataset.name,
                'summary': summary,
                'chart_data': chart_data,
                'computed_at': analysis.computed_at
            })
            
        except AnalysisResult.DoesNotExist:
            # Compute analytics on the fly if not cached
            analytics_service = AnalyticsService()
            analytics_data = analytics_service.compute_analytics(dataset.equipment_items.all())
            summary = analytics_service.get_summary_response(analytics_data)
            chart_data = analytics_service.get_chart_data(analytics_data)
            
            return Response({
                'dataset_id': dataset.id,
                'dataset_name': dataset.name,
                'summary': summary,
                'chart_data': chart_data,
                'computed_at': None
            })
    
    @action(detail=True, methods=['get'], url_path='equipment')
    def equipment_list(self, request: Request, pk: int | None = None) -> Response:
        """Get all equipment items for a dataset."""
        dataset: Dataset = self.get_object()
        equipment = dataset.equipment_items.all()
        serializer = EquipmentSerializer(equipment, many=True)
        
        return Response({
            'dataset_id': dataset.id,
            'dataset_name': dataset.name,
            'count': equipment.count(),
            'equipment': serializer.data
        })
    
    @action(detail=True, methods=['get'], url_path='pdf')
    def generate_pdf(self, request: Request, pk: int | None = None) -> Response | HttpResponse:
        """
        Generate and download a PDF report for the dataset.
        """
        dataset: Dataset = self.get_object()
        
        try:
            # Get analytics data
            try:
                analysis = dataset.analysis
                analytics_data = {
                    'total_count': analysis.total_count,
                    'avg_flowrate': analysis.avg_flowrate,
                    'avg_pressure': analysis.avg_pressure,
                    'avg_temperature': analysis.avg_temperature,
                    'min_flowrate': analysis.min_flowrate,
                    'max_flowrate': analysis.max_flowrate,
                    'min_pressure': analysis.min_pressure,
                    'max_pressure': analysis.max_pressure,
                    'min_temperature': analysis.min_temperature,
                    'max_temperature': analysis.max_temperature,
                    'std_flowrate': analysis.std_flowrate,
                    'std_pressure': analysis.std_pressure,
                    'std_temperature': analysis.std_temperature,
                    'type_distribution': analysis.type_distribution,
                    'stats_by_type': analysis.stats_by_type,
                }
            except AnalysisResult.DoesNotExist:
                analytics_service = AnalyticsService()
                analytics_data = analytics_service.compute_analytics(dataset.equipment_items.all())
            
            # Get equipment data
            equipment_data = list(dataset.equipment_items.values(
                'name', 'type', 'flowrate', 'pressure', 'temperature'
            ))
            
            # Generate PDF
            pdf_service = PDFReportService()
            pdf_content = pdf_service.generate_report(
                dataset_name=dataset.name,
                uploaded_at=dataset.uploaded_at,
                analytics=analytics_data,
                equipment_data=equipment_data
            )
            
            # Return PDF response
            response = HttpResponse(pdf_content, content_type='application/pdf')
            filename = f"equipment_report_{dataset.id}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            return response
            
        except Exception as e:
            logger.exception("Error generating PDF report")
            return Response({
                'error': f'Failed to generate PDF: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Delete a dataset and its associated file."""
        instance: Dataset = self.get_object()
        
        # Delete the uploaded file
        if instance.file:
            instance.file.delete(save=False)
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EquipmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only ViewSet for equipment items.
    
    Provides list and retrieve operations for individual equipment records.
    """
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self) -> QuerySet[Equipment]:
        """Return equipment items from user's datasets."""
        return Equipment.objects.filter(
            dataset__uploaded_by=self.request.user
        ).select_related('dataset')
    
    def list(self, request: Request) -> Response:
        """List equipment with optional filtering."""
        queryset = self.get_queryset()
        
        # Filter by dataset if provided
        dataset_id = request.query_params.get('dataset')
        if dataset_id:
            queryset = queryset.filter(dataset_id=dataset_id)
        
        # Filter by type if provided
        equipment_type = request.query_params.get('type')
        if equipment_type:
            queryset = queryset.filter(type__iexact=equipment_type)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })
