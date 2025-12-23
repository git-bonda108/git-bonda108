"""
Multi-Agent Data Analysis System
Powered by OpenAI Agents SDK
"""
import os
import streamlit as st
import pandas as pd
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
import ssl
from typing import Optional, Dict, List, Union
import numpy as np

# Import our tools
from tools import data_tools, statistical_tools, visualization_tools, formatting_tools
import re
import io

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

# Load environment variables
load_dotenv()

# Initialize session state
if 'dataframe' not in st.session_state:
    st.session_state.dataframe = None
if 'agents' not in st.session_state:
    st.session_state.agents = {}


@st.cache_data
def load_combined_data(files):
    """Load and combine multiple CSV/Excel files"""
    combined_df = pd.DataFrame()
    for file in files:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    return combined_df


def parse_text_to_dataframe(text: str, dataframe: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Parse text results to extract tabular data and convert to DataFrame.
    Handles various formats including pipe-separated tables, correlation results, etc.
    """
    if not text or not isinstance(text, str):
        return None
    
    try:
        # Try to find pipe-separated tables (common in text output)
        # Pattern: lines with | separators
        lines = text.split('\n')
        table_lines = []
        in_table = False
        
        for line in lines:
            if '|' in line and line.strip().startswith('|'):
                table_lines.append(line)
                in_table = True
            elif in_table and (not line.strip() or '---' in line):
                if '---' in line:
                    continue  # Skip separator lines
                if not line.strip():
                    break  # End of table
            elif in_table:
                break
        
        if table_lines:
            # Parse pipe-separated table
            try:
                # Clean up the lines
                cleaned_lines = []
                for line in table_lines:
                    # Remove leading/trailing pipes and split
                    parts = [p.strip() for p in line.strip().strip('|').split('|')]
                    if parts and any(p for p in parts):  # Skip empty lines
                        cleaned_lines.append(parts)
                
                if cleaned_lines and len(cleaned_lines) > 1:
                    # First line is header
                    headers = cleaned_lines[0]
                    data_rows = cleaned_lines[1:]
                    
                    # Create DataFrame
                    if headers and data_rows:
                        # Filter out empty rows
                        data_rows = [row for row in data_rows if any(cell for cell in row)]
                        if data_rows:
                            # Pad rows to match header length
                            max_cols = len(headers)
                            padded_rows = [row + [''] * (max_cols - len(row)) for row in data_rows]
                            df = pd.DataFrame(padded_rows, columns=headers[:max_cols])
                            # Remove completely empty columns
                            df = df.loc[:, (df != '').any(axis=0)]
                            if not df.empty:
                                return df
            except Exception:
                pass
        
        # Try to extract correlation results
        if 'correlation' in text.lower() or 'pearson' in text.lower():
            # Look for correlation coefficient patterns
            corr_pattern = r'(\w+)\s+and\s+(\w+)[:\s]+([-]?\d+\.?\d*)'
            matches = re.findall(corr_pattern, text, re.IGNORECASE)
            if matches:
                rows = []
                for match in matches:
                    rows.append({
                        'Feature 1': match[0],
                        'Feature 2': match[1],
                        'Correlation': float(match[2])
                    })
                if rows:
                    return pd.DataFrame(rows)
        
        # Try to find DataFrame-like structures in the text
        # Look for patterns like "Query Results (N rows):" followed by data
        if 'query results' in text.lower() or 'rows' in text.lower():
            # Try to extract data after "Query Results" or similar
            parts = re.split(r'query results.*?rows?[:\s]*', text, flags=re.IGNORECASE)
            if len(parts) > 1:
                data_part = parts[1].strip()
                # Try to parse as CSV-like data
                try:
                    df = pd.read_csv(io.StringIO(data_part), sep=r'\s+', engine='python')
                    if not df.empty:
                        return df
                except:
                    pass
        
        # Try to parse as CSV if it looks like CSV data
        if ',' in text and '\n' in text:
            lines = text.split('\n')
            # Check if it looks like CSV (at least 2 lines, consistent commas)
            if len(lines) >= 2:
                first_line_commas = lines[0].count(',')
                if first_line_commas > 0:
                    try:
                        df = pd.read_csv(io.StringIO(text))
                        if not df.empty and len(df.columns) > 1:
                            return df
                    except:
                        pass
        
        return None
    except Exception:
        return None


def extract_dataframe_from_result(result_text: str, dataframe: pd.DataFrame, query: str = "") -> Optional[pd.DataFrame]:
    """
    Try multiple methods to extract a DataFrame from result text.
    """
    # First try parsing text
    df = parse_text_to_dataframe(result_text, dataframe)
    if df is not None and not df.empty:
        return df
    
    # Try to extract using formatting tools
    try:
        df = formatting_tools.format_as_table(result_text)
        if df is not None and not df.empty:
            return df
    except:
        pass
    
    # For query results, try to execute the query directly if it's a simple query
    query_lower = query.lower()
    if any(word in query_lower for word in ['order by', 'sort', 'filter', 'group by', 'top', 'first', 'limit']):
        try:
            # Try to execute the query using data_tools
            if 'order by' in query_lower or 'sort' in query_lower:
                # Extract column name
                match = re.search(r'(?:order by|sort by)\s+(\w+)', query_lower)
                if match:
                    col = match.group(1)
                    # Check if column exists
                    if col in dataframe.columns:
                        direction = 'desc' if 'desc' in query_lower else 'asc'
                        result_df = dataframe.sort_values(by=col, ascending=(direction == 'asc'))
                        # Check for limit
                        limit_match = re.search(r'limit\s+(\d+)', query_lower)
                        if limit_match:
                            limit = int(limit_match.group(1))
                            result_df = result_df.head(limit)
                        return result_df
        except:
            pass
    
    return None


def create_agents(dataframe: pd.DataFrame, model_name: Optional[str] = None):
    """
    Create all specialized agents with their tools.
    
    Args:
        dataframe: The dataframe to analyze
        model_name: Optional model name (defaults to OpenAI, can be 'gpt-4o', 'gpt-4o-mini', etc.)
    """
    
    # Analysis Agent - Data exploration and querying with SQL-like operations
    @function_tool
    def query_data(query: str) -> str:
        """Query the dataframe using natural language. Supports SQL-like operations: ORDER BY, GROUP BY, WHERE, LIMIT."""
        try:
            # Try complex query first
            result = data_tools.execute_complex_query(dataframe, query)
            if not result.empty:
                return f"Query Results ({len(result)} rows):\n{result.to_string()}"
            # Fallback to simple query
            return data_tools.query_dataframe(query, dataframe)
        except Exception as e:
            return f"Error: {str(e)}. Available columns: {list(dataframe.columns)}"
    
    @function_tool
    def filter_data(column: str, condition: str, value: Union[str, float, int]) -> str:
        """Filter data. Conditions: 'greater', 'less', 'equal', 'contains', 'between'."""
        try:
            filtered = data_tools.filter_dataframe(column, condition, value, dataframe)
            return f"Filtered {len(filtered)} rows:\n{filtered.to_string()}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @function_tool
    def multi_filter(conditions: str, logic: str = 'AND') -> str:
        """Apply multiple filter conditions. Conditions format: 'column1>30,column2==value'. Logic: 'AND' or 'OR'."""
        try:
            # Parse conditions string
            cond_list = []
            for cond_str in conditions.split(','):
                parts = cond_str.strip().split('>')
                if len(parts) == 2:
                    cond_list.append({'column': parts[0].strip(), 'operator': '>', 'value': float(parts[1].strip())})
                elif '<' in cond_str:
                    parts = cond_str.split('<')
                    cond_list.append({'column': parts[0].strip(), 'operator': '<', 'value': float(parts[1].strip())})
                elif '==' in cond_str:
                    parts = cond_str.split('==')
                    val = parts[1].strip()
                    try:
                        val = float(val)
                    except:
                        pass
                    cond_list.append({'column': parts[0].strip(), 'operator': '==', 'value': val})
            
            if cond_list:
                filtered = data_tools.multi_condition_filter(dataframe, cond_list, logic)
                return f"Filtered {len(filtered)} rows:\n{filtered.to_string()}"
            return "No valid conditions provided"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @function_tool
    def group_by_aggregate(group_by: str, agg_function: str, agg_column: Optional[str] = None) -> str:
        """Group by a column and aggregate. Functions: 'sum', 'mean', 'count', 'max', 'min', 'std'."""
        try:
            result = data_tools.group_by_aggregate(dataframe, group_by, agg_function, agg_column)
            return result.to_string()
        except Exception as e:
            return f"Error: {str(e)}"
    
    @function_tool
    def advanced_group_by(group_by: str, aggregations: str) -> str:
        """Advanced group by with multiple aggregations. Format: 'column1:mean,column2:sum'."""
        try:
            agg_dict = {}
            for agg_str in aggregations.split(','):
                if ':' in agg_str:
                    col, func = agg_str.split(':')
                    agg_dict[col.strip()] = func.strip()
            
            result = data_tools.advanced_group_by(dataframe, group_by, agg_dict)
            return result.to_string()
        except Exception as e:
            return f"Error: {str(e)}"
    
    @function_tool
    def order_by(column: str, direction: str = 'asc') -> str:
        """Sort data by a column. Direction: 'asc' or 'desc'."""
        try:
            if column not in dataframe.columns:
                return f"Column '{column}' not found. Available: {list(dataframe.columns)}"
            ascending = direction.lower() == 'asc'
            sorted_df = dataframe.sort_values(by=column, ascending=ascending)
            return f"Sorted by {column} ({direction}):\n{sorted_df.head(50).to_string()}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @function_tool
    def get_data_info() -> str:
        """Get comprehensive information about the dataset."""
        info = data_tools.get_data_info(dataframe)
        return f"""Dataset Information:
- Shape: {info['shape']}
- Columns: {info['columns']}
- Numeric columns: {info['numeric_columns']}
- Categorical columns: {info['categorical_columns']}
- Missing values: {sum(info['missing_values'].values())}
- Duplicate rows: {info['duplicate_rows']}
- Memory usage: {info['memory_usage_mb']:.2f} MB"""
    
    @function_tool
    def get_data_quality() -> str:
        """Get comprehensive data quality summary including missing values, nulls, duplicates, completeness."""
        try:
            quality_df = data_tools.get_data_quality_summary(dataframe)
            return f"Data Quality Summary:\n{quality_df.to_string()}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @function_tool
    def detect_outliers(column: str, method: str = 'iqr') -> str:
        """Detect outliers in a column. Methods: 'iqr' or 'zscore'."""
        try:
            outliers = data_tools.detect_outliers(dataframe, column, method)
            return f"Found {len(outliers)} outliers:\n{outliers.to_string()}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @function_tool
    def execute_sql_query(query_description: str) -> str:
        """Execute SQL-like queries. Supports: SELECT, WHERE, GROUP BY, ORDER BY, LIMIT.
        Example: 'SELECT age, salary WHERE age > 30 ORDER BY salary DESC LIMIT 10'"""
        try:
            result = data_tools.execute_complex_query(dataframe, query_description)
            return f"Query Results ({len(result)} rows):\n{result.to_string()}"
        except Exception as e:
            return f"Error: {str(e)}. Available columns: {list(dataframe.columns)}"
    
    analysis_agent = Agent(
        name="Analysis Agent",
        instructions=f"""You are an expert data analyst with comprehensive SQL and pandas knowledge.
You have access to a dataframe with columns: {list(dataframe.columns)}.

Your capabilities:
- Execute complex queries with ORDER BY, GROUP BY, WHERE, LIMIT
- Filter data with single or multiple conditions (AND/OR logic)
- Group and aggregate data with multiple functions
- Sort data by any column (ascending/descending)
- Detect outliers and data quality issues
- Handle natural language queries and convert them to operations

SQL-like operations supported:
- ORDER BY column [ASC/DESC]
- GROUP BY column [WITH aggregations]
- WHERE conditions (>, <, >=, <=, ==, !=, contains, between)
- LIMIT/TOP/FIRST N rows
- Multiple WHERE conditions with AND/OR logic

When users ask for queries like:
- "Show top 10 rows ordered by salary"
- "Group by department and calculate average salary"
- "Filter where age > 30 and salary > 50000"
- "Order by age descending, limit 20"

Use the appropriate tools to execute these operations. Always provide clear, structured results.""",
        tools=[query_data, filter_data, multi_filter, group_by_aggregate, advanced_group_by, 
               order_by, get_data_info, get_data_quality, detect_outliers, execute_sql_query]
    )
    
    # Statistical Agent - Advanced statistics and feature relationships
    @function_tool
    def calculate_statistics() -> str:
        """Calculate comprehensive descriptive statistics for all numeric columns."""
        stats_df = statistical_tools.calculate_statistics(dataframe)
        if stats_df.empty:
            return "No numeric columns found for statistical analysis."
        return f"Statistical Summary:\n{stats_df.to_string()}"
    
    @function_tool
    def analyze_correlations(method: str = 'pearson') -> str:
        """Analyze correlations between numeric features. Methods: 'pearson', 'spearman', 'kendall'."""
        corr_df = statistical_tools.analyze_correlations(dataframe, method)
        if corr_df.empty:
            return "Need at least 2 numeric columns for correlation analysis."
        return f"Correlation Matrix ({method}):\n{corr_df.to_string()}"
    
    @function_tool
    def feature_relationships() -> str:
        """Analyze relationships between all feature pairs, including correlations and dependencies."""
        relationships_df = statistical_tools.feature_relationships(dataframe)
        if relationships_df.empty:
            return "No relationships found. Need numeric or categorical columns."
        return f"Feature Relationships:\n{relationships_df.to_string()}"
    
    @function_tool
    def hypothesis_test(column: str, test_type: str = 'ttest', value: Optional[float] = None) -> str:
        """Perform hypothesis testing. Test types: 'ttest', 'normality'."""
        try:
            result = statistical_tools.hypothesis_test(dataframe, column, test_type, value)
            return f"Hypothesis Test Results:\n{result}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @function_tool
    def distribution_analysis(column: str) -> str:
        """Analyze the distribution of a column including skewness, kurtosis, percentiles."""
        try:
            analysis = statistical_tools.distribution_analysis(dataframe, column)
            result = f"""Distribution Analysis for {column}:
- Mean: {analysis['mean']:.4f}
- Median: {analysis['median']:.4f}
- Std: {analysis['std']:.4f}
- Skewness: {analysis['skewness']:.4f}
- Kurtosis: {analysis['kurtosis']:.4f}
- Distribution Type: {analysis['distribution_type']}
- IQR: {analysis['iqr']:.4f}
- Range: {analysis['range']:.4f}"""
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    @function_tool
    def feature_importance(target_column: str) -> str:
        """Calculate feature importance based on correlation with target column."""
        try:
            importance_df = statistical_tools.feature_importance(dataframe, target_column)
            if importance_df.empty:
                return "No features found for importance analysis."
            return f"Feature Importance (correlation with {target_column}):\n{importance_df.to_string()}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    statistical_agent = Agent(
        name="Statistical Agent",
        instructions=f"""You are a statistical analysis expert specializing in advanced statistics and feature relationships.
You have access to a dataframe with columns: {list(dataframe.columns)}.

Your capabilities:
- Calculate comprehensive statistics
- Analyze correlations between features
- Identify feature relationships
- Perform hypothesis testing
- Analyze distributions
- Calculate feature importance

Always provide statistical insights and explain what the results mean. Focus on feature relationships and dependencies.""",
        tools=[calculate_statistics, analyze_correlations, feature_relationships, 
               hypothesis_test, distribution_analysis, feature_importance]
    )
    
    # Visualization Agent - Create charts and visualizations
    @function_tool
    def create_histogram(column: str, bins: int = 30) -> str:
        """Create a histogram to show distribution of a column."""
        return visualization_tools.create_histogram(dataframe, column, bins)
    
    @function_tool
    def create_scatter(x_column: str, y_column: str) -> str:
        """Create a scatter plot to show relationship between two columns."""
        return visualization_tools.create_scatter(dataframe, x_column, y_column)
    
    @function_tool
    def create_correlation_heatmap() -> str:
        """Create a correlation heatmap showing relationships between all numeric features."""
        return visualization_tools.create_correlation_heatmap(dataframe)
    
    @function_tool
    def create_bar_chart(column: str, top_n: int = 20) -> str:
        """Create a bar chart for a categorical column."""
        return visualization_tools.create_bar_chart(dataframe, column, top_n)
    
    @function_tool
    def create_box_plot(column: Optional[str] = None) -> str:
        """Create a box plot to show distribution and outliers."""
        return visualization_tools.create_box_plot(dataframe, column)
    
    @function_tool
    def create_line_plot(x_column: str, y_column: str) -> str:
        """Create a line plot for time series or sequential data."""
        return visualization_tools.create_line_plot(dataframe, x_column, y_column)
    
    @function_tool
    def create_pair_plot(columns: Optional[List[str]] = None) -> str:
        """Create a pair plot showing relationships between multiple numeric columns."""
        return visualization_tools.create_pair_plot(dataframe, columns)
    
    visualization_agent = Agent(
        name="Visualization Agent",
        instructions=f"""You are a data visualization expert specializing in creating insightful charts and graphs.
You have access to a dataframe with columns: {list(dataframe.columns)}.

Your capabilities:
- Create histograms for distributions
- Create scatter plots for relationships
- Create correlation heatmaps
- Create bar charts for categorical data
- Create box plots for distributions
- Create line plots for trends
- Create pair plots for multiple variables

Always choose the most appropriate visualization type for the data and question. Make charts informative and visually appealing.""",
        tools=[create_histogram, create_scatter, create_correlation_heatmap, 
               create_bar_chart, create_box_plot, create_line_plot, create_pair_plot]
    )
    
    # Formatting Agent - Structure results into tables
    @function_tool
    def format_as_table(data: str, title: str = "") -> str:
        """Convert any data into a formatted table (DataFrame)."""
        table_df = formatting_tools.format_as_table(data, title)
        return f"Formatted Table:\n{table_df.to_string()}"
    
    @function_tool
    def create_summary_table() -> str:
        """Create a formatted summary statistics table from the current dataframe."""
        stats_df = statistical_tools.calculate_statistics(dataframe)
        if stats_df.empty:
            return "No statistics available to format."
        return f"Summary Statistics Table:\n{stats_df.to_string()}"
    
    @function_tool
    def format_correlation_table() -> str:
        """Format correlation matrix into a readable table format."""
        corr_matrix = statistical_tools.analyze_correlations(dataframe)
        if corr_matrix.empty:
            return "No correlations to format."
        table_df = formatting_tools.format_correlation_table(corr_matrix)
        return f"Correlation Table:\n{table_df.to_string()}"
    
    @function_tool
    def format_insights() -> str:
        """Format insights into a structured table. Analyzes the dataframe and creates an insights table."""
        # Get feature relationships as insights
        relationships_df = statistical_tools.feature_relationships(dataframe)
        if relationships_df.empty:
            return "No insights available to format."
        return f"Insights Table:\n{relationships_df.to_string()}"
    
    formatting_agent = Agent(
        name="Formatting Agent",
        instructions=f"""You are a formatting expert specializing in structuring data and insights into readable table formats.
You have access to a dataframe with columns: {list(dataframe.columns)}.

Your capabilities:
- Convert any data to table format
- Create summary tables
- Format correlation tables
- Structure insights into tables

Always format results as clear, readable tables. Use proper column headers and organize data logically.""",
        tools=[format_as_table, create_summary_table, format_correlation_table, format_insights]
    )
    
    # Orchestrator Agent - Routes queries to appropriate agents
    orchestrator_agent = Agent(
        name="Orchestrator Agent",
        instructions=f"""You are an orchestrator that routes user queries to the appropriate specialized agents.

Available agents:
1. Analysis Agent - For data exploration, querying, filtering, grouping
2. Statistical Agent - For statistics, correlations, feature relationships, hypothesis testing
3. Visualization Agent - For creating charts, graphs, and visualizations
4. Formatting Agent - For formatting results into tables

Based on the user's query, determine which agent(s) should handle it:
- Data queries, filtering, grouping → Analysis Agent
- Statistics, correlations, relationships → Statistical Agent
- Charts, plots, visualizations → Visualization Agent
- Table formatting, structured output → Formatting Agent

For complex queries, you may need to coordinate multiple agents. Always ensure results are properly formatted in tables when possible.

The dataframe has columns: {list(dataframe.columns)}""",
        tools=[]  # Orchestrator uses handoffs instead of tools
    )
    
    return {
        'analysis': analysis_agent,
        'statistical': statistical_agent,
        'visualization': visualization_agent,
        'formatting': formatting_agent,
        'orchestrator': orchestrator_agent
    }


def route_query(query: str, agents: Dict[str, Agent], dataframe: pd.DataFrame) -> tuple:
    """
    Route query to appropriate agent(s) and return results.
    Returns: (agent_name, result_text, result_table)
    """
    query_lower = query.lower()
    
    # Determine which agent to use - prioritize SQL-like operations for Analysis Agent
    if any(word in query_lower for word in ['order by', 'sort by', 'group by', 'where', 'limit', 
                                             'select', 'filter', 'top', 'first']):
        agent_name = 'analysis'
        agent = agents['analysis']
    elif any(word in query_lower for word in ['plot', 'chart', 'graph', 'visualize', 'histogram', 
                                            'scatter', 'bar', 'heatmap', 'box plot', 'line plot']):
        agent_name = 'visualization'
        agent = agents['visualization']
    elif any(word in query_lower for word in ['statistic', 'correlation', 'relationship', 
                                               'feature', 'hypothesis', 'distribution', 'importance']):
        agent_name = 'statistical'
        agent = agents['statistical']
    elif any(word in query_lower for word in ['format', 'table', 'structure', 'organize']):
        agent_name = 'formatting'
        agent = agents['formatting']
    elif any(word in query_lower for word in ['query', 'aggregate', 'explore', 'info', 'outlier']):
        agent_name = 'analysis'
        agent = agents['analysis']
    else:
        # Default to analysis agent for general queries
        agent_name = 'analysis'
        agent = agents['analysis']
    
    try:
        result = Runner.run_sync(agent, query)
        result_text = result.final_output
        
        # Try to extract table from result - ALWAYS try to extract tabular data
        result_table = None
        
        # First, try the enhanced extraction function
        result_table = extract_dataframe_from_result(result_text, dataframe, query)
        
        # If that didn't work, try formatting tools
        if result_table is None or result_table.empty:
            try:
                result_table = formatting_tools.format_as_table(result_text)
            except:
                pass
        
        # For statistical/correlation queries, try to get actual data
        if (result_table is None or result_table.empty) and agent_name == 'statistical':
            if 'correlation' in query_lower:
                try:
                    numeric_cols = dataframe.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) >= 2:
                        corr_df = statistical_tools.analyze_correlations(dataframe)
                        if not corr_df.empty:
                            result_table = corr_df
                except:
                    pass
            elif 'statistic' in query_lower or 'summary' in query_lower:
                try:
                    stats_df = statistical_tools.calculate_statistics(dataframe)
                    if not stats_df.empty:
                        result_table = stats_df
                except:
                    pass
            elif 'relationship' in query_lower or 'feature' in query_lower:
                try:
                    rel_df = statistical_tools.feature_relationships(dataframe)
                    if not rel_df.empty:
                        result_table = rel_df
                except:
                    pass
        
        return agent_name, result_text, result_table
    except Exception as e:
        return agent_name, f"Error: {str(e)}", None


def main():
    st.set_page_config(
        page_title="Multi-Agent Data Analyzer", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 10px 20px;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-header">🤖 Multi-Agent Data Analysis System</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("❌ **OPENAI_API_KEY not set!**")
        st.info("""
        Please set your OpenAI API key:
        1. Create a `.env` file in this directory
        2. Add: `OPENAI_API_KEY=your-key-here`
        3. Or set environment variable: `export OPENAI_API_KEY=your-key-here`
        """)
        return
    
    # Sidebar - File upload
    with st.sidebar:
        st.header("📁 Data Upload")
        uploaded_files = st.file_uploader(
            "Upload CSV or Excel files", 
            type=["csv", "xlsx"],
            accept_multiple_files=True,
            help="Upload one or more data files to analyze"
        )
        
        st.markdown("---")
        st.header("ℹ️ About")
        st.markdown("""
        **Powered by OpenAI Agents SDK**
        
        This system uses specialized AI agents:
        - 📊 **Statistical Agent** - Advanced statistics
        - 🔍 **Analysis Agent** - Data exploration
        - 📈 **Visualization Agent** - Charts & graphs
        - 🔗 **Feature Relationships** - Correlations
        """)
    
    # Check if we have data (either from upload or session state)
    if uploaded_files:
        with st.spinner("Loading data..."):
            combined_data = load_combined_data(uploaded_files)
            st.session_state.dataframe = combined_data
            st.session_state.data_loaded = True
        
        # Create agents if not already created or if data changed
        if 'agents' not in st.session_state or not st.session_state.agents:
            with st.spinner("Initializing specialized agents..."):
                st.session_state.agents = create_agents(combined_data)
    
    # Use session state data if available - THIS ENSURES TABS ALWAYS SHOW WHEN DATA EXISTS
    if 'dataframe' in st.session_state and st.session_state.dataframe is not None and not st.session_state.dataframe.empty:
        combined_data = st.session_state.dataframe
        
        # Data Overview Section (always visible) - wrapped in try-except to ensure tabs are always created
        try:
            st.markdown("### 📊 Dataset Overview")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("📈 Rows", f"{combined_data.shape[0]:,}")
            with col2:
                st.metric("📋 Columns", combined_data.shape[1])
            with col3:
                st.metric("🔢 Numeric", len(combined_data.select_dtypes(include=[np.number]).columns))
            with col4:
                st.metric("📝 Categorical", len(combined_data.select_dtypes(include=['object', 'category']).columns))
            with col5:
                st.metric("💾 Memory", f"{combined_data.memory_usage(deep=True).sum() / (1024**2):.2f} MB")
            
            # Data Quality Summary - ALWAYS SHOW FIRST
            st.markdown("---")
            st.markdown("### 🔍 Data Quality Summary")
            with st.expander("📋 View Data Quality Details (Missing Values, Nulls, Duplicates)", expanded=True):
                try:
                    quality_df = data_tools.get_data_quality_summary(combined_data)
                    st.dataframe(quality_df, use_container_width=True, height=400)
                    
                    # Summary metrics
                    total_nulls = quality_df['Null Count'].sum()
                    total_duplicates = quality_df['Duplicates'].sum()
                    avg_completeness = quality_df['Completeness'].str.rstrip('%').astype(float).mean()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("⚠️ Total Nulls", f"{total_nulls:,}")
                    with col2:
                        st.metric("🔄 Total Duplicates", f"{total_duplicates:,}")
                    with col3:
                        st.metric("✅ Avg Completeness", f"{avg_completeness:.1f}%")
                except Exception as e:
                    st.warning(f"Could not generate quality summary: {e}")
        except Exception as e:
            st.warning(f"Error displaying data overview: {e}")
        
        st.markdown("---")
        
        # Create tabs for different sections - TABS ARE ALWAYS CREATED WHEN DATA EXISTS
        # This ensures tabs persist across all interactions and remain visible
        # CRITICAL: Tabs must be created regardless of any errors above
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Statistics", 
            "🔍 Data Analysis", 
            "📈 Visualizations", 
            "🔗 Feature Relationships",
            "💬 AI Chat"
        ])
        
        # Tab 1: Statistics
        with tab1:
            try:
                st.header("📊 Statistical Analysis")
                st.markdown("Get comprehensive statistical insights about your data")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    stat_query = st.text_input(
                        "Ask about statistics:",
                        placeholder="e.g., 'Calculate statistics for all numeric columns', 'Show mean and median for age column'",
                        key="stat_query"
                    )
                with col2:
                    run_stat = st.button("📊 Analyze", type="primary", use_container_width=True)
                
                if run_stat or stat_query:
                    query = stat_query if stat_query else "Calculate comprehensive statistics for all numeric columns"
                    with st.spinner("🤖 Statistical Agent is analyzing..."):
                        try:
                            agent_name, result_text, result_table = route_query(
                                query,
                                st.session_state.agents,
                                combined_data
                            )
                            
                            # Always show table if available
                            if result_table is not None and not result_table.empty:
                                st.subheader("📋 Statistical Results")
                                # Format numeric columns
                                formatted_table = result_table.copy()
                                for col in formatted_table.select_dtypes(include=[np.number]).columns:
                                    formatted_table[col] = formatted_table[col].round(4)
                                st.dataframe(formatted_table, use_container_width=True, height=400)
                            else:
                                # Try to extract table from text
                                extracted_table = extract_dataframe_from_result(result_text, combined_data, query)
                                if extracted_table is not None and not extracted_table.empty:
                                    st.subheader("📋 Statistical Results")
                                    st.dataframe(extracted_table, use_container_width=True, height=400)
                                else:
                                    # Show text only if no table could be extracted
                                    st.subheader("📝 Analysis Results")
                                    st.markdown(f"```\n{result_text}\n```")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
            except Exception as e:
                st.error(f"Error in Statistics tab: {str(e)}")
                st.info("Please try refreshing the page or re-uploading your data.")
            
            # Quick stats buttons
            st.markdown("### ⚡ Quick Statistics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("📊 Summary Stats", use_container_width=True):
                    agent_name, result_text, result_table = route_query(
                        "Calculate comprehensive statistics for all numeric columns",
                        st.session_state.agents,
                        combined_data
                    )
                    if result_table is not None and not result_table.empty:
                        st.dataframe(result_table, use_container_width=True)
                    else:
                        extracted = extract_dataframe_from_result(result_text, combined_data)
                        if extracted is not None and not extracted.empty:
                            st.dataframe(extracted, use_container_width=True)
            with col2:
                if st.button("📈 Distribution", use_container_width=True):
                    numeric_cols = combined_data.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        agent_name, result_text, result_table = route_query(
                            f"Analyze the distribution of {numeric_cols[0]} column",
                            st.session_state.agents,
                            combined_data
                        )
                        if result_table is not None and not result_table.empty:
                            st.dataframe(result_table, use_container_width=True)
                        else:
                            extracted = extract_dataframe_from_result(result_text, combined_data)
                            if extracted is not None and not extracted.empty:
                                st.dataframe(extracted, use_container_width=True)
            with col3:
                if st.button("🧪 Hypothesis Test", use_container_width=True):
                    numeric_cols = combined_data.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        agent_name, result_text, result_table = route_query(
                            f"Perform hypothesis test on {numeric_cols[0]} column",
                            st.session_state.agents,
                            combined_data
                        )
                        if result_table is not None and not result_table.empty:
                            st.dataframe(result_table, use_container_width=True)
                        else:
                            extracted = extract_dataframe_from_result(result_text, combined_data)
                            if extracted is not None and not extracted.empty:
                                st.dataframe(extracted, use_container_width=True)
            with col4:
                if st.button("📉 Percentiles", use_container_width=True):
                    numeric_cols = combined_data.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        st.dataframe(combined_data[numeric_cols].describe().T, use_container_width=True)
        
        # Tab 2: Data Analysis
        with tab2:
            try:
                st.header("🔍 Data Analysis & Exploration")
                st.markdown("Explore, filter, query, and analyze your data")
                
                st.markdown("**💡 Supported Operations:** ORDER BY, GROUP BY, WHERE conditions, LIMIT, multiple filters with AND/OR logic")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    analysis_query = st.text_input(
                        "Ask about your data (supports SQL-like queries):",
                        placeholder="e.g., 'Order by salary desc limit 10', 'Group by department calculate average salary', 'Filter where age > 30 and salary > 50000'",
                        key="analysis_query"
                    )
                with col2:
                    run_analysis = st.button("🔍 Analyze", type="primary", use_container_width=True)
                
                if run_analysis or analysis_query:
                    query = analysis_query if analysis_query else "Get comprehensive information about the dataset"
                    with st.spinner("🤖 Analysis Agent is processing..."):
                        try:
                            agent_name, result_text, result_table = route_query(
                                query,
                                st.session_state.agents,
                                combined_data
                            )
                            
                            # Always prioritize showing table format
                            if result_table is not None and not result_table.empty:
                                st.subheader("📋 Analysis Results")
                                st.dataframe(result_table, use_container_width=True, height=400)
                            else:
                                # Try to extract table from text
                                extracted_table = extract_dataframe_from_result(result_text, combined_data, query)
                                if extracted_table is not None and not extracted_table.empty:
                                    st.subheader("📋 Analysis Results")
                                    st.dataframe(extracted_table, use_container_width=True, height=400)
                                else:
                                    # Only show text if no table could be extracted
                                    st.subheader("📝 Analysis Results")
                                    st.markdown(f"```\n{result_text}\n```")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                            st.info("Try rephrasing your query or use simpler syntax like 'order by column_name' or 'group by column_name'")
                
                # Data preview
                st.markdown("### 👁️ Data Preview")
                preview_rows = st.slider("Number of rows to preview", 5, 100, 10)
                st.dataframe(combined_data.head(preview_rows), use_container_width=True, height=400)
                
                # Quick analysis buttons
                st.markdown("### ⚡ Quick Actions")
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    if st.button("📋 Data Info", use_container_width=True):
                        agent_name, result_text, result_table = route_query(
                            "Get comprehensive information about the dataset",
                            st.session_state.agents,
                            combined_data
                        )
                        if result_table is not None and not result_table.empty:
                            st.dataframe(result_table, use_container_width=True)
                        else:
                            extracted = extract_dataframe_from_result(result_text, combined_data)
                            if extracted is not None and not extracted.empty:
                                st.dataframe(extracted, use_container_width=True)
                with col2:
                    if st.button("🔍 Data Quality", use_container_width=True):
                        try:
                            quality_df = data_tools.get_data_quality_summary(combined_data)
                            st.dataframe(quality_df, use_container_width=True)
                        except Exception as e:
                            st.error(f"Error: {e}")
                with col3:
                    if st.button("🔍 Detect Outliers", use_container_width=True):
                        numeric_cols = combined_data.select_dtypes(include=[np.number]).columns
                        if len(numeric_cols) > 0:
                            agent_name, result_text, result_table = route_query(
                                f"Detect outliers in {numeric_cols[0]} column",
                                st.session_state.agents,
                                combined_data
                            )
                            if result_table is not None and not result_table.empty:
                                st.dataframe(result_table, use_container_width=True)
                            else:
                                extracted = extract_dataframe_from_result(result_text, combined_data)
                                if extracted is not None and not extracted.empty:
                                    st.dataframe(extracted, use_container_width=True)
                with col4:
                    if st.button("📊 Column Info", use_container_width=True):
                        st.dataframe(combined_data.dtypes.to_frame('Data Type'), use_container_width=True)
                with col5:
                    if st.button("🔢 Missing Values", use_container_width=True):
                        missing = combined_data.isnull().sum()
                        missing_df = missing[missing > 0].to_frame('Missing Count')
                        missing_df['Percentage'] = (missing_df['Missing Count'] / len(combined_data) * 100).round(2)
                        st.dataframe(missing_df, use_container_width=True)
            except Exception as e:
                st.error(f"Error in Data Analysis tab: {str(e)}")
                st.info("Please try refreshing the page or re-uploading your data.")
        
        # Tab 3: Visualizations
        with tab3:
            try:
                st.header("📈 Data Visualizations")
                st.markdown("Create beautiful charts and graphs from your data")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    viz_query = st.text_input(
                        "Request a visualization:",
                        placeholder="e.g., 'Create a scatter plot of age vs salary', 'Show histogram of age column', 'Create correlation heatmap'",
                        key="viz_query"
                    )
                with col2:
                    run_viz = st.button("📈 Create", type="primary", use_container_width=True)
                
                if run_viz or viz_query:
                    query = viz_query if viz_query else "Create a correlation heatmap"
                    with st.spinner("🤖 Visualization Agent is creating your chart..."):
                        try:
                            agent_name, result_text, result_table = route_query(
                                query,
                                st.session_state.agents,
                                combined_data
                            )
                            st.success(f"✅ Visualization created by {agent_name.replace('_', ' ').title()} Agent")
                            if result_text:
                                st.text(result_text)
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                
                # Quick visualization buttons
                st.markdown("### ⚡ Quick Visualizations")
                numeric_cols = list(combined_data.select_dtypes(include=[np.number]).columns)
                categorical_cols = list(combined_data.select_dtypes(include=['object', 'category']).columns)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("📊 Histogram", use_container_width=True) and len(numeric_cols) > 0:
                        route_query(
                            f"Create a histogram of {numeric_cols[0]} column",
                            st.session_state.agents,
                            combined_data
                        )
                with col2:
                    if st.button("📈 Scatter Plot", use_container_width=True) and len(numeric_cols) >= 2:
                        route_query(
                            f"Create a scatter plot of {numeric_cols[0]} vs {numeric_cols[1]}",
                            st.session_state.agents,
                            combined_data
                        )
                with col3:
                    if st.button("🔥 Heatmap", use_container_width=True):
                        route_query(
                            "Create a correlation heatmap",
                            st.session_state.agents,
                            combined_data
                        )
                with col4:
                    if st.button("📊 Box Plot", use_container_width=True) and len(numeric_cols) > 0:
                        route_query(
                            f"Create a box plot of {numeric_cols[0]} column",
                            st.session_state.agents,
                            combined_data
                        )
                
                if len(numeric_cols) >= 2:
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📉 Line Plot", use_container_width=True):
                            route_query(
                                f"Create a line plot of {numeric_cols[0]} vs {numeric_cols[1]}",
                                st.session_state.agents,
                                combined_data
                            )
                    with col2:
                        if st.button("🔗 Pair Plot", use_container_width=True) and len(numeric_cols) >= 3:
                            route_query(
                                f"Create a pair plot for {', '.join(numeric_cols[:3])}",
                                st.session_state.agents,
                                combined_data
                            )
                
                if len(categorical_cols) > 0:
                    if st.button("📊 Bar Chart", use_container_width=True):
                        route_query(
                            f"Create a bar chart of {categorical_cols[0]} column",
                            st.session_state.agents,
                            combined_data
                        )
            except Exception as e:
                st.error(f"Error in Visualizations tab: {str(e)}")
                st.info("Please try refreshing the page or re-uploading your data.")
        
        # Tab 4: Feature Relationships
        with tab4:
            try:
                st.header("🔗 Feature Relationships & Correlations")
                st.markdown("Discover relationships and dependencies between features")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    rel_query = st.text_input(
                        "Analyze relationships:",
                        placeholder="e.g., 'Show correlations between all features', 'Analyze feature relationships', 'Show feature importance for target column'",
                        key="rel_query"
                    )
                with col2:
                    run_rel = st.button("🔗 Analyze", type="primary", use_container_width=True)
                
                if run_rel or rel_query:
                    query = rel_query if rel_query else "Analyze correlations between all numeric features and format as table"
                    with st.spinner("🤖 Statistical Agent is analyzing relationships..."):
                        try:
                            agent_name, result_text, result_table = route_query(
                                query,
                                st.session_state.agents,
                                combined_data
                            )
                            
                            # Always show table format for relationships
                            if result_table is not None and not result_table.empty:
                                st.subheader("📋 Feature Relationships")
                                # Format numeric columns to 4 decimal places
                                formatted_table = result_table.copy()
                                for col in formatted_table.select_dtypes(include=[np.number]).columns:
                                    formatted_table[col] = formatted_table[col].round(4)
                                st.dataframe(formatted_table, use_container_width=True, height=400)
                            else:
                                # Try to extract table from text
                                extracted_table = extract_dataframe_from_result(result_text, combined_data, query)
                                if extracted_table is not None and not extracted_table.empty:
                                    st.subheader("📋 Feature Relationships")
                                    # Format numeric columns to 4 decimal places
                                    formatted_table = extracted_table.copy()
                                    for col in formatted_table.select_dtypes(include=[np.number]).columns:
                                        formatted_table[col] = formatted_table[col].round(4)
                                    st.dataframe(formatted_table, use_container_width=True, height=400)
                                else:
                                    # For correlation queries, try to get correlation matrix directly
                                    if 'correlation' in query.lower():
                                        try:
                                            numeric_cols = combined_data.select_dtypes(include=[np.number]).columns
                                            if len(numeric_cols) >= 2:
                                                corr_df = statistical_tools.analyze_correlations(combined_data)
                                                if not corr_df.empty:
                                                    st.subheader("📋 Correlation Matrix")
                                                    formatted_corr = corr_df.round(4)
                                                    st.dataframe(formatted_corr, use_container_width=True, height=400)
                                                else:
                                                    st.markdown(f"```\n{result_text}\n```")
                                            else:
                                                st.markdown(f"```\n{result_text}\n```")
                                        except:
                                            st.markdown(f"```\n{result_text}\n```")
                                    else:
                                        st.markdown(f"```\n{result_text}\n```")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                
                # Quick relationship buttons
                st.markdown("### ⚡ Quick Relationship Analysis")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("🔗 Correlations", use_container_width=True):
                        # Directly get correlation matrix
                        try:
                            numeric_cols = combined_data.select_dtypes(include=[np.number]).columns
                            if len(numeric_cols) >= 2:
                                corr_df = statistical_tools.analyze_correlations(combined_data)
                                if not corr_df.empty:
                                    formatted_corr = corr_df.round(4)
                                    st.dataframe(formatted_corr, use_container_width=True)
                                else:
                                    agent_name, result_text, result_table = route_query(
                                        "Analyze correlations between all numeric features and format as table",
                                        st.session_state.agents,
                                        combined_data
                                    )
                                    if result_table is not None and not result_table.empty:
                                        formatted_table = result_table.round(4)
                                        st.dataframe(formatted_table, use_container_width=True)
                            else:
                                st.warning("Need at least 2 numeric columns for correlation analysis")
                        except Exception as e:
                            st.error(f"Error: {e}")
                with col2:
                    if st.button("📊 Feature Relationships", use_container_width=True):
                        try:
                            rel_df = statistical_tools.feature_relationships(combined_data)
                            if not rel_df.empty:
                                formatted_rel = rel_df.round(4)
                                st.dataframe(formatted_rel, use_container_width=True)
                            else:
                                agent_name, result_text, result_table = route_query(
                                    "Analyze relationships between all feature pairs",
                                    st.session_state.agents,
                                    combined_data
                                )
                                if result_table is not None and not result_table.empty:
                                    formatted_table = result_table.round(4)
                                    st.dataframe(formatted_table, use_container_width=True)
                        except Exception as e:
                            st.error(f"Error: {e}")
                with col3:
                    if st.button("🔥 Correlation Heatmap", use_container_width=True):
                        route_query(
                            "Create a correlation heatmap",
                            st.session_state.agents,
                            combined_data
                        )
                with col4:
                    if st.button("⭐ Feature Importance", use_container_width=True):
                        numeric_cols = combined_data.select_dtypes(include=[np.number]).columns
                        if len(numeric_cols) > 1:
                            agent_name, result_text, result_table = route_query(
                                f"Calculate feature importance for {numeric_cols[-1]} column",
                                st.session_state.agents,
                                combined_data
                            )
                            if result_table is not None and not result_table.empty:
                                formatted_table = result_table.round(4)
                                st.dataframe(formatted_table, use_container_width=True)
                            else:
                                extracted = extract_dataframe_from_result(result_text, combined_data)
                                if extracted is not None and not extracted.empty:
                                    formatted_extracted = extracted.round(4)
                                    st.dataframe(formatted_extracted, use_container_width=True)
            except Exception as e:
                st.error(f"Error in Feature Relationships tab: {str(e)}")
                st.info("Please try refreshing the page or re-uploading your data.")
        
        # Tab 5: AI Chat
        with tab5:
            try:
                st.header("💬 AI-Powered Chat")
                st.markdown("Ask any question about your data in natural language")
                
                # Chat interface
                query = st.text_input(
                    "💬 Ask me anything about your data:",
                    placeholder="e.g., 'What insights can you give me about this dataset?', 'Compare the first two numeric columns', 'What are the key findings?'",
                    key="chat_query"
                )
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    run_chat = st.button("🚀 Ask", type="primary", use_container_width=True)
                
                if run_chat and query:
                    with st.spinner("🤖 AI Agents are thinking..."):
                        try:
                            agent_name, result_text, result_table = route_query(
                                query,
                                st.session_state.agents,
                                combined_data
                            )
                            
                            st.success(f"✅ Answered by: **{agent_name.replace('_', ' ').title()} Agent**")
                            
                            # Always prioritize showing table format
                            if result_table is not None and not result_table.empty:
                                st.subheader("📋 Results")
                                st.dataframe(result_table, use_container_width=True, height=400)
                            else:
                                # Try to extract table from text
                                extracted_table = extract_dataframe_from_result(result_text, combined_data, query)
                                if extracted_table is not None and not extracted_table.empty:
                                    st.subheader("📋 Results")
                                    st.dataframe(extracted_table, use_container_width=True, height=400)
                            
                            # Show text answer only if it contains additional insights beyond the table
                            if result_text and (result_table is None or result_table.empty):
                                st.subheader("📝 Answer")
                                st.markdown(result_text)
                            elif result_text and len(result_text) > 200:  # Show if there's substantial text content
                                st.subheader("📝 Additional Insights")
                                st.markdown(result_text)
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                            st.info("Make sure your OPENAI_API_KEY is valid and you have API credits.")
                
                # Example queries
                st.markdown("### 💡 Example Questions")
                examples = [
                    "What are the main insights from this dataset?",
                    "Show me the top 10 rows",
                    "What columns have missing values?",
                    "Create a summary of all numeric columns",
                    "What is the relationship between the first two numeric columns?"
                ]
                for example in examples:
                    if st.button(f"💡 {example}", key=f"example_{example}", use_container_width=True):
                        with st.spinner("🤖 Processing..."):
                            try:
                                agent_name, result_text, result_table = route_query(
                                    example,
                                    st.session_state.agents,
                                    combined_data
                                )
                                if result_table is not None and not result_table.empty:
                                    st.dataframe(result_table, use_container_width=True)
                                else:
                                    extracted = extract_dataframe_from_result(result_text, combined_data, example)
                                    if extracted is not None and not extracted.empty:
                                        st.dataframe(extracted, use_container_width=True)
                                    else:
                                        st.markdown(result_text)
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
            except Exception as e:
                st.error(f"Error in AI Chat tab: {str(e)}")
                st.info("Please try refreshing the page or re-uploading your data.")
    
    else:
        # Welcome screen
        st.info("👆 **Please upload CSV or Excel files to get started**")
        
        st.markdown("""
        ### 🎯 What You Can Do:
        
        #### 📊 **Statistics Tab**
        - Comprehensive statistical analysis
        - Mean, median, mode, standard deviation
        - Distribution analysis
        - Hypothesis testing
        
        #### 🔍 **Data Analysis Tab**
        - Explore and query your data
        - Filter and group data
        - Detect outliers
        - Data quality assessment
        
        #### 📈 **Visualizations Tab**
        - Histograms, scatter plots, bar charts
        - Correlation heatmaps
        - Box plots, line plots, pair plots
        - Custom visualizations
        
        #### 🔗 **Feature Relationships Tab**
        - Correlation analysis
        - Feature dependencies
        - Feature importance
        - Relationship strength analysis
        
        #### 💬 **AI Chat Tab**
        - Natural language queries
        - Intelligent data insights
        - Multi-agent coordination
        - Contextual answers
        """)


if __name__ == "__main__":
    main()
