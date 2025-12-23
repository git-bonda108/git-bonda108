"""Visualization tools for the Visualization Agent"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List
import streamlit as st


def create_histogram(dataframe: pd.DataFrame, column: str, bins: int = 30, 
                    title: Optional[str] = None) -> str:
    """Create a histogram"""
    if column not in dataframe.columns:
        return f"Column '{column}' not found."
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(dataframe[column].dropna(), bins=bins, edgecolor='black', alpha=0.7)
    ax.set_xlabel(column)
    ax.set_ylabel('Frequency')
    ax.set_title(title or f'Histogram of {column}')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    return f"Histogram created for {column}"


def create_scatter(dataframe: pd.DataFrame, x_column: str, y_column: str,
                   title: Optional[str] = None) -> str:
    """Create a scatter plot"""
    if x_column not in dataframe.columns or y_column not in dataframe.columns:
        return f"One or both columns not found."
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(dataframe[x_column], dataframe[y_column], alpha=0.6)
    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)
    ax.set_title(title or f'Scatter Plot: {x_column} vs {y_column}')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    return f"Scatter plot created: {x_column} vs {y_column}"


def create_correlation_heatmap(dataframe: pd.DataFrame, title: Optional[str] = None) -> str:
    """Create a correlation heatmap"""
    numeric_cols = dataframe.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) < 2:
        return "Need at least 2 numeric columns for correlation heatmap."
    
    corr = dataframe[numeric_cols].corr()
    
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr, annot=True, fmt='.2f', ax=ax, cmap='coolwarm', 
                center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    ax.set_title(title or 'Correlation Heatmap')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    return "Correlation heatmap created"


def create_bar_chart(dataframe: pd.DataFrame, column: str, top_n: int = 20,
                     title: Optional[str] = None) -> str:
    """Create a bar chart"""
    if column not in dataframe.columns:
        return f"Column '{column}' not found."
    
    value_counts = dataframe[column].value_counts().head(top_n)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(range(len(value_counts)), value_counts.values, color='steelblue', alpha=0.7)
    ax.set_xticks(range(len(value_counts)))
    ax.set_xticklabels(value_counts.index, rotation=45, ha='right')
    ax.set_xlabel(column)
    ax.set_ylabel('Count')
    ax.set_title(title or f'Bar Chart of {column}')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    return f"Bar chart created for {column}"


def create_box_plot(dataframe: pd.DataFrame, column: Optional[str] = None,
                    title: Optional[str] = None) -> str:
    """Create a box plot"""
    numeric_cols = dataframe.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) == 0:
        return "No numeric columns found."
    
    if column:
        if column not in numeric_cols:
            return f"Column '{column}' not found or not numeric."
        columns_to_plot = [column]
    else:
        columns_to_plot = list(numeric_cols[:5])  # Limit to 5 columns
    
    fig, ax = plt.subplots(figsize=(12, 6))
    dataframe[columns_to_plot].boxplot(ax=ax)
    ax.set_ylabel('Value')
    ax.set_title(title or 'Box Plot')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    return f"Box plot created for {', '.join(columns_to_plot)}"


def create_line_plot(dataframe: pd.DataFrame, x_column: str, y_column: str,
                    title: Optional[str] = None) -> str:
    """Create a line plot"""
    if x_column not in dataframe.columns or y_column not in dataframe.columns:
        return f"One or both columns not found."
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dataframe[x_column], dataframe[y_column], marker='o', linewidth=2, markersize=4)
    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)
    ax.set_title(title or f'Line Plot: {x_column} vs {y_column}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    return f"Line plot created: {x_column} vs {y_column}"


def create_pair_plot(dataframe: pd.DataFrame, columns: Optional[List[str]] = None) -> str:
    """Create a pair plot for multiple numeric columns"""
    numeric_cols = dataframe.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) < 2:
        return "Need at least 2 numeric columns for pair plot."
    
    if columns:
        plot_cols = [col for col in columns if col in numeric_cols]
    else:
        plot_cols = list(numeric_cols[:5])  # Limit to 5 columns
    
    if len(plot_cols) < 2:
        return "Not enough valid columns for pair plot."
    
    fig = sns.pairplot(dataframe[plot_cols], diag_kind='kde')
    fig.fig.suptitle('Pair Plot', y=1.02)
    st.pyplot(fig.fig)
    plt.close(fig.fig)
    return f"Pair plot created for {', '.join(plot_cols)}"



