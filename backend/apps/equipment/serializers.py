"""
DRF Serializers for Equipment management.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dataset, Equipment, AnalysisResult


class EquipmentSerializer(serializers.ModelSerializer):
    """Serializer for Equipment model."""
    
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'type', 'flowrate', 'pressure', 'temperature']
        read_only_fields = ['id']


class EquipmentDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Equipment including dataset info."""
    dataset_name = serializers.CharField(source='dataset.name', read_only=True)
    
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'type', 'flowrate', 'pressure', 'temperature', 'dataset', 'dataset_name']
        read_only_fields = ['id', 'dataset', 'dataset_name']


class AnalysisResultSerializer(serializers.ModelSerializer):
    """Serializer for AnalysisResult model."""
    
    class Meta:
        model = AnalysisResult
        fields = [
            'id', 'total_count',
            'avg_flowrate', 'avg_pressure', 'avg_temperature',
            'min_flowrate', 'max_flowrate',
            'min_pressure', 'max_pressure',
            'min_temperature', 'max_temperature',
            'std_flowrate', 'std_pressure', 'std_temperature',
            'type_distribution', 'stats_by_type',
            'computed_at'
        ]
        read_only_fields = fields


class DatasetListSerializer(serializers.ModelSerializer):
    """Serializer for Dataset list view."""
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    has_analysis = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = ['id', 'name', 'uploaded_by', 'uploaded_by_username', 'uploaded_at', 'row_count', 'has_analysis']
        read_only_fields = fields
    
    def get_has_analysis(self, obj):
        return hasattr(obj, 'analysis')


class DatasetDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Dataset including equipment and analysis."""
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    equipment_items = EquipmentSerializer(many=True, read_only=True)
    analysis = AnalysisResultSerializer(read_only=True)
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'name', 'uploaded_by', 'uploaded_by_username',
            'uploaded_at', 'row_count', 'equipment_items', 'analysis'
        ]
        read_only_fields = fields


class DatasetUploadSerializer(serializers.Serializer):
    """Serializer for CSV file upload."""
    file = serializers.FileField(
        help_text="CSV file containing equipment data"
    )
    name = serializers.CharField(
        max_length=255,
        required=False,
        help_text="Optional custom name for the dataset"
    )
    
    def validate_file(self, value):
        """Validate that the uploaded file is a CSV."""
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed.")
        
        # Check file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size must be less than 10MB.")
        
        return value


class SummaryStatisticsSerializer(serializers.Serializer):
    """Serializer for summary statistics response."""
    total_count = serializers.IntegerField()
    equipment_types = serializers.ListField(child=serializers.CharField())
    averages = serializers.DictField()
    ranges = serializers.DictField()
    type_distribution = serializers.DictField()
