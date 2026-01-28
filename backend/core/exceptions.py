"""
Custom exceptions for the application.
"""

from rest_framework.exceptions import APIException


class CSVParsingError(APIException):
    """Exception raised when CSV parsing fails."""
    status_code = 400
    default_detail = 'Failed to parse CSV file.'
    default_code = 'csv_parsing_error'


class AnalyticsError(APIException):
    """Exception raised when analytics computation fails."""
    status_code = 500
    default_detail = 'Failed to compute analytics.'
    default_code = 'analytics_error'


class PDFGenerationError(APIException):
    """Exception raised when PDF generation fails."""
    status_code = 500
    default_detail = 'Failed to generate PDF report.'
    default_code = 'pdf_generation_error'


class DatasetLimitExceeded(APIException):
    """Exception raised when user exceeds dataset limit."""
    status_code = 400
    default_detail = 'Maximum number of datasets reached. Please delete an existing dataset.'
    default_code = 'dataset_limit_exceeded'
