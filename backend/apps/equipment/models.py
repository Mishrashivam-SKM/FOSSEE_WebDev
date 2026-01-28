"""
Database models for Equipment management.
"""

from django.db import models
from django.contrib.auth.models import User


class Dataset(models.Model):
    """
    Stores uploaded CSV dataset metadata.
    Represents a single CSV file upload containing equipment data.
    """
    name = models.CharField(max_length=255, help_text="Dataset name/filename")
    file = models.FileField(upload_to='uploads/', help_text="Uploaded CSV file")
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='datasets',
        help_text="User who uploaded the dataset"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    row_count = models.IntegerField(default=0, help_text="Number of equipment records")
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Dataset'
        verbose_name_plural = 'Datasets'
    
    def __str__(self):
        return f"{self.name} ({self.uploaded_at.strftime('%Y-%m-%d %H:%M')})"


class Equipment(models.Model):
    """
    Stores individual equipment records from CSV.
    Each record represents a single piece of chemical equipment.
    """
    EQUIPMENT_TYPES = [
        ('Pump', 'Pump'),
        ('Compressor', 'Compressor'),
        ('Valve', 'Valve'),
        ('HeatExchanger', 'Heat Exchanger'),
        ('Reactor', 'Reactor'),
        ('Condenser', 'Condenser'),
        ('Other', 'Other'),
    ]
    
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name='equipment_items',
        help_text="Parent dataset"
    )
    name = models.CharField(max_length=255, help_text="Equipment name/identifier")
    type = models.CharField(
        max_length=100,
        help_text="Equipment type/category"
    )
    flowrate = models.FloatField(help_text="Flow rate measurement")
    pressure = models.FloatField(help_text="Pressure measurement")
    temperature = models.FloatField(help_text="Temperature measurement")
    
    class Meta:
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipment'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.type})"


class AnalysisResult(models.Model):
    """
    Stores pre-computed analytics for a dataset.
    Cached analytics data for performance optimization.
    """
    dataset = models.OneToOneField(
        Dataset,
        on_delete=models.CASCADE,
        related_name='analysis',
        help_text="Related dataset"
    )
    
    # Aggregate statistics
    total_count = models.IntegerField(default=0)
    avg_flowrate = models.FloatField(default=0.0)
    avg_pressure = models.FloatField(default=0.0)
    avg_temperature = models.FloatField(default=0.0)
    
    min_flowrate = models.FloatField(default=0.0)
    max_flowrate = models.FloatField(default=0.0)
    min_pressure = models.FloatField(default=0.0)
    max_pressure = models.FloatField(default=0.0)
    min_temperature = models.FloatField(default=0.0)
    max_temperature = models.FloatField(default=0.0)
    
    # Standard deviations
    std_flowrate = models.FloatField(default=0.0)
    std_pressure = models.FloatField(default=0.0)
    std_temperature = models.FloatField(default=0.0)
    
    # Type distribution stored as JSON
    type_distribution = models.JSONField(
        default=dict,
        help_text="Distribution of equipment types"
    )
    
    # Statistics by type stored as JSON
    stats_by_type = models.JSONField(
        default=dict,
        help_text="Detailed statistics grouped by equipment type"
    )
    
    computed_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Analysis Result'
        verbose_name_plural = 'Analysis Results'
    
    def __str__(self):
        return f"Analysis for {self.dataset.name}"
