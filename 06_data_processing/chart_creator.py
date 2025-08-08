#!/usr/bin/env python3
"""
Chart Creator Script - Data Visualization with Matplotlib

This script demonstrates various chart creation techniques using matplotlib
and seaborn for creating professional-looking data visualizations.

Author: Python Learning Series
Dependencies: matplotlib, seaborn, pandas, numpy
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')


class ChartCreator:
    """
    A comprehensive chart creation class that provides methods for creating
    various types of visualizations using matplotlib and seaborn.
    """
    
    def __init__(self, style: str = 'seaborn-v0_8', figsize: Tuple[int, int] = (10, 6)):
        """
        Initialize the ChartCreator.
        
        Args:
            style: Matplotlib style to use
            figsize: Default figure size (width, height)
        """
        self.style = style
        self.figsize = figsize
        self.setup_style()
    
    def setup_style(self):
        """Set up the plotting style and parameters."""
        try:
            plt.style.use(self.style)
        except OSError:
            # Fallback to default style if seaborn style not available
            plt.style.use('default')
            print(f"Style '{self.style}' not found. Using default style.")
        
        # Set seaborn palette
        sns.set_palette("husl")
        
        # Configure matplotlib parameters
        plt.rcParams.update({
            'figure.figsize': self.figsize,
            'font.size': 12,
            'axes.titlesize': 14,
            'axes.labelsize': 12,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 10,
            'figure.dpi': 100
        })
    
    def create_line_chart(self, data: pd.DataFrame, x_col: str, y_col: str,
                         title: str = None, save_path: str = None,
                         group_col: str = None) -> plt.Figure:
        """
        Create a line chart.
        
        Args:
            data: DataFrame containing the data
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            title: Chart title
            save_path: Path to save the chart
            group_col: Column for grouping lines
            
        Returns:
            plt.Figure: The created figure
        """
        try:
            fig, ax = plt.subplots(figsize=self.figsize)
            
            if group_col and group_col in data.columns:
                # Create multiple lines for each group
                for group in data[group_col].unique():
                    group_data = data[data[group_col] == group]
                    ax.plot(group_data[x_col], group_data[y_col], 
                           marker='o', label=str(group), linewidth=2)
                ax.legend()
            else:
                # Single line
                ax.plot(data[x_col], data[y_col], marker='o', 
                       linewidth=2, markersize=4)
            
            ax.set_xlabel(x_col.replace('_', ' ').title())
            ax.set_ylabel(y_col.replace('_', ' ').title())
            
            if title:
                ax.set_title(title, fontsize=16, fontweight='bold')
            else:
                ax.set_title(f'{y_col.replace("_", " ").title()} vs {x_col.replace("_", " ").title()}',
                           fontsize=16, fontweight='bold')
            
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            
            if save_path:
                self._save_chart(fig, save_path)
            
            return fig
            
        except Exception as e:
            print(f"Error creating line chart: {e}")
            return None
    
    def create_bar_chart(self, data: pd.DataFrame, x_col: str, y_col: str,
                        title: str = None, save_path: str = None,
                        horizontal: bool = False, color_col: str = None) -> plt.Figure:
        """
        Create a bar chart.
        
        Args:
            data: DataFrame containing the data
            x_col: Column name for x-axis (categories)
            y_col: Column name for y-axis (values)
            title: Chart title
            save_path: Path to save the chart
            horizontal: Whether to create horizontal bars
            color_col: Column for color coding bars
            
        Returns:
            plt.Figure: The created figure
        """
        try:
            fig, ax = plt.subplots(figsize=self.figsize)
            
            # Prepare data
            if color_col and color_col in data.columns:
                colors = plt.cm.viridis(np.linspace(0, 1, len(data)))
            else:
                colors = plt.cm.tab10(np.linspace(0, 1, len(data)))
            
            if horizontal:
                bars = ax.barh(data[x_col], data[y_col], color=colors)
                ax.set_xlabel(y_col.replace('_', ' ').title())
                ax.set_ylabel(x_col.replace('_', ' ').title())
            else:
                bars = ax.bar(data[x_col], data[y_col], color=colors)
                ax.set_xlabel(x_col.replace('_', ' ').title())
                ax.set_ylabel(y_col.replace('_', ' ').title())
                
                # Rotate x-axis labels if they're long
                if data[x_col].astype(str).str.len().max() > 8:
                    plt.xticks(rotation=45, ha='right')
            
            # Add value labels on bars
            for bar in bars:
                if horizontal:
                    width = bar.get_width()
                    ax.text(width, bar.get_y() + bar.get_height()/2,
                           f'{width:.1f}', ha='left', va='center')
                else:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2, height,
                           f'{height:.1f}', ha='center', va='bottom')
            
            if title:
                ax.set_title(title, fontsize=16, fontweight='bold')
            else:
                chart_type = "Horizontal" if horizontal else "Vertical"
                ax.set_title(f'{chart_type} Bar Chart: {y_col.replace("_", " ").title()}',
                           fontsize=16, fontweight='bold')
            
            ax.grid(True, alpha=0.3, axis='y' if not horizontal else 'x')
            plt.tight_layout()
            
            if save_path:
                self._save_chart(fig, save_path)
            
            return fig
            
        except Exception as e:
            print(f"Error creating bar chart: {e}")
            return None
    
    def create_scatter_plot(self, data: pd.DataFrame, x_col: str, y_col: str,
                           title: str = None, save_path: str = None,
                           size_col: str = None, color_col: str = None) -> plt.Figure:
        """
        Create a scatter plot.
        
        Args:
            data: DataFrame containing the data
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            title: Chart title
            save_path: Path to save the chart
            size_col: Column for point sizes
            color_col: Column for color coding
            
        Returns:
            plt.Figure: The created figure
        """
        try:
            fig, ax = plt.subplots(figsize=self.figsize)
            
            # Prepare size and color arrays
            sizes = data[size_col] * 10 if size_col and size_col in data.columns else 50
            colors = data[color_col] if color_col and color_col in data.columns else 'blue'
            
            scatter = ax.scatter(data[x_col], data[y_col], s=sizes, c=colors,
                               alpha=0.6, cmap='viridis')
            
            # Add colorbar if color column is used
            if color_col and color_col in data.columns:
                cbar = plt.colorbar(scatter)
                cbar.set_label(color_col.replace('_', ' ').title())
            
            # Add trendline
            z = np.polyfit(data[x_col], data[y_col], 1)
            p = np.poly1d(z)
            ax.plot(data[x_col], p(data[x_col]), "r--", alpha=0.8, linewidth=1)
            
            # Calculate correlation coefficient
            corr_coef = data[x_col].corr(data[y_col])
            ax.text(0.05, 0.95, f'r = {corr_coef:.3f}', transform=ax.transAxes,
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            ax.set_xlabel(x_col.replace('_', ' ').title())
            ax.set_ylabel(y_col.replace('_', ' ').title())
            
            if title:
                ax.set_title(title, fontsize=16, fontweight='bold')
            else:
                ax.set_title(f'Scatter Plot: {y_col.replace("_", " ").title()} vs {x_col.replace("_", " ").title()}',
                           fontsize=16, fontweight='bold')
            
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            
            if save_path:
                self._save_chart(fig, save_path)
            
            return fig
            
        except Exception as e:
            print(f"Error creating scatter plot: {e}")
            return None
    
    def create_histogram(self, data: pd.DataFrame, col: str, bins: int = 30,
                        title: str = None, save_path: str = None,
                        show_stats: bool = True) -> plt.Figure:
        """
        Create a histogram.
        
        Args:
            data: DataFrame containing the data
            col: Column name for the histogram
            bins: Number of bins
            title: Chart title
            save_path: Path to save the chart
            show_stats: Whether to show statistical information
            
        Returns:
            plt.Figure: The created figure
        """
        try:
            fig, ax = plt.subplots(figsize=self.figsize)
            
            # Create histogram
            n, bins, patches = ax.hist(data[col].dropna(), bins=bins, 
                                     alpha=0.7, color='skyblue', edgecolor='black')
            
            # Add statistical lines
            mean_val = data[col].mean()
            median_val = data[col].median()
            
            ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
            ax.axvline(median_val, color='orange', linestyle='--', linewidth=2, label=f'Median: {median_val:.2f}')
            
            if show_stats:
                # Add statistics text box
                stats_text = f"""
                Count: {data[col].count()}
                Mean: {mean_val:.2f}
                Median: {median_val:.2f}
                Std: {data[col].std():.2f}
                Min: {data[col].min():.2f}
                Max: {data[col].max():.2f}
                """.strip()
                
                ax.text(0.75, 0.95, stats_text, transform=ax.transAxes, 
                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                       verticalalignment='top', fontfamily='monospace')
            
            ax.set_xlabel(col.replace('_', ' ').title())
            ax.set_ylabel('Frequency')
            
            if title:
                ax.set_title(title, fontsize=16, fontweight='bold')
            else:
                ax.set_title(f'Distribution of {col.replace("_", " ").title()}',
                           fontsize=16, fontweight='bold')
            
            ax.legend()
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            
            if save_path:
                self._save_chart(fig, save_path)
            
            return fig
            
        except Exception as e:
            print(f"Error creating histogram: {e}")
            return None
    
    def create_pie_chart(self, data: pd.DataFrame, col: str, title: str = None,
                        save_path: str = None, max_categories: int = 10) -> plt.Figure:
        """
        Create a pie chart.
        
        Args:
            data: DataFrame containing the data
            col: Column name for categories
            title: Chart title
            save_path: Path to save the chart
            max_categories: Maximum number of categories to show
            
        Returns:
            plt.Figure: The created figure
        """
        try:
            fig, ax = plt.subplots(figsize=self.figsize)
            
            # Get value counts
            value_counts = data[col].value_counts()
            
            # Handle too many categories
            if len(value_counts) > max_categories:
                top_categories = value_counts.head(max_categories - 1)
                others_count = value_counts.iloc[max_categories - 1:].sum()
                top_categories['Others'] = others_count
                value_counts = top_categories
            
            # Create pie chart
            wedges, texts, autotexts = ax.pie(value_counts.values, 
                                            labels=value_counts.index,
                                            autopct='%1.1f%%',
                                            startangle=90,
                                            colors=plt.cm.Set3.colors)
            
            # Enhance text formatting
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
            
            if title:
                ax.set_title(title, fontsize=16, fontweight='bold')
            else:
                ax.set_title(f'Distribution of {col.replace("_", " ").title()}',
                           fontsize=16, fontweight='bold')
            
            # Equal aspect ratio ensures that pie is drawn as a circle
            ax.axis('equal')
            plt.tight_layout()
            
            if save_path:
                self._save_chart(fig, save_path)
            
            return fig
            
        except Exception as e:
            print(f"Error creating pie chart: {e}")
            return None
    
    def create_box_plot(self, data: pd.DataFrame, x_col: str = None, y_col: str = None,
                       title: str = None, save_path: str = None) -> plt.Figure:
        """
        Create a box plot.
        
        Args:
            data: DataFrame containing the data
            x_col: Column for grouping (optional)
            y_col: Column for values
            title: Chart title
            save_path: Path to save the chart
            
        Returns:
            plt.Figure: The created figure
        """
        try:
            fig, ax = plt.subplots(figsize=self.figsize)
            
            if x_col and x_col in data.columns:
                # Grouped box plot
                box_data = [data[data[x_col] == group][y_col].dropna() 
                           for group in data[x_col].unique()]
                labels = data[x_col].unique()
                
                bp = ax.boxplot(box_data, labels=labels, patch_artist=True)
                
                # Color the boxes
                colors = plt.cm.Set2(np.linspace(0, 1, len(bp['boxes'])))
                for patch, color in zip(bp['boxes'], colors):
                    patch.set_facecolor(color)
                
                ax.set_xlabel(x_col.replace('_', ' ').title())
                ax.set_ylabel(y_col.replace('_', ' ').title())
                
                # Rotate labels if necessary
                if max(len(str(label)) for label in labels) > 8:
                    plt.xticks(rotation=45, ha='right')
                
            else:
                # Single box plot
                bp = ax.boxplot(data[y_col].dropna(), patch_artist=True)
                bp['boxes'][0].set_facecolor('lightblue')
                ax.set_ylabel(y_col.replace('_', ' ').title())
            
            if title:
                ax.set_title(title, fontsize=16, fontweight='bold')
            else:
                ax.set_title(f'Box Plot: {y_col.replace("_", " ").title()}',
                           fontsize=16, fontweight='bold')
            
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            
            if save_path:
                self._save_chart(fig, save_path)
            
            return fig
            
        except Exception as e:
            print(f"Error creating box plot: {e}")
            return None
    
    def create_heatmap(self, data: pd.DataFrame, title: str = None,
                      save_path: str = None, annot: bool = True) -> plt.Figure:
        """
        Create a correlation heatmap.
        
        Args:
            data: DataFrame containing numeric data
            title: Chart title
            save_path: Path to save the chart
            annot: Whether to annotate cells with values
            
        Returns:
            plt.Figure: The created figure
        """
        try:
            # Select only numeric columns
            numeric_data = data.select_dtypes(include=[np.number])
            
            if numeric_data.empty:
                print("No numeric columns found for heatmap")
                return None
            
            # Calculate correlation matrix
            corr_matrix = numeric_data.corr()
            
            fig, ax = plt.subplots(figsize=(max(8, len(corr_matrix.columns)), 
                                           max(6, len(corr_matrix.columns))))
            
            # Create heatmap
            sns.heatmap(corr_matrix, annot=annot, cmap='coolwarm', center=0,
                       square=True, ax=ax, fmt='.2f' if annot else '')
            
            if title:
                ax.set_title(title, fontsize=16, fontweight='bold')
            else:
                ax.set_title('Correlation Heatmap', fontsize=16, fontweight='bold')
            
            plt.tight_layout()
            
            if save_path:
                self._save_chart(fig, save_path)
            
            return fig
            
        except Exception as e:
            print(f"Error creating heatmap: {e}")
            return None
    
    def create_multi_chart_dashboard(self, data: pd.DataFrame, 
                                   save_path: str = None) -> plt.Figure:
        """
        Create a dashboard with multiple charts.
        
        Args:
            data: DataFrame containing the data
            save_path: Path to save the dashboard
            
        Returns:
            plt.Figure: The created figure
        """
        try:
            # Create subplots
            fig = plt.figure(figsize=(16, 12))
            
            # Get numeric and categorical columns
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = data.select_dtypes(include=['object']).columns.tolist()
            
            if len(numeric_cols) < 2:
                print("Need at least 2 numeric columns for dashboard")
                return None
            
            # Chart 1: Histogram of first numeric column
            ax1 = plt.subplot(2, 3, 1)
            data[numeric_cols[0]].hist(bins=20, ax=ax1, alpha=0.7, color='skyblue')
            ax1.set_title(f'Distribution of {numeric_cols[0]}')
            ax1.grid(True, alpha=0.3)
            
            # Chart 2: Scatter plot of two numeric columns
            ax2 = plt.subplot(2, 3, 2)
            ax2.scatter(data[numeric_cols[0]], data[numeric_cols[1]], alpha=0.6)
            ax2.set_xlabel(numeric_cols[0])
            ax2.set_ylabel(numeric_cols[1])
            ax2.set_title(f'{numeric_cols[1]} vs {numeric_cols[0]}')
            ax2.grid(True, alpha=0.3)
            
            # Chart 3: Box plot
            ax3 = plt.subplot(2, 3, 3)
            data.boxplot(column=numeric_cols[0], ax=ax3)
            ax3.set_title(f'Box Plot: {numeric_cols[0]}')
            
            # Chart 4: Bar chart (if categorical column exists)
            ax4 = plt.subplot(2, 3, 4)
            if categorical_cols:
                value_counts = data[categorical_cols[0]].value_counts()
                ax4.bar(value_counts.index, value_counts.values)
                ax4.set_title(f'Count by {categorical_cols[0]}')
                plt.xticks(rotation=45, ha='right')
            else:
                ax4.plot(data.index, data[numeric_cols[0]])
                ax4.set_title(f'Line Plot: {numeric_cols[0]}')
            
            # Chart 5: Correlation heatmap
            ax5 = plt.subplot(2, 3, 5)
            corr_matrix = data[numeric_cols].corr()
            im = ax5.imshow(corr_matrix, cmap='coolwarm', aspect='auto')
            ax5.set_xticks(range(len(numeric_cols)))
            ax5.set_yticks(range(len(numeric_cols)))
            ax5.set_xticklabels(numeric_cols, rotation=45, ha='right')
            ax5.set_yticklabels(numeric_cols)
            ax5.set_title('Correlation Matrix')
            plt.colorbar(im, ax=ax5, shrink=0.8)
            
            # Chart 6: Summary statistics
            ax6 = plt.subplot(2, 3, 6)
            ax6.axis('off')
            stats_text = f"""
            Dataset Summary:
            
            Rows: {len(data):,}
            Columns: {len(data.columns)}
            Numeric Columns: {len(numeric_cols)}
            Categorical Columns: {len(categorical_cols)}
            
            Missing Values:
            {data.isnull().sum().to_string()}
            """
            ax6.text(0.1, 0.9, stats_text, transform=ax6.transAxes,
                    fontfamily='monospace', fontsize=10, verticalalignment='top')
            
            plt.suptitle('Data Analysis Dashboard', fontsize=18, fontweight='bold')
            plt.tight_layout()
            
            if save_path:
                self._save_chart(fig, save_path)
            
            return fig
            
        except Exception as e:
            print(f"Error creating dashboard: {e}")
            return None
    
    def _save_chart(self, fig: plt.Figure, save_path: str, dpi: int = 300):
        """
        Save a chart to file.
        
        Args:
            fig: Figure to save
            save_path: Path to save the file
            dpi: Resolution for saving
        """
        try:
            # Create directory if it doesn't exist
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Save with high quality
            fig.savefig(save_path, dpi=dpi, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            print(f"Chart saved to: {save_path}")
            
        except Exception as e:
            print(f"Error saving chart: {e}")


def create_sample_data() -> pd.DataFrame:
    """
    Create sample data for chart demonstrations.
    
    Returns:
        pd.DataFrame: Sample dataset
    """
    np.random.seed(42)
    n_samples = 500
    
    # Generate sample data
    data = {
        'date': pd.date_range('2023-01-01', periods=n_samples, freq='D'),
        'sales': np.random.normal(1000, 200, n_samples) + 
                np.sin(np.arange(n_samples) * 2 * np.pi / 365) * 100,
        'temperature': np.random.normal(20, 10, n_samples),
        'category': np.random.choice(['A', 'B', 'C', 'D'], n_samples, p=[0.3, 0.3, 0.2, 0.2]),
        'score': np.random.normal(75, 15, n_samples),
        'satisfaction': np.random.randint(1, 6, n_samples)
    }
    
    # Add some correlation
    data['revenue'] = data['sales'] * np.random.uniform(0.8, 1.2, n_samples)
    
    return pd.DataFrame(data)


def main():
    """
    Demonstrate the ChartCreator class with various chart types.
    
    Usage Examples:
    1. Basic usage:
       python chart_creator.py
       
    2. Create specific chart types:
       creator = ChartCreator()
       creator.create_line_chart(data, 'x', 'y')
       creator.create_bar_chart(data, 'category', 'value')
       
    3. Save charts:
       creator.create_scatter_plot(data, 'x', 'y', save_path='scatter.png')
    """
    print("Chart Creator - Demonstration")
    print("=" * 40)
    
    try:
        # Create sample data
        print("Creating sample dataset...")
        data = create_sample_data()
        
        # Initialize chart creator
        creator = ChartCreator(figsize=(12, 8))
        
        # Create output directory
        output_dir = Path("charts")
        output_dir.mkdir(exist_ok=True)
        
        print(f"\nCreating various chart types...")
        print(f"Charts will be saved to: {output_dir.absolute()}")
        
        # 1. Line Chart
        print("1. Creating line chart...")
        creator.create_line_chart(
            data.head(50), 'date', 'sales',
            title='Sales Trend Over Time',
            save_path=output_dir / 'line_chart.png'
        )
        
        # 2. Bar Chart
        print("2. Creating bar chart...")
        category_sales = data.groupby('category')['sales'].mean().reset_index()
        creator.create_bar_chart(
            category_sales, 'category', 'sales',
            title='Average Sales by Category',
            save_path=output_dir / 'bar_chart.png'
        )
        
        # 3. Scatter Plot
        print("3. Creating scatter plot...")
        creator.create_scatter_plot(
            data, 'temperature', 'sales',
            title='Sales vs Temperature',
            color_col='satisfaction',
            save_path=output_dir / 'scatter_plot.png'
        )
        
        # 4. Histogram
        print("4. Creating histogram...")
        creator.create_histogram(
            data, 'score',
            title='Score Distribution',
            save_path=output_dir / 'histogram.png'
        )
        
        # 5. Pie Chart
        print("5. Creating pie chart...")
        creator.create_pie_chart(
            data, 'category',
            title='Category Distribution',
            save_path=output_dir / 'pie_chart.png'
        )
        
        # 6. Box Plot
        print("6. Creating box plot...")
        creator.create_box_plot(
            data, 'category', 'sales',
            title='Sales Distribution by Category',
            save_path=output_dir / 'box_plot.png'
        )
        
        # 7. Heatmap
        print("7. Creating correlation heatmap...")
        creator.create_heatmap(
            data,
            title='Variable Correlations',
            save_path=output_dir / 'heatmap.png'
        )
        
        # 8. Dashboard
        print("8. Creating multi-chart dashboard...")
        creator.create_multi_chart_dashboard(
            data,
            save_path=output_dir / 'dashboard.png'
        )
        
        print(f"\nAll charts created successfully!")
        print(f"Check the '{output_dir}' directory for your visualizations.")
        
        # Display sample data info
        print(f"\nSample data overview:")
        print(f"Shape: {data.shape}")
        print(f"Columns: {list(data.columns)}")
        
        # Show the plots (comment out if running in non-interactive environment)
        plt.show()
        
    except Exception as e:
        print(f"Error in main execution: {e}")


if __name__ == "__main__":
    main()