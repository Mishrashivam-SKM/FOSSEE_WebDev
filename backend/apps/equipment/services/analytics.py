"""
Analytics Service for computing equipment data statistics.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
from django.db.models import QuerySet
import logging

logger = logging.getLogger(__name__)


class AnalyticsService:
    """
    Service for computing analytics and statistics on equipment data.
    """
    
    def __init__(self):
        pass
    
    def compute_analytics(self, equipment_queryset: QuerySet) -> Dict[str, Any]:
        """
        Compute comprehensive analytics from equipment queryset.
        
        Args:
            equipment_queryset: QuerySet of Equipment objects
            
        Returns:
            Dictionary containing all computed analytics
        """
        # Convert queryset to DataFrame for efficient computation
        df = pd.DataFrame.from_records(
            equipment_queryset.values('name', 'type', 'flowrate', 'pressure', 'temperature')
        )
        
        if df.empty:
            return self._empty_analytics()
        
        analytics = {
            'total_count': len(df),
            'avg_flowrate': float(df['flowrate'].mean()),
            'avg_pressure': float(df['pressure'].mean()),
            'avg_temperature': float(df['temperature'].mean()),
            'min_flowrate': float(df['flowrate'].min()),
            'max_flowrate': float(df['flowrate'].max()),
            'min_pressure': float(df['pressure'].min()),
            'max_pressure': float(df['pressure'].max()),
            'min_temperature': float(df['temperature'].min()),
            'max_temperature': float(df['temperature'].max()),
            'std_flowrate': float(df['flowrate'].std()) if len(df) > 1 else 0.0,
            'std_pressure': float(df['pressure'].std()) if len(df) > 1 else 0.0,
            'std_temperature': float(df['temperature'].std()) if len(df) > 1 else 0.0,
            'type_distribution': self._compute_type_distribution(df),
            'stats_by_type': self._compute_stats_by_type(df),
        }
        
        return analytics
    
    def _compute_type_distribution(self, df: pd.DataFrame) -> Dict[str, int]:
        """Compute distribution of equipment types."""
        return df['type'].value_counts().to_dict()
    
    def _compute_stats_by_type(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """Compute statistics grouped by equipment type."""
        stats_by_type = {}
        
        for equipment_type in df['type'].unique():
            type_df = df[df['type'] == equipment_type]
            
            stats_by_type[equipment_type] = {
                'count': len(type_df),
                'flowrate': {
                    'avg': float(type_df['flowrate'].mean()),
                    'min': float(type_df['flowrate'].min()),
                    'max': float(type_df['flowrate'].max()),
                    'std': float(type_df['flowrate'].std()) if len(type_df) > 1 else 0.0,
                },
                'pressure': {
                    'avg': float(type_df['pressure'].mean()),
                    'min': float(type_df['pressure'].min()),
                    'max': float(type_df['pressure'].max()),
                    'std': float(type_df['pressure'].std()) if len(type_df) > 1 else 0.0,
                },
                'temperature': {
                    'avg': float(type_df['temperature'].mean()),
                    'min': float(type_df['temperature'].min()),
                    'max': float(type_df['temperature'].max()),
                    'std': float(type_df['temperature'].std()) if len(type_df) > 1 else 0.0,
                },
            }
        
        return stats_by_type
    
    def _empty_analytics(self) -> Dict[str, Any]:
        """Return empty analytics structure."""
        return {
            'total_count': 0,
            'avg_flowrate': 0.0,
            'avg_pressure': 0.0,
            'avg_temperature': 0.0,
            'min_flowrate': 0.0,
            'max_flowrate': 0.0,
            'min_pressure': 0.0,
            'max_pressure': 0.0,
            'min_temperature': 0.0,
            'max_temperature': 0.0,
            'std_flowrate': 0.0,
            'std_pressure': 0.0,
            'std_temperature': 0.0,
            'type_distribution': {},
            'stats_by_type': {},
        }
    
    def get_summary_response(self, analytics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format analytics for API summary response.
        
        Args:
            analytics: Raw analytics dictionary
            
        Returns:
            Formatted summary for API response
        """
        return {
            'total_count': analytics['total_count'],
            'equipment_types': list(analytics['type_distribution'].keys()),
            'averages': {
                'flowrate': round(analytics['avg_flowrate'], 2),
                'pressure': round(analytics['avg_pressure'], 2),
                'temperature': round(analytics['avg_temperature'], 2),
            },
            'ranges': {
                'flowrate': {
                    'min': round(analytics['min_flowrate'], 2),
                    'max': round(analytics['max_flowrate'], 2),
                },
                'pressure': {
                    'min': round(analytics['min_pressure'], 2),
                    'max': round(analytics['max_pressure'], 2),
                },
                'temperature': {
                    'min': round(analytics['min_temperature'], 2),
                    'max': round(analytics['max_temperature'], 2),
                },
            },
            'type_distribution': analytics['type_distribution'],
            'stats_by_type': analytics['stats_by_type'],
        }
    
    def get_chart_data(self, analytics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare data formatted for chart visualization.
        
        Args:
            analytics: Raw analytics dictionary
            
        Returns:
            Data formatted for charts
        """
        type_distribution = analytics['type_distribution']
        stats_by_type = analytics['stats_by_type']
        
        # Bar chart data - averages by type
        types = list(stats_by_type.keys())
        
        bar_chart_data = {
            'labels': types,
            'datasets': [
                {
                    'label': 'Avg Flowrate',
                    'data': [stats_by_type[t]['flowrate']['avg'] for t in types],
                },
                {
                    'label': 'Avg Pressure',
                    'data': [stats_by_type[t]['pressure']['avg'] for t in types],
                },
                {
                    'label': 'Avg Temperature',
                    'data': [stats_by_type[t]['temperature']['avg'] for t in types],
                },
            ]
        }
        
        # Pie chart data - type distribution
        pie_chart_data = {
            'labels': list(type_distribution.keys()),
            'data': list(type_distribution.values()),
        }
        
        return {
            'bar_chart': bar_chart_data,
            'pie_chart': pie_chart_data,
        }
