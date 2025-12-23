"""Statistical analysis tools for the Statistical Agent"""
import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Any, Optional


def calculate_statistics(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate comprehensive descriptive statistics.
    
    Args:
        dataframe: The dataframe to analyze
        
    Returns:
        DataFrame with statistics for each numeric column
    """
    numeric_cols = dataframe.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) == 0:
        return pd.DataFrame()
    
    stats_dict = {
        'count': dataframe[numeric_cols].count(),
        'mean': dataframe[numeric_cols].mean(),
        'median': dataframe[numeric_cols].median(),
        'std': dataframe[numeric_cols].std(),
        'min': dataframe[numeric_cols].min(),
        'max': dataframe[numeric_cols].max(),
        'q25': dataframe[numeric_cols].quantile(0.25),
        'q75': dataframe[numeric_cols].quantile(0.75),
        'skewness': dataframe[numeric_cols].skew(),
        'kurtosis': dataframe[numeric_cols].kurtosis()
    }
    
    return pd.DataFrame(stats_dict).T


def analyze_correlations(dataframe: pd.DataFrame, method: str = 'pearson') -> pd.DataFrame:
    """
    Calculate correlation matrix between numeric features.
    
    Args:
        dataframe: The dataframe to analyze
        method: Correlation method ('pearson', 'spearman', 'kendall')
        
    Returns:
        Correlation matrix as DataFrame
    """
    numeric_cols = dataframe.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) < 2:
        return pd.DataFrame()
    
    return dataframe[numeric_cols].corr(method=method)


def feature_relationships(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze relationships between all feature pairs.
    
    Args:
        dataframe: The dataframe to analyze
        
    Returns:
        DataFrame with feature relationships
    """
    numeric_cols = list(dataframe.select_dtypes(include=[np.number]).columns)
    categorical_cols = list(dataframe.select_dtypes(include=['object', 'category']).columns)
    
    relationships = []
    
    # Numeric to Numeric relationships
    for i, col1 in enumerate(numeric_cols):
        for col2 in numeric_cols[i+1:]:
            corr = dataframe[col1].corr(dataframe[col2])
            relationships.append({
                'Feature_1': col1,
                'Feature_2': col2,
                'Type': 'Numeric-Numeric',
                'Correlation': corr,
                'Strength': _correlation_strength(abs(corr))
            })
    
    # Categorical to Numeric relationships (using ANOVA-like approach)
    for cat_col in categorical_cols:
        for num_col in numeric_cols:
            try:
                groups = [dataframe[dataframe[cat_col] == val][num_col].dropna() 
                         for val in dataframe[cat_col].unique()]
                if len(groups) > 1 and all(len(g) > 0 for g in groups):
                    f_stat, p_value = stats.f_oneway(*groups)
                    relationships.append({
                        'Feature_1': cat_col,
                        'Feature_2': num_col,
                        'Type': 'Categorical-Numeric',
                        'F_Statistic': f_stat,
                        'P_Value': p_value,
                        'Significant': 'Yes' if p_value < 0.05 else 'No'
                    })
            except:
                pass
    
    return pd.DataFrame(relationships)


def _correlation_strength(corr_abs: float) -> str:
    """Interpret correlation strength"""
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


def hypothesis_test(dataframe: pd.DataFrame, column: str, test_type: str = 'ttest', 
                    value: Optional[float] = None) -> Dict[str, Any]:
    """
    Perform hypothesis testing.
    
    Args:
        dataframe: The dataframe
        column: Column to test
        test_type: Type of test ('ttest', 'normality', 'independence')
        value: Value for one-sample t-test
        
    Returns:
        Dictionary with test results
    """
    if column not in dataframe.columns:
        raise ValueError(f"Column '{column}' not found.")
    
    if dataframe[column].dtype not in [np.number]:
        raise ValueError(f"Column '{column}' must be numeric.")
    
    data = dataframe[column].dropna()
    
    results = {}
    
    if test_type.lower() == 'ttest' or test_type.lower() == 't-test':
        if value is not None:
            t_stat, p_value = stats.ttest_1samp(data, value)
            results = {
                'test': 'One-Sample T-Test',
                'null_hypothesis': f'Mean = {value}',
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': 'Yes' if p_value < 0.05 else 'No',
                'mean': data.mean(),
                'std': data.std()
            }
        else:
            # Two-sample would require another column
            results = {'error': 'For two-sample t-test, provide two columns'}
    
    elif test_type.lower() == 'normality':
        stat, p_value = stats.normaltest(data)
        results = {
            'test': 'Normality Test (D\'Agostino)',
            'null_hypothesis': 'Data is normally distributed',
            'statistic': stat,
            'p_value': p_value,
            'normal': 'Yes' if p_value > 0.05 else 'No'
        }
    
    return results


def distribution_analysis(dataframe: pd.DataFrame, column: str) -> Dict[str, Any]:
    """
    Analyze the distribution of a column.
    
    Args:
        dataframe: The dataframe
        column: Column to analyze
        
    Returns:
        Dictionary with distribution information
    """
    if column not in dataframe.columns:
        raise ValueError(f"Column '{column}' not found.")
    
    data = dataframe[column].dropna()
    
    analysis = {
        'mean': data.mean(),
        'median': data.median(),
        'mode': data.mode().iloc[0] if len(data.mode()) > 0 else None,
        'std': data.std(),
        'variance': data.var(),
        'skewness': data.skew(),
        'kurtosis': data.kurtosis(),
        'range': data.max() - data.min(),
        'iqr': data.quantile(0.75) - data.quantile(0.25),
        'min': data.min(),
        'max': data.max(),
        'percentiles': {
            '25th': data.quantile(0.25),
            '50th': data.quantile(0.50),
            '75th': data.quantile(0.75),
            '90th': data.quantile(0.90),
            '95th': data.quantile(0.95),
            '99th': data.quantile(0.99)
        }
    }
    
    # Distribution type
    if abs(analysis['skewness']) < 0.5:
        analysis['distribution_type'] = 'Approximately Normal'
    elif analysis['skewness'] > 0.5:
        analysis['distribution_type'] = 'Right-Skewed (Positive)'
    else:
        analysis['distribution_type'] = 'Left-Skewed (Negative)'
    
    return analysis


def feature_importance(dataframe: pd.DataFrame, target_column: str) -> pd.DataFrame:
    """
    Calculate feature importance (correlation with target).
    
    Args:
        dataframe: The dataframe
        target_column: Target column to analyze relationships with
        
    Returns:
        DataFrame with feature importance
    """
    if target_column not in dataframe.columns:
        raise ValueError(f"Target column '{target_column}' not found.")
    
    numeric_cols = dataframe.select_dtypes(include=[np.number]).columns
    numeric_cols = [col for col in numeric_cols if col != target_column]
    
    if len(numeric_cols) == 0:
        return pd.DataFrame()
    
    importance = []
    for col in numeric_cols:
        corr = abs(dataframe[col].corr(dataframe[target_column]))
        importance.append({
            'Feature': col,
            'Correlation_with_Target': dataframe[col].corr(dataframe[target_column]),
            'Absolute_Correlation': corr,
            'Importance_Rank': 0  # Will be set after sorting
        })
    
    importance_df = pd.DataFrame(importance)
    importance_df = importance_df.sort_values('Absolute_Correlation', ascending=False)
    importance_df['Importance_Rank'] = range(1, len(importance_df) + 1)
    
    return importance_df

