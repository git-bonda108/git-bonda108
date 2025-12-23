"""Formatting tools to convert results into table format"""
import pandas as pd
from typing import Any, Dict, List, Union


def format_as_table(data: Any, title: str = "") -> pd.DataFrame:
    """
    Convert various data types to DataFrame format.
    
    Args:
        data: Data to convert (dict, list, string, etc.)
        title: Optional title for the table
        
    Returns:
        DataFrame representation
    """
    if isinstance(data, pd.DataFrame):
        return data
    
    if isinstance(data, dict):
        # Try to convert dict to DataFrame
        if all(isinstance(v, (list, tuple)) for v in data.values()):
            # Dict of lists
            max_len = max(len(v) for v in data.values())
            padded_data = {k: list(v) + [None] * (max_len - len(v)) for k, v in data.items()}
            return pd.DataFrame(padded_data)
        else:
            # Dict of scalars
            return pd.DataFrame([data])
    
    if isinstance(data, (list, tuple)):
        if len(data) > 0 and isinstance(data[0], dict):
            return pd.DataFrame(data)
        else:
            return pd.DataFrame({'Value': data})
    
    if isinstance(data, str):
        return pd.DataFrame({'Result': [data]})
    
    return pd.DataFrame({'Value': [str(data)]})


def create_summary_table(statistics: Dict[str, Any]) -> pd.DataFrame:
    """
    Create a formatted summary statistics table.
    
    Args:
        statistics: Dictionary of statistics
        
    Returns:
        Formatted DataFrame
    """
    rows = []
    for key, value in statistics.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                rows.append({
                    'Metric': f"{key} - {sub_key}",
                    'Value': sub_value
                })
        else:
            rows.append({
                'Metric': key,
                'Value': value
            })
    
    return pd.DataFrame(rows)


def create_comparison_table(data1: pd.DataFrame, data2: pd.DataFrame, 
                           label1: str = "Dataset 1", label2: str = "Dataset 2") -> pd.DataFrame:
    """
    Create a comparison table between two datasets.
    
    Args:
        data1: First dataframe
        data2: Second dataframe
        label1: Label for first dataset
        label2: Label for second dataset
        
    Returns:
        Comparison DataFrame
    """
    comparison = {
        'Metric': ['Rows', 'Columns', 'Memory (MB)'],
        label1: [
            len(data1),
            len(data1.columns),
            data1.memory_usage(deep=True).sum() / (1024 * 1024)
        ],
        label2: [
            len(data2),
            len(data2.columns),
            data2.memory_usage(deep=True).sum() / (1024 * 1024)
        ]
    }
    
    return pd.DataFrame(comparison)


def format_insights(insights: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Format insights into a structured table.
    
    Args:
        insights: List of insight dictionaries with keys: finding, value, significance
        
    Returns:
        Formatted insights DataFrame
    """
    if not insights:
        return pd.DataFrame({'Finding': ['No insights available'], 'Value': [''], 'Significance': ['']})
    
    formatted = []
    for insight in insights:
        formatted.append({
            'Finding': insight.get('finding', ''),
            'Value': insight.get('value', ''),
            'Significance': insight.get('significance', ''),
            'Category': insight.get('category', 'General')
        })
    
    return pd.DataFrame(formatted)


def format_correlation_table(correlation_matrix: pd.DataFrame) -> pd.DataFrame:
    """
    Format correlation matrix into a readable table format.
    
    Args:
        correlation_matrix: Correlation matrix DataFrame
        
    Returns:
        Formatted correlation table
    """
    if correlation_matrix.empty:
        return pd.DataFrame()
    
    # Convert matrix to long format
    corr_table = []
    for i, col1 in enumerate(correlation_matrix.columns):
        for col2 in correlation_matrix.columns[i+1:]:
            corr_value = correlation_matrix.loc[col1, col2]
            corr_table.append({
                'Feature_1': col1,
                'Feature_2': col2,
                'Correlation': round(corr_value, 4),
                'Strength': _correlation_strength_label(abs(corr_value))
            })
    
    return pd.DataFrame(corr_table).sort_values('Correlation', key=abs, ascending=False)


def _correlation_strength_label(corr_abs: float) -> str:
    """Get correlation strength label"""
    if corr_abs >= 0.9:
        return 'Very Strong'
    elif corr_abs >= 0.7:
        return 'Strong'
    elif corr_abs >= 0.5:
        return 'Moderate'
    elif corr_abs >= 0.3:
        return 'Weak'
    else:
        return 'Very Weak'


def format_statistics_table(stats_df: pd.DataFrame) -> pd.DataFrame:
    """
    Format statistics DataFrame for better readability.
    
    Args:
        stats_df: Statistics DataFrame
        
    Returns:
        Formatted DataFrame with rounded values
    """
    if stats_df.empty:
        return pd.DataFrame()
    
    formatted = stats_df.copy()
    
    # Round numeric columns
    for col in formatted.columns:
        if formatted[col].dtype in ['float64', 'float32']:
            formatted[col] = formatted[col].round(4)
    
    return formatted


def format_statistics_table(stats_df: pd.DataFrame) -> pd.DataFrame:
    """
    Format statistics DataFrame for better readability.
    
    Args:
        stats_df: Statistics DataFrame
        
    Returns:
        Formatted DataFrame with rounded values
    """
    if stats_df.empty:
        return pd.DataFrame()
    
    formatted = stats_df.copy()
    
    # Round numeric columns
    for col in formatted.columns:
        if formatted[col].dtype in ['float64', 'float32']:
            formatted[col] = formatted[col].round(4)
    
    return formatted

