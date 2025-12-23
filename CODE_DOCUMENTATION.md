# Comprehensive Code Documentation
## Multi-Agent Data Analysis System with OpenAI Agents SDK

**Version:** 1.0  
**Date:** 2025  
**Author:** AI Data Analysis System

---

## Table of Contents

1. [Introduction](#introduction)
2. [OpenAI Agents SDK Architecture](#openai-agents-sdk-architecture)
3. [Project Structure](#project-structure)
4. [Main Application File: data-insights.py](#main-application-file)
5. [Tool Modules](#tool-modules)
6. [Code Block-by-Block Analysis](#code-block-by-block-analysis)
7. [How Everything Works Together](#how-everything-works-together)
8. [Agent Workflow](#agent-workflow)

---

## Introduction

This document provides a comprehensive explanation of every code file, every block of code, and how the OpenAI Agents SDK works in this Multi-Agent Data Analysis System. The system uses specialized AI agents to perform data analysis, statistical computations, visualizations, and data formatting.

### System Overview

The application is a Streamlit-based web application that uses OpenAI's Agents SDK to create specialized AI agents. Each agent has specific tools and capabilities:

- **Analysis Agent**: Data exploration, querying, filtering, grouping
- **Statistical Agent**: Advanced statistics, correlations, feature relationships
- **Visualization Agent**: Creating charts and graphs
- **Formatting Agent**: Structuring results into tables
- **Orchestrator Agent**: Routes queries to appropriate agents

---

## OpenAI Agents SDK Architecture

### What is OpenAI Agents SDK?

The OpenAI Agents SDK is a framework that allows you to create AI agents with specific capabilities. Each agent can:
- Have custom instructions (system prompts)
- Use function tools (callable functions)
- Process natural language queries
- Return structured results

### Key Components

#### 1. Agent Class
```python
from agents import Agent

agent = Agent(
    name="Agent Name",
    instructions="Detailed instructions for the agent",
    tools=[function1, function2, ...]
)
```

**Parameters:**
- `name`: Identifier for the agent
- `instructions`: System prompt that defines the agent's role and behavior
- `tools`: List of function tools the agent can use

#### 2. Function Tools
```python
from agents import function_tool

@function_tool
def my_function(param: str) -> str:
    """Description of what the function does."""
    # Function implementation
    return result
```

**Key Points:**
- Decorator `@function_tool` marks a function as a tool
- Docstring becomes the tool description for the AI
- Type hints help the AI understand parameters
- Return value is used by the agent

#### 3. Runner
```python
from agents import Runner

result = Runner.run_sync(agent, user_query)
final_output = result.final_output
```

**How it works:**
1. User query is sent to the agent
2. Agent analyzes the query
3. Agent decides which tools to use
4. Tools are executed
5. Results are returned to the agent
6. Agent processes results and generates final output

### Agent Decision-Making Process

1. **Query Analysis**: Agent reads and understands the user's query
2. **Tool Selection**: Agent identifies which tools are needed
3. **Tool Execution**: Selected tools are called with appropriate parameters
4. **Result Processing**: Agent analyzes tool outputs
5. **Response Generation**: Agent creates a natural language response

---

## Project Structure

```
data-analyzer/
├── data-insights.py          # Main Streamlit application
├── tools/                    # Tool modules
│   ├── __init__.py          # Package initialization
│   ├── data_tools.py        # Data manipulation tools
│   ├── statistical_tools.py # Statistical analysis tools
│   ├── visualization_tools.py # Chart creation tools
│   └── formatting_tools.py  # Table formatting tools
├── requirements.txt         # Python dependencies
└── venv/                    # Virtual environment
```

---

## Main Application File: data-insights.py

### File Overview

This is the main Streamlit application file that orchestrates the entire system. It's approximately 1,362 lines of code.

### Section 1: Imports and Setup (Lines 1-30)

```python
import os
import streamlit as st
import pandas as pd
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
import ssl
from typing import Optional, Dict, List, Union
import numpy as np
from tools import data_tools, statistical_tools, visualization_tools, formatting_tools
import re
import io
```

**Explanation:**
- **os**: Environment variable access
- **streamlit**: Web framework for the UI
- **pandas**: Data manipulation
- **agents**: OpenAI Agents SDK components
- **dotenv**: Loads environment variables from .env file
- **ssl**: SSL certificate handling
- **typing**: Type hints for better code documentation
- **numpy**: Numerical operations
- **tools**: Custom tool modules

**Session State Initialization:**
```python
if 'dataframe' not in st.session_state:
    st.session_state.dataframe = None
if 'agents' not in st.session_state:
    st.session_state.agents = {}
```

**Purpose:** Maintains state across Streamlit reruns. Stores:
- Loaded dataframe
- Created agents (to avoid recreating them)

### Section 2: Data Loading Function (Lines 32-42)

```python
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
```

**Explanation:**
- `@st.cache_data`: Streamlit decorator that caches the result
- Handles both CSV and Excel files
- Combines multiple files into one dataframe
- `ignore_index=True`: Resets index after concatenation

### Section 3: Text Parsing Functions (Lines 45-194)

#### parse_text_to_dataframe (Lines 45-151)

**Purpose:** Converts text output from agents into pandas DataFrames.

**How it works:**
1. Detects pipe-separated tables (`|` delimiters)
2. Extracts correlation coefficients from text
3. Parses CSV-like data
4. Returns DataFrame if successful, None otherwise

**Key Logic:**
```python
# Detects tables with | separators
if '|' in line and line.strip().startswith('|'):
    table_lines.append(line)
```

#### extract_dataframe_from_result (Lines 154-194)

**Purpose:** Multiple fallback methods to extract tabular data.

**Methods:**
1. Calls `parse_text_to_dataframe`
2. Uses formatting tools
3. Directly executes simple queries (ORDER BY, LIMIT)

### Section 4: Agent Creation Function (Lines 197-580)

This is the core function that creates all specialized agents.

#### Analysis Agent (Lines 207-364)

**Tools Created:**
1. `query_data`: Executes SQL-like queries
2. `filter_data`: Filters by column and condition
3. `multi_filter`: Multiple conditions with AND/OR logic
4. `group_by_aggregate`: Groups and aggregates data
5. `advanced_group_by`: Multiple aggregations
6. `order_by`: Sorts data
7. `get_data_info`: Dataset information
8. `get_data_quality`: Data quality metrics
9. `detect_outliers`: Finds outliers
10. `execute_sql_query`: SQL-like operations

**Agent Instructions:**
The agent is given detailed instructions about:
- Available columns in the dataframe
- Supported SQL operations
- How to handle user queries
- Expected output format

**Example Tool:**
```python
@function_tool
def query_data(query: str) -> str:
    """Query the dataframe using natural language."""
    try:
        result = data_tools.execute_complex_query(dataframe, query)
        if not result.empty:
            return f"Query Results ({len(result)} rows):\n{result.to_string()}"
        return data_tools.query_dataframe(query, dataframe)
    except Exception as e:
        return f"Error: {str(e)}. Available columns: {list(dataframe.columns)}"
```

**How it works:**
1. User asks: "Show top 10 orders by total amount"
2. Agent calls `query_data` with the query
3. Function parses the query and executes it
4. Returns formatted results
5. Agent presents results to user

#### Statistical Agent (Lines 366-445)

**Tools:**
1. `calculate_statistics`: Descriptive statistics
2. `analyze_correlations`: Correlation matrices
3. `feature_relationships`: Feature pair analysis
4. `hypothesis_test`: Statistical tests
5. `distribution_analysis`: Distribution metrics
6. `feature_importance`: Feature ranking

**Example:**
```python
@function_tool
def calculate_statistics() -> str:
    """Calculate comprehensive descriptive statistics."""
    stats_df = statistical_tools.calculate_statistics(dataframe)
    if stats_df.empty:
        return "No numeric columns found."
    return f"Statistical Summary:\n{stats_df.to_string()}"
```

#### Visualization Agent (Lines 447-500)

**Tools:**
1. `create_histogram`: Distribution visualization
2. `create_scatter`: Relationship plots
3. `create_correlation_heatmap`: Correlation visualization
4. `create_bar_chart`: Categorical data
5. `create_box_plot`: Distribution and outliers
6. `create_line_plot`: Time series
7. `create_pair_plot`: Multi-variable relationships

#### Formatting Agent (Lines 502-548)

**Tools:**
1. `format_as_table`: Convert data to tables
2. `create_summary_table`: Statistics tables
3. `format_correlation_table`: Correlation tables
4. `format_insights`: Insights tables

#### Orchestrator Agent (Lines 550-571)

**Purpose:** Routes queries to appropriate agents (currently not actively used, but available for future multi-agent coordination).

### Section 5: Query Routing Function (Lines 583-630)

```python
def route_query(query: str, agents: Dict[str, Agent], dataframe: pd.DataFrame) -> tuple:
```

**Purpose:** Determines which agent should handle a query.

**Routing Logic:**
- Keywords like "order by", "filter" → Analysis Agent
- Keywords like "plot", "chart" → Visualization Agent
- Keywords like "statistic", "correlation" → Statistical Agent
- Keywords like "format", "table" → Formatting Agent

**Returns:** `(agent_name, result_text, result_table)`

**Enhanced Extraction:**
- Tries to extract tabular data from text results
- For statistical queries, directly gets correlation/statistics dataframes
- Multiple fallback methods

### Section 6: Main Streamlit Application (Lines 632-1362)

#### Page Configuration (Lines 633-637)

```python
st.set_page_config(
    page_title="Multi-Agent Data Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

#### Custom CSS (Lines 639-655)

Styles the application with custom colors and layouts.

#### Header and API Key Check (Lines 657-671)

- Displays application header
- Checks for OpenAI API key
- Shows error if missing

#### Sidebar (Lines 673-694)

- File uploader for CSV/Excel files
- About section with agent descriptions

#### Data Loading and Overview (Lines 696-758)

**Process:**
1. User uploads files
2. Files are loaded and combined
3. Agents are created (cached in session state)
4. Data overview metrics displayed
5. Data quality summary shown

#### Tab Structure (Lines 760-1362)

Five main tabs:

1. **Statistics Tab** (Lines 768-849)
   - Statistical analysis queries
   - Quick statistics buttons
   - Results displayed in tables

2. **Data Analysis Tab** (Lines 851-1003)
   - SQL-like queries
   - Data preview
   - Quick action buttons
   - Results in tabular format

3. **Visualizations Tab** (Lines 1005-1097)
   - Visualization requests
   - Quick visualization buttons
   - Charts displayed inline

4. **Feature Relationships Tab** (Lines 1099-1235)
   - Correlation analysis
   - Feature relationship queries
   - Quick relationship buttons
   - Results in formatted tables

5. **AI Chat Tab** (Lines 1237-1317)
   - Natural language queries
   - Example questions
   - Multi-agent coordination

**Tab Implementation Pattern:**
```python
with tab1:
    try:
        # Tab content
        # Query input
        # Results display
    except Exception as e:
        st.error(f"Error: {str(e)}")
```

**Error Handling:**
Each tab is wrapped in try-except to prevent errors from breaking the application.

---

## Tool Modules

### tools/data_tools.py

**Purpose:** Data manipulation and querying functions.

#### Key Functions:

1. **query_dataframe** (Lines 7-67)
   - Handles common query patterns
   - Returns string representation of results

2. **filter_dataframe** (Lines 70-109)
   - Filters by column and condition
   - Supports: greater, less, equal, contains, between

3. **group_by_aggregate** (Lines 112-162)
   - Groups data and applies aggregations
   - Functions: sum, mean, count, max, min, std

4. **detect_outliers** (Lines 165-200)
   - IQR method: Q1 - 1.5*IQR to Q3 + 1.5*IQR
   - Z-score method: values beyond 3 standard deviations

5. **get_data_info** (Lines 203-224)
   - Comprehensive dataset information
   - Returns dictionary with shape, columns, types, etc.

6. **get_data_quality_summary** (Lines 227-261)
   - Creates DataFrame with quality metrics
   - Includes: null counts, duplicates, completeness

7. **execute_complex_query** (Lines 264-313)
   - Parses natural language queries
   - Extracts ORDER BY, LIMIT, WHERE, GROUP BY
   - Uses regex to parse query components

8. **multi_condition_filter** (Lines 316-359)
   - Multiple conditions with AND/OR logic
   - Creates boolean masks and combines them

9. **advanced_group_by** (Lines 362-379)
   - Multiple grouping columns
   - Multiple aggregation functions

### tools/statistical_tools.py

**Purpose:** Statistical analysis functions.

#### Key Functions:

1. **calculate_statistics** (Lines 8-36)
   - Descriptive statistics for numeric columns
   - Returns: count, mean, median, std, min, max, quartiles, skewness, kurtosis

2. **analyze_correlations** (Lines 39-55)
   - Correlation matrix calculation
   - Methods: pearson, spearman, kendall

3. **feature_relationships** (Lines 58-104)
   - Analyzes all feature pairs
   - Numeric-numeric: correlation
   - Categorical-numeric: ANOVA F-test

4. **hypothesis_test** (Lines 121-171)
   - One-sample t-test
   - Normality test (D'Agostino)

5. **distribution_analysis** (Lines 174-220)
   - Comprehensive distribution metrics
   - Determines distribution type (normal, skewed)

6. **feature_importance** (Lines 223-257)
   - Correlation with target column
   - Ranks features by importance

### tools/visualization_tools.py

**Purpose:** Chart and graph creation.

#### Key Functions:

1. **create_histogram** (Lines 10-24)
   - Distribution visualization
   - Uses matplotlib

2. **create_scatter** (Lines 27-41)
   - Relationship between two columns
   - Shows correlation visually

3. **create_correlation_heatmap** (Lines 44-60)
   - Correlation matrix as heatmap
   - Uses seaborn

4. **create_bar_chart** (Lines 63-81)
   - Categorical data visualization
   - Top N values

5. **create_box_plot** (Lines 84-107)
   - Distribution and outliers
   - Shows quartiles

6. **create_line_plot** (Lines 110-125)
   - Time series or sequential data
   - Trend visualization

7. **create_pair_plot** (Lines 128-147)
   - Multiple variable relationships
   - Grid of scatter plots

**Important:** All visualization functions use `st.pyplot(fig)` to display in Streamlit and `plt.close(fig)` to free memory.

### tools/formatting_tools.py

**Purpose:** Convert data to table formats.

#### Key Functions:

1. **format_as_table** (Lines 6-40)
   - Converts various data types to DataFrame
   - Handles: dict, list, string, DataFrame

2. **create_summary_table** (Lines 43-67)
   - Formats statistics dictionary
   - Creates structured table

3. **format_correlation_table** (Lines 126-151)
   - Converts correlation matrix to long format
   - Adds strength labels

4. **format_statistics_table** (Lines 168-188, 191-211)
   - Rounds numeric values
   - Improves readability

### tools/__init__.py

**Purpose:** Package initialization, exports all tool modules.

---

## Code Block-by-Block Analysis

### Agent Creation Pattern

Every agent follows this pattern:

1. **Define Function Tools** using `@function_tool` decorator
2. **Create Agent** with name, instructions, and tools
3. **Return Agent** in dictionary

**Example:**
```python
# Step 1: Define tools
@function_tool
def my_tool(param: str) -> str:
    """Tool description."""
    # Implementation
    return result

# Step 2: Create agent
my_agent = Agent(
    name="My Agent",
    instructions="Agent instructions...",
    tools=[my_tool]
)

# Step 3: Return
return {'my_agent': my_agent}
```

### Query Processing Flow

1. **User Input** → Text query in Streamlit
2. **Route Query** → `route_query()` determines agent
3. **Run Agent** → `Runner.run_sync(agent, query)`
4. **Agent Processes** → Analyzes query, selects tools
5. **Tools Execute** → Functions are called
6. **Results Returned** → Agent formats output
7. **Display** → Results shown in Streamlit

### Error Handling Strategy

**Three Levels:**
1. **Function Level**: Try-except in each tool function
2. **Agent Level**: Agent handles tool errors gracefully
3. **UI Level**: Try-except around each tab

### Session State Management

**Purpose:** Maintain state across Streamlit reruns.

**Stored:**
- `dataframe`: Loaded data
- `agents`: Created agents (expensive to recreate)

**Benefits:**
- Faster performance
- Maintains user context
- Reduces API calls

---

## How Everything Works Together

### Complete Workflow

1. **User Uploads Data**
   - Files uploaded via Streamlit file uploader
   - `load_combined_data()` processes files
   - Data stored in `st.session_state.dataframe`

2. **Agents Created**
   - `create_agents()` called once per dataset
   - Agents stored in `st.session_state.agents`
   - Each agent has access to the dataframe

3. **User Makes Query**
   - Query entered in text input
   - `route_query()` determines appropriate agent
   - Agent selected based on keywords

4. **Agent Executes**
   - `Runner.run_sync()` executes agent
   - Agent analyzes query
   - Agent selects and calls tools
   - Tools execute and return results

5. **Results Displayed**
   - Agent formats results
   - `extract_dataframe_from_result()` tries to get table
   - Results displayed in Streamlit
   - Tables shown with `st.dataframe()`

### Data Flow Diagram

```
User Query
    ↓
route_query()
    ↓
Select Agent (Analysis/Statistical/Visualization/Formatting)
    ↓
Runner.run_sync(agent, query)
    ↓
Agent analyzes query
    ↓
Agent selects tools
    ↓
Tools execute (data_tools/statistical_tools/etc.)
    ↓
Results returned to agent
    ↓
Agent formats output
    ↓
extract_dataframe_from_result()
    ↓
Display in Streamlit
```

### Agent Interaction

**Current Implementation:**
- Agents work independently
- Each agent handles specific query types
- Routing function selects appropriate agent

**Future Enhancement:**
- Orchestrator agent can coordinate multiple agents
- Agents can call other agents
- Complex queries can use multiple agents

---

## Agent Workflow

### Example: "Show top 10 orders by total amount"

1. **User enters query** in Data Analysis tab

2. **route_query() analyzes:**
   - Detects "order by" → Analysis Agent
   - Returns Analysis Agent

3. **Runner.run_sync() executes:**
   - Agent receives query
   - Agent analyzes: "top 10" = LIMIT 10, "order by total amount" = ORDER BY TotalAmount DESC

4. **Agent selects tool:**
   - Chooses `execute_sql_query` or `order_by` + `query_data`

5. **Tool executes:**
   ```python
   execute_complex_query(dataframe, query)
   # Extracts: ORDER BY TotalAmount DESC LIMIT 10
   # Executes: dataframe.sort_values('TotalAmount', ascending=False).head(10)
   ```

6. **Results returned:**
   - DataFrame with top 10 rows
   - Converted to string format

7. **Agent formats:**
   - Creates natural language response
   - Includes the table

8. **Display:**
   - `extract_dataframe_from_result()` extracts DataFrame
   - `st.dataframe()` displays table
   - Text response shown below

### Example: "Show correlations between all features"

1. **User enters query** in Feature Relationships tab

2. **route_query() analyzes:**
   - Detects "correlation" → Statistical Agent

3. **Agent selects tool:**
   - Chooses `analyze_correlations`

4. **Tool executes:**
   ```python
   analyze_correlations(dataframe, method='pearson')
   # Returns: correlation matrix DataFrame
   ```

5. **Results displayed:**
   - Correlation matrix shown as formatted table
   - Values rounded to 4 decimal places

---

## Key Concepts

### Function Tools

**Why use @function_tool?**
- Makes functions callable by AI agents
- Docstrings become tool descriptions
- Type hints help AI understand parameters
- Enables AI to decide when to use tools

### Agent Instructions

**Purpose:** System prompt that defines agent behavior.

**Components:**
- Role definition
- Available capabilities
- Data context (column names)
- Expected output format
- Best practices

### Runner

**Purpose:** Executes agents with queries.

**Process:**
1. Sends query to agent
2. Agent decides on tools
3. Tools execute
4. Results return to agent
5. Agent generates final response

### Session State

**Purpose:** Maintains state in Streamlit.

**Why needed:**
- Streamlit reruns entire script on interaction
- Without session state, data would reload
- Agents would be recreated (expensive)

---

## Best Practices Implemented

1. **Error Handling**: Try-except at multiple levels
2. **Caching**: Agents cached in session state
3. **Type Hints**: All functions have type hints
4. **Documentation**: Comprehensive docstrings
5. **Modularity**: Separate tool modules
6. **User Experience**: Tabular results, clear errors
7. **Performance**: Caching, efficient queries

---

## Dependencies

From `requirements.txt`:
- `openai`: OpenAI API client
- `pandas`: Data manipulation
- `streamlit`: Web framework
- `python-dotenv`: Environment variables
- `scipy`: Statistical functions
- `matplotlib`: Plotting
- `seaborn`: Statistical visualizations
- `openai-agents`: Agents SDK
- `eval-type-backport`: Type evaluation

---

## Conclusion

This Multi-Agent Data Analysis System demonstrates:

1. **OpenAI Agents SDK Usage**: Creating specialized agents with tools
2. **Modular Architecture**: Separate tool modules
3. **User-Friendly Interface**: Streamlit web application
4. **Comprehensive Functionality**: Data analysis, statistics, visualizations
5. **Error Resilience**: Multiple error handling layers
6. **Performance Optimization**: Caching and efficient queries

The system successfully combines:
- AI agent intelligence
- Data analysis capabilities
- User-friendly interface
- Comprehensive error handling

---

**End of Documentation**


