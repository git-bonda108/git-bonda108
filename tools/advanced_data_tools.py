"""Advanced data manipulation tools with SQL-like operations"""
import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any, Union
import re


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
        
        # For numeric columns, add range info
        if pd.api.types.is_numeric_dtype(dataframe[col]):
            min_val = dataframe[col].min()
            max_val = dataframe[col].mean()
            mean_val = dataframe[col].mean()
        else:
            min_val = "N/A"
            max_val = "N/A"
            mean_val = "N/A"
        
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


def execute_sql_like_query(dataframe: pd.DataFrame, 
                          select_columns: Optional[List[str]] = None,
                          where_conditions: Optional[List[Dict[str, Any]]] = None,
                          group_by: Optional[str] = None,
                          order_by: Optional[str] = None,
                          order_direction: str = 'asc',
                          limit: Optional[int] = None) -> pd.DataFrame:
    """
    Execute SQL-like query on dataframe.
    
    Args:
        dataframe: The dataframe to query
        select_columns: Columns to select (None = all columns)
        where_conditions: List of conditions like [{'column': 'age', 'operator': '>', 'value': 30}]
        group_by: Column to group by
        order_by: Column to order by
        order_direction: 'asc' or 'desc'
        limit: Limit number of rows
        
    Returns:
        Resulting dataframe
    """
    result = dataframe.copy()
    
    # WHERE clause
    if where_conditions:
        mask = pd.Series([True] * len(result))
        for condition in where_conditions:
            col = condition.get('column')
            operator = condition.get('operator', '==')
            value = condition.get('value')
            
            if col not in result.columns:
                raise ValueError(f"Column '{col}' not found")
            
            if operator == '>':
                mask = mask & (result[col] > value)
            elif operator == '>=':
                mask = mask & (result[col] >= value)
            elif operator == '<':
                mask = mask & (result[col] < value)
            elif operator == '<=':
                mask = mask & (result[col] <= value)
            elif operator == '==':
                mask = mask & (result[col] == value)
            elif operator == '!=':
                mask = mask & (result[col] != value)
            elif operator == 'in':
                mask = mask & (result[col].isin(value))
            elif operator == 'contains':
                mask = mask & (result[col].astype(str).str.contains(str(value), case=False, na=False))
            elif operator == 'between':
                if isinstance(value, (list, tuple)) and len(value) == 2:
                    mask = mask & (result[col] >= value[0]) & (result[col] <= value[1])
        
        result = result[mask]
    
    # GROUP BY
    if group_by:
        if group_by not in result.columns:
            raise ValueError(f"Column '{group_by}' not found for GROUP BY")
        # Note: Aggregation should be done separately
    
    # ORDER BY
    if order_by:
        if order_by not in result.columns:
            raise ValueError(f"Column '{order_by}' not found for ORDER BY")
        ascending = order_direction.lower() == 'asc'
        result = result.sort_values(by=order_by, ascending=ascending)
    
    # SELECT columns
    if select_columns:
        missing_cols = [col for col in select_columns if col not in result.columns]
        if missing_cols:
            raise ValueError(f"Columns not found: {missing_cols}")
        result = result[select_columns]
    
    # LIMIT
    if limit:
        result = result.head(limit)
    
    return result


def parse_natural_language_query(query: str, dataframe: pd.DataFrame) -> Dict[str, Any]:
    """
    Parse natural language query into structured operations.
    
    Args:
        query: Natural language query
        dataframe: The dataframe
        
    Returns:
        Dictionary with parsed operations
    """
    query_lower = query.lower()
    operations = {
        'select_columns': None,
        'where_conditions': [],
        'group_by': None,
        'order_by': None,
        'order_direction': 'asc',
        'limit': None,
        'aggregate': None
    }
    
    # Extract ORDER BY
    order_patterns = [
        r'order by (\w+)',
        r'sort by (\w+)',
        r'sorted by (\w+)',
        r'sort (\w+)',
    ]
    for pattern in order_patterns:
        match = re.search(pattern, query_lower)
        if match:
            col = match.group(1)
            if col in dataframe.columns:
                operations['order_by'] = col
                if 'desc' in query_lower or 'descending' in query_lower:
                    operations['order_direction'] = 'desc'
                break
    
    # Extract GROUP BY
    group_patterns = [
        r'group by (\w+)',
        r'grouped by (\w+)',
        r'group (\w+)',
    ]
    for pattern in group_patterns:
        match = re.search(pattern, query_lower)
        if match:
            col = match.group(1)
            if col in dataframe.columns:
                operations['group_by'] = col
                break
    
    # Extract WHERE conditions
    # Pattern: "where column > value", "where column is value", etc.
    where_patterns = [
        (r'where (\w+)\s*(>|>=|<|<=|==|!=)\s*([\d.]+)', lambda m: {'column': m.group(1), 'operator': m.group(2), 'value': float(m.group(3))}),
        (r'where (\w+)\s+is\s+([\w\s]+)', lambda m: {'column': m.group(1), 'operator': '==', 'value': m.group(2).strip()}),
        (r'where (\w+)\s+greater\s+than\s+([\d.]+)', lambda m: {'column': m.group(1), 'operator': '>', 'value': float(m.group(2))}),
        (r'where (\w+)\s+less\s+than\s+([\d.]+)', lambda m: {'column': m.group(1), 'operator': '<', 'value': float(m.group(2))}),
    ]
    
    for pattern, extractor in where_patterns:
        match = re.search(pattern, query_lower)
        if match:
            condition = extractor(match)
            if condition['column'] in dataframe.columns:
                operations['where_conditions'].append(condition)
    
    # Extract LIMIT
    limit_match = re.search(r'limit\s+(\d+)|first\s+(\d+)|top\s+(\d+)', query_lower)
    if limit_match:
        operations['limit'] = int(limit_match.group(1) or limit_match.group(2) or limit_match.group(3))
    
    # Extract aggregate functions
    agg_patterns = [
        (r'sum of (\w+)', 'sum'),
        (r'average of (\w+)|mean of (\w+)', 'mean'),
        (r'count of (\w+)', 'count'),
        (r'max of (\w+)', 'max'),
        (r'min of (\w+)', 'min'),
    ]
    
    return operations


def complex_query(dataframe: pd.DataFrame, query: str) -> pd.DataFrame:
    """
    Execute complex natural language or SQL-like query.
    
    Args:
        dataframe: The dataframe
        query: Natural language or SQL-like query
        
    Returns:
        Result dataframe
    """
    # Try to parse as natural language
    operations = parse_natural_language_query(query, dataframe)
    
    # Execute the operations
    result = execute_sql_like_query(
        dataframe,
        select_columns=operations.get('select_columns'),
        where_conditions=operations.get('where_conditions'),
        group_by=operations.get('group_by'),
        order_by=operations.get('order_by'),
        order_direction=operations.get('order_direction', 'asc'),
        limit=operations.get('limit')
    )
    
    # Handle GROUP BY with aggregation if needed
    if operations.get('group_by'):
        # Default to count if no aggregation specified
        result = result.groupby(operations['group_by']).size().reset_index(name='count')
    
    return result


def multi_condition_filter(dataframe: pd.DataFrame, 
                          conditions: List[Dict[str, Any]],
                          logic: str = 'AND') -> pd.DataFrame:
    """
    Apply multiple conditions with AND/OR logic.
    
    Args:
        dataframe: The dataframe
        conditions: List of condition dicts [{'column': 'age', 'operator': '>', 'value': 30}, ...]
        logic: 'AND' or 'OR'
        
    Returns:
        Filtered dataframe
    """
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
    """
    Advanced group by with multiple aggregations.
    
    Args:
        dataframe: The dataframe
        group_by: Column(s) to group by
        aggregations: Dict like {'column1': 'mean', 'column2': ['sum', 'count']}
        
    Returns:
        Aggregated dataframe
    """
    if isinstance(group_by, str):
        group_by = [group_by]
    
    # Verify all group_by columns exist
    for col in group_by:
        if col not in dataframe.columns:
            raise ValueError(f"Column '{col}' not found for GROUP BY")
    
    grouped = dataframe.groupby(group_by)
    
    # Build aggregation dict
    agg_dict = {}
    for col, funcs in aggregations.items():
        if col not in dataframe.columns:
            continue
        if isinstance(funcs, str):
            agg_dict[col] = funcs
        elif isinstance(funcs, list):
            agg_dict[col] = funcs
    
    if not agg_dict:
        # Default: count
        return grouped.size().reset_index(name='count')
    
    result = grouped.agg(agg_dict)
    result.columns = [f"{col}_{func}" if isinstance(func, list) and len(func) > 1 else col 
                      for col, func in zip(result.columns, [v if isinstance(v, list) else [v] for v in aggregations.values()])]
    
    return result.reset_index()



