"""Data manipulation and querying tools for the Analysis Agent"""
import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any, Union


def query_dataframe(query: str, dataframe: pd.DataFrame) -> str:
    """
    Query the dataframe using pandas operations.
    
    Args:
        query: A pandas query string or operation description
        dataframe: The dataframe to query
        
    Returns:
        String representation of the query results
    """
    try:
        if dataframe.empty:
            return "DataFrame is empty."
        
        # Handle common query patterns
        query_lower = query.lower()
        
        if "head" in query_lower or "first" in query_lower:
            n = 5
            if "10" in query:
                n = 10
            elif "20" in query or "twenty" in query_lower:
                n = 20
            elif "50" in query or "fifty" in query_lower:
                n = 50
            return f"First {n} rows:\n{dataframe.head(n).to_string()}"
        
        if "tail" in query_lower or "last" in query_lower:
            n = 5
            if "10" in query:
                n = 10
            return f"Last {n} rows:\n{dataframe.tail(n).to_string()}"
        
        if "shape" in query_lower or "size" in query_lower or "dimensions" in query_lower:
            return f"Dataframe shape: {dataframe.shape[0]} rows × {dataframe.shape[1]} columns"
        
        if "columns" in query_lower or "column names" in query_lower:
            return f"Column names: {list(dataframe.columns)}"
        
        if "info" in query_lower:
            buffer = []
            buffer.append(f"Dataframe Info:")
            buffer.append(f"Shape: {dataframe.shape}")
            buffer.append(f"Columns: {list(dataframe.columns)}")
            buffer.append(f"\nData types:\n{dataframe.dtypes}")
            buffer.append(f"\nMissing values:\n{dataframe.isnull().sum()}")
            buffer.append(f"\nMemory usage: {dataframe.memory_usage(deep=True).sum() / 1024:.2f} KB")
            return "\n".join(buffer)
        
        if "sample" in query_lower:
            n = 5
            if "10" in query:
                n = 10
            return f"Random sample ({n} rows):\n{dataframe.sample(min(n, len(dataframe))).to_string()}"
        
        # Default: return summary
        return f"Dataframe summary:\n{dataframe.describe().to_string()}\n\nFirst 5 rows:\n{dataframe.head().to_string()}"
    
    except Exception as e:
        return f"Error querying dataframe: {e}"


def filter_dataframe(column: str, condition: str, value: Any, dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Filter the dataframe based on column and condition.
    
    Args:
        column: Column name to filter on
        condition: Condition type ('greater', 'less', 'equal', 'contains', 'between')
        value: Value to compare against
        dataframe: The dataframe to filter
        
    Returns:
        Filtered dataframe
    """
    if dataframe.empty:
        return dataframe
    
    if column not in dataframe.columns:
        raise ValueError(f"Column '{column}' not found. Available columns: {list(dataframe.columns)}")
    
    try:
        if condition.lower() in ['greater', '>', 'gt', 'above']:
            filtered = dataframe[dataframe[column] > value]
        elif condition.lower() in ['less', '<', 'lt', 'below']:
            filtered = dataframe[dataframe[column] < value]
        elif condition.lower() in ['equal', '==', 'eq', 'equals']:
            filtered = dataframe[dataframe[column] == value]
        elif condition.lower() in ['contains', 'in', 'includes']:
            filtered = dataframe[dataframe[column].astype(str).str.contains(str(value), case=False, na=False)]
        elif condition.lower() in ['between', 'range']:
            if isinstance(value, (list, tuple)) and len(value) == 2:
                filtered = dataframe[(dataframe[column] >= value[0]) & (dataframe[column] <= value[1])]
            else:
                raise ValueError("Between condition requires a list/tuple of [min, max]")
        else:
            raise ValueError(f"Unknown condition: {condition}. Use 'greater', 'less', 'equal', 'contains', or 'between'")
        
        return filtered
    
    except Exception as e:
        raise ValueError(f"Error filtering dataframe: {e}")


def group_by_aggregate(dataframe: pd.DataFrame, group_by: str, agg_function: str, 
                      agg_column: Optional[str] = None) -> pd.DataFrame:
    """
    Group by a column and apply aggregation.
    
    Args:
        dataframe: The dataframe to group
        group_by: Column to group by
        agg_function: Aggregation function ('sum', 'mean', 'count', 'max', 'min', 'std')
        agg_column: Column to aggregate (if None, aggregates all numeric columns)
        
    Returns:
        Aggregated dataframe
    """
    if group_by not in dataframe.columns:
        raise ValueError(f"Column '{group_by}' not found.")
    
    try:
        grouped = dataframe.groupby(group_by)
        
        if agg_column and agg_column in dataframe.columns:
            if agg_function.lower() == 'sum':
                result = grouped[agg_column].sum().reset_index()
            elif agg_function.lower() == 'mean' or agg_function.lower() == 'average':
                result = grouped[agg_column].mean().reset_index()
            elif agg_function.lower() == 'count':
                result = grouped[agg_column].count().reset_index()
            elif agg_function.lower() == 'max':
                result = grouped[agg_column].max().reset_index()
            elif agg_function.lower() == 'min':
                result = grouped[agg_column].min().reset_index()
            elif agg_function.lower() == 'std' or agg_function.lower() == 'stddev':
                result = grouped[agg_column].std().reset_index()
            else:
                raise ValueError(f"Unknown aggregation function: {agg_function}")
        else:
            # Aggregate all numeric columns
            numeric_cols = dataframe.select_dtypes(include=[np.number]).columns
            if agg_function.lower() == 'sum':
                result = grouped[numeric_cols].sum().reset_index()
            elif agg_function.lower() == 'mean' or agg_function.lower() == 'average':
                result = grouped[numeric_cols].mean().reset_index()
            elif agg_function.lower() == 'count':
                result = grouped[numeric_cols].count().reset_index()
            else:
                result = grouped[numeric_cols].agg(agg_function).reset_index()
        
        return result
    
    except Exception as e:
        raise ValueError(f"Error in group by operation: {e}")


def detect_outliers(dataframe: pd.DataFrame, column: str, method: str = 'iqr') -> pd.DataFrame:
    """
    Detect outliers in a column.
    
    Args:
        dataframe: The dataframe to analyze
        column: Column to check for outliers
        method: Method to use ('iqr' or 'zscore')
        
    Returns:
        DataFrame with outliers
    """
    if column not in dataframe.columns:
        raise ValueError(f"Column '{column}' not found.")
    
    if dataframe[column].dtype not in [np.number]:
        raise ValueError(f"Column '{column}' must be numeric for outlier detection.")
    
    try:
        if method.lower() == 'iqr':
            Q1 = dataframe[column].quantile(0.25)
            Q3 = dataframe[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = dataframe[(dataframe[column] < lower_bound) | (dataframe[column] > upper_bound)]
        elif method.lower() == 'zscore':
            z_scores = np.abs((dataframe[column] - dataframe[column].mean()) / dataframe[column].std())
            outliers = dataframe[z_scores > 3]
        else:
            raise ValueError(f"Unknown method: {method}. Use 'iqr' or 'zscore'")
        
        return outliers
    
    except Exception as e:
        raise ValueError(f"Error detecting outliers: {e}")


def get_data_info(dataframe: pd.DataFrame) -> Dict[str, Any]:
    """
    Get comprehensive information about the dataframe.
    
    Args:
        dataframe: The dataframe to analyze
        
    Returns:
        Dictionary with data information
    """
    info = {
        'shape': dataframe.shape,
        'columns': list(dataframe.columns),
        'dtypes': dataframe.dtypes.to_dict(),
        'missing_values': dataframe.isnull().sum().to_dict(),
        'missing_percentage': (dataframe.isnull().sum() / len(dataframe) * 100).to_dict(),
        'memory_usage_mb': dataframe.memory_usage(deep=True).sum() / (1024 * 1024),
        'numeric_columns': list(dataframe.select_dtypes(include=[np.number]).columns),
        'categorical_columns': list(dataframe.select_dtypes(include=['object', 'category']).columns),
        'duplicate_rows': dataframe.duplicated().sum()
    }
    return info


def get_data_quality_summary(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Get comprehensive data quality summary including missing values, nulls, duplicates, etc.
    
    Args:
        dataframe: The dataframe to analyze
        
    Returns:
        DataFrame with data quality metrics
    """
    quality_data = []
    
    for col in dataframe.columns:
        null_count = dataframe[col].isnull().sum()
        null_percentage = (null_count / len(dataframe)) * 100
        non_null_count = dataframe[col].notna().sum()
        unique_count = dataframe[col].nunique()
        duplicate_count = dataframe[col].duplicated().sum()
        
        # Data type info
        dtype = str(dataframe[col].dtype)
        
        quality_data.append({
            'Column': col,
            'Data Type': dtype,
            'Total Rows': len(dataframe),
            'Non-Null Count': non_null_count,
            'Null Count': null_count,
            'Null Percentage': f"{null_percentage:.2f}%",
            'Unique Values': unique_count,
            'Duplicates': duplicate_count,
            'Completeness': f"{(1 - null_percentage/100)*100:.2f}%"
        })
    
    return pd.DataFrame(quality_data)


def execute_complex_query(dataframe: pd.DataFrame, query: str) -> pd.DataFrame:
    """Execute complex natural language or SQL-like query with ORDER BY, GROUP BY, WHERE, etc."""
    import re
    
    result = dataframe.copy()
    query_lower = query.lower()
    
    # Extract ORDER BY
    order_match = re.search(r'order by (\w+)|sort by (\w+)|sorted by (\w+)', query_lower)
    if order_match:
        col = order_match.group(1) or order_match.group(2) or order_match.group(3)
        if col in result.columns:
            ascending = 'desc' not in query_lower
            result = result.sort_values(by=col, ascending=ascending)
    
    # Extract LIMIT
    limit_match = re.search(r'limit\s+(\d+)|first\s+(\d+)|top\s+(\d+)', query_lower)
    if limit_match:
        limit_val = int(limit_match.group(1) or limit_match.group(2) or limit_match.group(3))
        result = result.head(limit_val)
    
    # Extract WHERE conditions (simplified)
    if 'where' in query_lower:
        # Try to extract column and value
        where_match = re.search(r'where\s+(\w+)\s*(>|<|>=|<=|==)\s*([\d.]+)', query_lower)
        if where_match:
            col = where_match.group(1)
            op = where_match.group(2)
            val = float(where_match.group(3))
            if col in result.columns:
                if op == '>':
                    result = result[result[col] > val]
                elif op == '<':
                    result = result[result[col] < val]
                elif op == '>=':
                    result = result[result[col] >= val]
                elif op == '<=':
                    result = result[result[col] <= val]
                elif op == '==':
                    result = result[result[col] == val]
    
    # Extract GROUP BY (simplified - would need aggregation separately)
    group_match = re.search(r'group by (\w+)', query_lower)
    if group_match:
        col = group_match.group(1)
        if col in result.columns:
            # Default to count
            result = result.groupby(col).size().reset_index(name='count')
    
    return result


def multi_condition_filter(dataframe: pd.DataFrame, 
                          conditions: List[Dict[str, Any]],
                          logic: str = 'AND') -> pd.DataFrame:
    """Apply multiple conditions with AND/OR logic."""
    if not conditions:
        return dataframe
    
    masks = []
    for condition in conditions:
        col = condition.get('column')
        operator = condition.get('operator', '==')
        value = condition.get('value')
        
        if col not in dataframe.columns:
            continue
        
        if operator == '>':
            masks.append(dataframe[col] > value)
        elif operator == '>=':
            masks.append(dataframe[col] >= value)
        elif operator == '<':
            masks.append(dataframe[col] < value)
        elif operator == '<=':
            masks.append(dataframe[col] <= value)
        elif operator == '==':
            masks.append(dataframe[col] == value)
        elif operator == '!=':
            masks.append(dataframe[col] != value)
        elif operator == 'contains':
            masks.append(dataframe[col].astype(str).str.contains(str(value), case=False, na=False))
    
    if not masks:
        return dataframe
    
    if logic.upper() == 'AND':
        combined_mask = masks[0]
        for mask in masks[1:]:
            combined_mask = combined_mask & mask
    else:  # OR
        combined_mask = masks[0]
        for mask in masks[1:]:
            combined_mask = combined_mask | mask
    
    return dataframe[combined_mask]


def advanced_group_by(dataframe: pd.DataFrame,
                     group_by: Union[str, List[str]],
                     aggregations: Dict[str, Union[str, List[str]]]) -> pd.DataFrame:
    """Advanced group by with multiple aggregations."""
    if isinstance(group_by, str):
        group_by = [group_by]
    
    for col in group_by:
        if col not in dataframe.columns:
            raise ValueError(f"Column '{col}' not found for GROUP BY")
    
    grouped = dataframe.groupby(group_by)
    
    if not aggregations:
        return grouped.size().reset_index(name='count')
    
    result = grouped.agg(aggregations)
    return result.reset_index()

