#!/usr/bin/env python3
"""
Data Analyzer Script - Basic Statistics with Pandas

This script demonstrates various data analysis techniques using pandas,
including data loading, cleaning, statistical analysis, and data manipulation.

Author: Python Learning Series
Dependencies: pandas, numpy
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union


class DataAnalyzer:
    """
    A comprehensive data analysis class that provides methods for loading,
    cleaning, and analyzing datasets using pandas.
    """
    
    def __init__(self, data: Optional[Union[str, pd.DataFrame]] = None):
        """
        Initialize the DataAnalyzer.
        
        Args:
            data: Path to CSV file or pandas DataFrame
        """
        self.df = None
        self.original_df = None
        
        if data is not None:
            self.load_data(data)
    
    def load_data(self, source: Union[str, pd.DataFrame]) -> bool:
        """
        Load data from various sources.
        
        Args:
            source: Path to CSV file or pandas DataFrame
            
        Returns:
            bool: True if data loaded successfully, False otherwise
        """
        try:
            if isinstance(source, str):
                # Load from CSV file
                if not Path(source).exists():
                    print(f"Error: File '{source}' not found.")
                    return False
                
                self.df = pd.read_csv(source)
                print(f"Successfully loaded data from '{source}'")
                
            elif isinstance(source, pd.DataFrame):
                # Load from DataFrame
                self.df = source.copy()
                print("Successfully loaded DataFrame")
                
            else:
                raise ValueError("Source must be a file path (str) or pandas DataFrame")
            
            # Keep a copy of original data
            self.original_df = self.df.copy()
            print(f"Dataset shape: {self.df.shape}")
            return True
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def get_basic_info(self) -> Dict:
        """
        Get basic information about the dataset.
        
        Returns:
            Dict: Dictionary containing basic dataset information
        """
        if self.df is None:
            print("No data loaded. Please load data first.")
            return {}
        
        try:
            info = {
                'shape': self.df.shape,
                'columns': list(self.df.columns),
                'dtypes': dict(self.df.dtypes),
                'memory_usage': self.df.memory_usage(deep=True).sum(),
                'null_values': dict(self.df.isnull().sum()),
                'duplicate_rows': self.df.duplicated().sum()
            }
            
            print("=== DATASET BASIC INFORMATION ===")
            print(f"Shape: {info['shape'][0]} rows × {info['shape'][1]} columns")
            print(f"Memory usage: {info['memory_usage'] / 1024:.2f} KB")
            print(f"Duplicate rows: {info['duplicate_rows']}")
            print(f"Columns with null values: {sum(1 for v in info['null_values'].values() if v > 0)}")
            
            return info
            
        except Exception as e:
            print(f"Error getting basic info: {e}")
            return {}
    
    def get_descriptive_statistics(self, numeric_only: bool = True) -> Optional[pd.DataFrame]:
        """
        Generate descriptive statistics for the dataset.
        
        Args:
            numeric_only: Whether to include only numeric columns
            
        Returns:
            pd.DataFrame: Descriptive statistics
        """
        if self.df is None:
            print("No data loaded. Please load data first.")
            return None
        
        try:
            if numeric_only:
                stats = self.df.describe()
            else:
                stats = self.df.describe(include='all')
            
            print("=== DESCRIPTIVE STATISTICS ===")
            print(stats)
            return stats
            
        except Exception as e:
            print(f"Error generating descriptive statistics: {e}")
            return None
    
    def find_outliers(self, column: str, method: str = 'iqr') -> Optional[pd.Series]:
        """
        Find outliers in a numeric column using IQR or Z-score method.
        
        Args:
            column: Column name to analyze
            method: 'iqr' for Interquartile Range or 'zscore' for Z-score method
            
        Returns:
            pd.Series: Boolean series indicating outliers
        """
        if self.df is None or column not in self.df.columns:
            print(f"Column '{column}' not found in dataset.")
            return None
        
        if not pd.api.types.is_numeric_dtype(self.df[column]):
            print(f"Column '{column}' is not numeric.")
            return None
        
        try:
            if method.lower() == 'iqr':
                # Interquartile Range method
                Q1 = self.df[column].quantile(0.25)
                Q3 = self.df[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = (self.df[column] < lower_bound) | (self.df[column] > upper_bound)
                
            elif method.lower() == 'zscore':
                # Z-score method (assuming normal distribution)
                z_scores = np.abs((self.df[column] - self.df[column].mean()) / self.df[column].std())
                outliers = z_scores > 3
                
            else:
                raise ValueError("Method must be 'iqr' or 'zscore'")
            
            outlier_count = outliers.sum()
            print(f"Found {outlier_count} outliers in column '{column}' using {method.upper()} method")
            
            if outlier_count > 0:
                print("Outlier values:")
                print(self.df[outliers][column].values)
            
            return outliers
            
        except Exception as e:
            print(f"Error finding outliers: {e}")
            return None
    
    def analyze_correlations(self, method: str = 'pearson') -> Optional[pd.DataFrame]:
        """
        Analyze correlations between numeric columns.
        
        Args:
            method: Correlation method ('pearson', 'kendall', or 'spearman')
            
        Returns:
            pd.DataFrame: Correlation matrix
        """
        if self.df is None:
            print("No data loaded. Please load data first.")
            return None
        
        try:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) < 2:
                print("Need at least 2 numeric columns for correlation analysis.")
                return None
            
            corr_matrix = self.df[numeric_cols].corr(method=method)
            
            print(f"=== CORRELATION MATRIX ({method.upper()}) ===")
            print(corr_matrix.round(3))
            
            # Find strong correlations (> 0.7 or < -0.7)
            strong_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.7:
                        strong_corr.append((
                            corr_matrix.columns[i],
                            corr_matrix.columns[j],
                            corr_val
                        ))
            
            if strong_corr:
                print("\n=== STRONG CORRELATIONS (|r| > 0.7) ===")
                for col1, col2, corr_val in strong_corr:
                    print(f"{col1} ↔ {col2}: {corr_val:.3f}")
            
            return corr_matrix
            
        except Exception as e:
            print(f"Error analyzing correlations: {e}")
            return None
    
    def group_analysis(self, group_by: str, target_col: str, 
                      agg_functions: List[str] = None) -> Optional[pd.DataFrame]:
        """
        Perform group-by analysis.
        
        Args:
            group_by: Column to group by
            target_col: Target column for aggregation
            agg_functions: List of aggregation functions
            
        Returns:
            pd.DataFrame: Grouped analysis results
        """
        if self.df is None:
            print("No data loaded. Please load data first.")
            return None
        
        if group_by not in self.df.columns or target_col not in self.df.columns:
            print("Specified columns not found in dataset.")
            return None
        
        if agg_functions is None:
            agg_functions = ['count', 'mean', 'std', 'min', 'max']
        
        try:
            grouped = self.df.groupby(group_by)[target_col].agg(agg_functions)
            
            print(f"=== GROUP ANALYSIS: {group_by} → {target_col} ===")
            print(grouped)
            
            return grouped
            
        except Exception as e:
            print(f"Error in group analysis: {e}")
            return None
    
    def clean_data(self, drop_duplicates: bool = True, 
                   handle_nulls: str = 'drop') -> bool:
        """
        Clean the dataset by handling duplicates and null values.
        
        Args:
            drop_duplicates: Whether to drop duplicate rows
            handle_nulls: How to handle null values ('drop', 'fill_mean', 'fill_median')
            
        Returns:
            bool: True if cleaning successful
        """
        if self.df is None:
            print("No data loaded. Please load data first.")
            return False
        
        try:
            initial_shape = self.df.shape
            
            # Handle duplicates
            if drop_duplicates:
                duplicates_count = self.df.duplicated().sum()
                self.df = self.df.drop_duplicates()
                print(f"Dropped {duplicates_count} duplicate rows")
            
            # Handle null values
            null_count = self.df.isnull().sum().sum()
            if null_count > 0:
                if handle_nulls == 'drop':
                    self.df = self.df.dropna()
                    print(f"Dropped rows with null values")
                    
                elif handle_nulls == 'fill_mean':
                    numeric_cols = self.df.select_dtypes(include=[np.number]).columns
                    self.df[numeric_cols] = self.df[numeric_cols].fillna(
                        self.df[numeric_cols].mean()
                    )
                    print("Filled null values with column means")
                    
                elif handle_nulls == 'fill_median':
                    numeric_cols = self.df.select_dtypes(include=[np.number]).columns
                    self.df[numeric_cols] = self.df[numeric_cols].fillna(
                        self.df[numeric_cols].median()
                    )
                    print("Filled null values with column medians")
            
            final_shape = self.df.shape
            print(f"Data cleaned: {initial_shape} → {final_shape}")
            
            return True
            
        except Exception as e:
            print(f"Error cleaning data: {e}")
            return False
    
    def export_results(self, filename: str, include_stats: bool = True) -> bool:
        """
        Export analysis results to a file.
        
        Args:
            filename: Output filename
            include_stats: Whether to include descriptive statistics
            
        Returns:
            bool: True if export successful
        """
        if self.df is None:
            print("No data loaded. Please load data first.")
            return False
        
        try:
            # Export cleaned data
            self.df.to_csv(filename, index=False)
            print(f"Data exported to '{filename}'")
            
            # Export statistics if requested
            if include_stats:
                stats_filename = filename.replace('.csv', '_stats.txt')
                with open(stats_filename, 'w') as f:
                    f.write("DATASET ANALYSIS REPORT\n")
                    f.write("=" * 50 + "\n\n")
                    
                    f.write(f"Original shape: {self.original_df.shape}\n")
                    f.write(f"Cleaned shape: {self.df.shape}\n\n")
                    
                    f.write("DESCRIPTIVE STATISTICS:\n")
                    f.write(str(self.df.describe()))
                    
                print(f"Statistics exported to '{stats_filename}'")
            
            return True
            
        except Exception as e:
            print(f"Error exporting results: {e}")
            return False


def create_sample_data() -> pd.DataFrame:
    """
    Create a sample dataset for demonstration purposes.
    
    Returns:
        pd.DataFrame: Sample dataset
    """
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'age': np.random.randint(18, 80, n_samples),
        'income': np.random.normal(50000, 15000, n_samples),
        'education_years': np.random.randint(8, 20, n_samples),
        'experience': np.random.randint(0, 40, n_samples),
        'category': np.random.choice(['A', 'B', 'C'], n_samples),
        'score': np.random.normal(75, 10, n_samples)
    }
    
    # Add some outliers and null values for demonstration
    data['income'][::100] = np.random.normal(150000, 20000, 10)  # High income outliers
    data['score'][::150] = np.nan  # Some missing scores
    
    return pd.DataFrame(data)


def main():
    """
    Demonstrate the DataAnalyzer class with sample data.
    
    Usage Examples:
    1. Basic usage with sample data:
       python data_analyzer.py
       
    2. Load from CSV file:
       analyzer = DataAnalyzer('your_data.csv')
       
    3. Perform specific analysis:
       analyzer.get_basic_info()
       analyzer.get_descriptive_statistics()
       analyzer.analyze_correlations()
    """
    print("Data Analyzer - Demonstration")
    print("=" * 40)
    
    try:
        # Create and load sample data
        print("Creating sample dataset...")
        sample_data = create_sample_data()
        
        # Initialize analyzer
        analyzer = DataAnalyzer(sample_data)
        
        # Perform comprehensive analysis
        print("\n1. BASIC INFORMATION")
        print("-" * 20)
        analyzer.get_basic_info()
        
        print("\n2. DESCRIPTIVE STATISTICS")
        print("-" * 25)
        analyzer.get_descriptive_statistics()
        
        print("\n3. OUTLIER DETECTION")
        print("-" * 20)
        analyzer.find_outliers('income', 'iqr')
        analyzer.find_outliers('score', 'zscore')
        
        print("\n4. CORRELATION ANALYSIS")
        print("-" * 23)
        analyzer.analyze_correlations()
        
        print("\n5. GROUP ANALYSIS")
        print("-" * 17)
        analyzer.group_analysis('category', 'income')
        
        print("\n6. DATA CLEANING")
        print("-" * 16)
        analyzer.clean_data(drop_duplicates=True, handle_nulls='fill_mean')
        
        print("\n7. EXPORT RESULTS")
        print("-" * 16)
        output_file = "analysis_results.csv"
        analyzer.export_results(output_file)
        
        print(f"\nAnalysis complete! Results saved to '{output_file}'")
        
    except Exception as e:
        print(f"Error in main execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()