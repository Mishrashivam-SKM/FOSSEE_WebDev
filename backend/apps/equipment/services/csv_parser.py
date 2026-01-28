"""
CSV Parser Service for processing uploaded equipment data files.
"""

import pandas as pd
from typing import Tuple, List, Dict, Any
from io import StringIO
import logging

logger = logging.getLogger(__name__)


class CSVParserError(Exception):
    """Custom exception for CSV parsing errors."""
    pass


class CSVParserService:
    """
    Service for parsing and validating CSV files containing equipment data.
    """
    
    REQUIRED_COLUMNS = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    COLUMN_MAPPING = {
        'Equipment Name': 'name',
        'Type': 'type',
        'Flowrate': 'flowrate',
        'Pressure': 'pressure',
        'Temperature': 'temperature'
    }
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def parse_file(self, file_obj) -> Tuple[pd.DataFrame, bool]:
        """
        Parse a CSV file and return a DataFrame.
        
        Args:
            file_obj: Uploaded file object
            
        Returns:
            Tuple of (DataFrame, success_flag)
        """
        self.errors = []
        self.warnings = []
        
        try:
            # Read the file content
            content = file_obj.read()
            
            # Try to decode as UTF-8, fallback to latin-1
            try:
                content_str = content.decode('utf-8')
            except UnicodeDecodeError:
                content_str = content.decode('latin-1')
                self.warnings.append("File was not UTF-8 encoded, used latin-1 encoding.")
            
            # Parse CSV
            df = pd.read_csv(StringIO(content_str))
            
            # Validate structure
            if not self._validate_columns(df):
                return pd.DataFrame(), False
            
            # Clean and validate data
            df = self._clean_data(df)
            
            if not self._validate_data(df):
                return pd.DataFrame(), False
            
            # Rename columns to match model fields
            df = df.rename(columns=self.COLUMN_MAPPING)
            
            logger.info(f"Successfully parsed CSV with {len(df)} records")
            return df, True
            
        except pd.errors.EmptyDataError:
            self.errors.append("The uploaded file is empty.")
            return pd.DataFrame(), False
        except pd.errors.ParserError as e:
            self.errors.append(f"Failed to parse CSV: {str(e)}")
            return pd.DataFrame(), False
        except Exception as e:
            logger.exception("Unexpected error parsing CSV")
            self.errors.append(f"Unexpected error: {str(e)}")
            return pd.DataFrame(), False
    
    def _validate_columns(self, df: pd.DataFrame) -> bool:
        """Validate that all required columns are present."""
        missing_columns = []
        
        for col in self.REQUIRED_COLUMNS:
            if col not in df.columns:
                # Try case-insensitive match
                matched = False
                for actual_col in df.columns:
                    if actual_col.lower().strip() == col.lower():
                        df.rename(columns={actual_col: col}, inplace=True)
                        matched = True
                        break
                if not matched:
                    missing_columns.append(col)
        
        if missing_columns:
            self.errors.append(f"Missing required columns: {', '.join(missing_columns)}")
            return False
        
        return True
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess the data."""
        # Remove completely empty rows
        df = df.dropna(how='all')
        
        # Strip whitespace from string columns
        for col in ['Equipment Name', 'Type']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        # Convert numeric columns
        for col in ['Flowrate', 'Pressure', 'Temperature']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def _validate_data(self, df: pd.DataFrame) -> bool:
        """Validate data integrity."""
        if df.empty:
            self.errors.append("No valid data rows found in the file.")
            return False
        
        # Check for null values in required columns
        null_counts = df[self.REQUIRED_COLUMNS].isnull().sum()
        null_columns = null_counts[null_counts > 0]
        
        if not null_columns.empty:
            for col, count in null_columns.items():
                self.warnings.append(f"Column '{col}' has {count} missing values.")
        
        # Drop rows with null values in numeric columns
        original_count = len(df)
        df_clean = df.dropna(subset=['Flowrate', 'Pressure', 'Temperature'])
        dropped = original_count - len(df_clean)
        
        if dropped > 0:
            self.warnings.append(f"Dropped {dropped} rows with missing numeric values.")
        
        if df_clean.empty:
            self.errors.append("No valid data rows after cleaning.")
            return False
        
        # Validate numeric ranges (basic sanity checks)
        for col in ['Flowrate', 'Pressure', 'Temperature']:
            if (df[col] < 0).any():
                self.warnings.append(f"Column '{col}' contains negative values.")
        
        return True
    
    def get_errors(self) -> List[str]:
        """Return list of parsing errors."""
        return self.errors
    
    def get_warnings(self) -> List[str]:
        """Return list of parsing warnings."""
        return self.warnings
    
    def to_equipment_dicts(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Convert DataFrame to list of equipment dictionaries.
        
        Args:
            df: Cleaned and validated DataFrame
            
        Returns:
            List of dictionaries ready for model creation
        """
        return df.to_dict('records')
