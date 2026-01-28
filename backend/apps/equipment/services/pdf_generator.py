"""
PDF Report Generator Service for equipment data reports.
"""

import io
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    Image, PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PDFReportService:
    """
    Service for generating PDF reports for equipment data analysis.
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Set up custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1a365d')
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.HexColor('#2c5282')
        ))
        
        self.styles.add(ParagraphStyle(
            name='SubHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceBefore=10,
            spaceAfter=5,
            textColor=colors.HexColor('#4a5568')
        ))
        
        self.styles.add(ParagraphStyle(
            name='FooterStyle',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.grey
        ))
    
    def generate_report(
        self,
        dataset_name: str,
        uploaded_at: datetime,
        analytics: Dict[str, Any],
        equipment_data: List[Dict[str, Any]]
    ) -> bytes:
        """
        Generate a complete PDF report.
        
        Args:
            dataset_name: Name of the dataset
            uploaded_at: Upload timestamp
            analytics: Analytics data dictionary
            equipment_data: List of equipment records
            
        Returns:
            PDF file as bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        elements = []
        
        # Title
        elements.append(Paragraph(
            "Chemical Equipment Analysis Report",
            self.styles['CustomTitle']
        ))
        
        # Dataset info
        elements.append(Paragraph(
            f"Dataset: {dataset_name}",
            self.styles['Normal']
        ))
        elements.append(Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            self.styles['Normal']
        ))
        elements.append(Paragraph(
            f"Data Uploaded: {uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}",
            self.styles['Normal']
        ))
        
        elements.append(Spacer(1, 20))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
        elements.append(Spacer(1, 20))
        
        # Summary Section
        elements.append(Paragraph("Summary Statistics", self.styles['SectionHeader']))
        elements.extend(self._create_summary_table(analytics))
        
        elements.append(Spacer(1, 20))
        
        # Type Distribution Section
        elements.append(Paragraph("Equipment Type Distribution", self.styles['SectionHeader']))
        elements.extend(self._create_type_distribution_table(analytics))
        
        # Charts
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("Visualizations", self.styles['SectionHeader']))
        
        # Generate and add charts
        chart_images = self._generate_charts(analytics)
        for chart_name, chart_buffer in chart_images.items():
            elements.append(Paragraph(chart_name, self.styles['SubHeader']))
            elements.append(Image(chart_buffer, width=6*inch, height=4*inch))
            elements.append(Spacer(1, 10))
        
        # Equipment Data Table (first 20 records)
        elements.append(PageBreak())
        elements.append(Paragraph("Equipment Data Sample", self.styles['SectionHeader']))
        elements.extend(self._create_equipment_table(equipment_data[:20]))
        
        if len(equipment_data) > 20:
            elements.append(Paragraph(
                f"... and {len(equipment_data) - 20} more records",
                self.styles['Normal']
            ))
        
        # Footer
        elements.append(Spacer(1, 30))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
        elements.append(Paragraph(
            "Generated by Chemical Equipment Parameter Visualizer",
            self.styles['FooterStyle']
        ))
        
        # Build PDF
        doc.build(elements)
        
        pdf_content = buffer.getvalue()
        buffer.close()
        
        return pdf_content
    
    def _create_summary_table(self, analytics: Dict[str, Any]) -> List:
        """Create summary statistics table."""
        data = [
            ['Metric', 'Flowrate', 'Pressure', 'Temperature'],
            ['Average', 
             f"{analytics.get('avg_flowrate', 0):.2f}",
             f"{analytics.get('avg_pressure', 0):.2f}",
             f"{analytics.get('avg_temperature', 0):.2f}"],
            ['Minimum',
             f"{analytics.get('min_flowrate', 0):.2f}",
             f"{analytics.get('min_pressure', 0):.2f}",
             f"{analytics.get('min_temperature', 0):.2f}"],
            ['Maximum',
             f"{analytics.get('max_flowrate', 0):.2f}",
             f"{analytics.get('max_pressure', 0):.2f}",
             f"{analytics.get('max_temperature', 0):.2f}"],
            ['Std Dev',
             f"{analytics.get('std_flowrate', 0):.2f}",
             f"{analytics.get('std_pressure', 0):.2f}",
             f"{analytics.get('std_temperature', 0):.2f}"],
        ]
        
        table = Table(data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7fafc')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        return [table, Spacer(1, 10)]
    
    def _create_type_distribution_table(self, analytics: Dict[str, Any]) -> List:
        """Create equipment type distribution table."""
        type_dist = analytics.get('type_distribution', {})
        total = sum(type_dist.values()) if type_dist else 1
        
        data = [['Equipment Type', 'Count', 'Percentage']]
        for eq_type, count in type_dist.items():
            percentage = (count / total) * 100 if total > 0 else 0
            data.append([eq_type, str(count), f"{percentage:.1f}%"])
        
        if len(data) == 1:
            data.append(['No data available', '-', '-'])
        
        table = Table(data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7fafc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        return [table, Spacer(1, 10)]
    
    def _create_equipment_table(self, equipment_data: List[Dict[str, Any]]) -> List:
        """Create equipment data table."""
        data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
        
        for eq in equipment_data:
            data.append([
                str(eq.get('name', ''))[:20],  # Truncate long names
                str(eq.get('type', '')),
                f"{eq.get('flowrate', 0):.2f}",
                f"{eq.get('pressure', 0):.2f}",
                f"{eq.get('temperature', 0):.2f}",
            ])
        
        table = Table(data, colWidths=[1.4*inch, 1.2*inch, 1.1*inch, 1.1*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#edf2f7')]),
        ]))
        
        return [table]
    
    def _generate_charts(self, analytics: Dict[str, Any]) -> Dict[str, io.BytesIO]:
        """Generate chart images for the report."""
        charts = {}
        
        # Type Distribution Pie Chart
        type_dist = analytics.get('type_distribution', {})
        if type_dist:
            fig, ax = plt.subplots(figsize=(8, 6))
            colors_list = plt.cm.Set3(range(len(type_dist)))
            
            wedges, texts, autotexts = ax.pie(
                type_dist.values(),
                labels=type_dist.keys(),
                autopct='%1.1f%%',
                colors=colors_list,
                startangle=90
            )
            ax.set_title('Equipment Type Distribution', fontsize=14, fontweight='bold')
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            charts['Equipment Type Distribution'] = buffer
            plt.close(fig)
        
        # Average Parameters by Type Bar Chart
        stats_by_type = analytics.get('stats_by_type', {})
        if stats_by_type:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            types = list(stats_by_type.keys())
            x = range(len(types))
            width = 0.25
            
            flowrates = [stats_by_type[t]['flowrate']['avg'] for t in types]
            pressures = [stats_by_type[t]['pressure']['avg'] for t in types]
            temps = [stats_by_type[t]['temperature']['avg'] for t in types]
            
            bars1 = ax.bar([i - width for i in x], flowrates, width, label='Flowrate', color='#4299e1')
            bars2 = ax.bar(x, pressures, width, label='Pressure', color='#48bb78')
            bars3 = ax.bar([i + width for i in x], temps, width, label='Temperature', color='#ed8936')
            
            ax.set_xlabel('Equipment Type', fontsize=11)
            ax.set_ylabel('Average Value', fontsize=11)
            ax.set_title('Average Parameters by Equipment Type', fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(types, rotation=45, ha='right')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            charts['Average Parameters by Type'] = buffer
            plt.close(fig)
        
        return charts
