from django.contrib import admin
from .models import Dataset, Equipment, AnalysisResult


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_by', 'uploaded_at', 'row_count')
    list_filter = ('uploaded_at', 'uploaded_by')
    search_fields = ('name',)
    readonly_fields = ('uploaded_at', 'row_count')
    ordering = ('-uploaded_at',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'flowrate', 'pressure', 'temperature', 'dataset')
    list_filter = ('type', 'dataset')
    search_fields = ('name', 'type')
    ordering = ('name',)


@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('dataset', 'total_count', 'avg_flowrate', 'avg_pressure', 'avg_temperature', 'computed_at')
    readonly_fields = ('computed_at',)
