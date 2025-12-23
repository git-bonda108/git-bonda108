# 🤖 Multi-Agent Data Analysis System

A powerful, enterprise-grade data analysis platform powered by **OpenAI Agents SDK**, featuring specialized AI agents for comprehensive data analysis, visualization, and statistical insights.

## 🚀 Resume Description (3 Lines)

**Multi-Agent Data Analysis System** - Developed an AI-powered data analysis platform using OpenAI Agents SDK with 5 specialized agents (Analysis, Statistical, Visualization, Formatting, Orchestrator) that process natural language queries to perform complex data operations, statistical analysis, and generate visualizations. Built with Streamlit, Python, and pandas, featuring SQL-like query support, correlation analysis, hypothesis testing, and automated table formatting. Implements session state management, error handling, and modular architecture for scalable data analysis workflows.

## 🎯 Features

### ✨ Multi-Agent Architecture
- **Analysis Agent**: Data exploration, querying, filtering, grouping with SQL-like operations
- **Statistical Agent**: Advanced statistics, correlations, feature relationships, hypothesis testing
- **Visualization Agent**: Create charts, graphs, and visualizations
- **Formatting Agent**: Structure results into readable table formats
- **Orchestrator Agent**: Intelligently routes queries to appropriate agents

### 📊 Key Capabilities

- ✅ **Natural Language Queries**: Ask questions in plain English
- ✅ **Feature Relationship Analysis**: Deep insights into data correlations and dependencies
- ✅ **Comprehensive Statistics**: Mean, median, mode, z-scores, p-values, distributions
- ✅ **Advanced Visualizations**: Histograms, scatter plots, heatmaps, box plots, pair plots
- ✅ **Table-Formatted Results**: All insights presented in structured table format
- ✅ **Multi-File Support**: Combine multiple CSV/Excel files
- ✅ **Outlier Detection**: Identify anomalies in your data
- ✅ **Hypothesis Testing**: Statistical significance testing
- ✅ **SQL-like Queries**: ORDER BY, GROUP BY, WHERE, LIMIT operations

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.9 or higher
- OpenAI API key

### 2. Setup Virtual Environment

```bash
# Navigate to project directory
cd data-analyzer

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Key

Create a `.env` file in the `data-analyzer` directory:

```bash
OPENAI_API_KEY=your-openai-api-key-here
```

Get your API key from: https://platform.openai.com/api-keys

### 4. Run the Application

```bash
# Activate virtual environment (if not already activated)
source venv/bin/activate

# Run Streamlit
python -m streamlit run data-insights.py
```

The app will open at `http://localhost:8501`

## 📁 Project Structure

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
├── CODE_DOCUMENTATION.md   # Comprehensive code documentation
└── README.md               # This file
```

## 🎨 Usage Guide

### Upload Data

1. Click "Upload CSV or Excel files" in the sidebar
2. Select one or more data files
3. Data will be automatically loaded and combined

### Using the Tabs

#### 📊 Statistics Tab
- Calculate comprehensive statistics
- Analyze distributions
- Perform hypothesis tests
- View percentiles and quartiles

**Example Queries:**
- "Calculate statistics for all numeric columns"
- "Show mean and median for age column"
- "Perform hypothesis test on salary column"

#### 🔍 Data Analysis Tab
- Explore and query your data
- Filter and group data
- Detect outliers
- Data quality assessment

**Example Queries:**
- "Order by salary desc limit 10"
- "Group by department calculate average salary"
- "Filter where age > 30 and salary > 50000"

#### 📈 Visualizations Tab
- Create histograms, scatter plots, bar charts
- Correlation heatmaps
- Box plots, line plots, pair plots

**Example Queries:**
- "Create a scatter plot of age vs salary"
- "Show histogram of age column"
- "Create correlation heatmap"

#### 🔗 Feature Relationships Tab
- Correlation analysis
- Feature dependencies
- Feature importance
- Relationship strength analysis

**Example Queries:**
- "Show correlations between all features"
- "Analyze feature relationships"
- "Show feature importance for target column"

#### 💬 AI Chat Tab
- Natural language queries
- Intelligent data insights
- Multi-agent coordination
- Contextual answers

## 🔧 Technical Details

### Dependencies

- `openai>=2.8.0`: OpenAI API client
- `pandas`: Data manipulation
- `streamlit`: Web framework
- `python-dotenv`: Environment variables
- `scipy`: Statistical functions
- `matplotlib`: Plotting
- `seaborn`: Statistical visualizations
- `openai-agents>=0.6.0`: Agents SDK
- `eval-type-backport`: Type evaluation

### Architecture

The system uses OpenAI's Agents SDK to create specialized AI agents. Each agent has:
- Custom instructions (system prompts)
- Function tools (callable functions)
- Natural language processing capabilities

**Agent Workflow:**
1. User query → Route to appropriate agent
2. Agent analyzes query → Selects tools
3. Tools execute → Return results
4. Agent formats → Displays to user

### Code Documentation

For comprehensive code documentation, see:
- `CODE_DOCUMENTATION.md`: Detailed explanation of every code file and block
- Explains how OpenAI Agents SDK works
- Code block-by-block analysis
- Architecture and workflow diagrams

## 🛠️ Development

### Running Tests

```bash
python test_order_data.py
```

### Code Structure

- **Main Application**: `data-insights.py` - Streamlit UI and agent orchestration
- **Data Tools**: `tools/data_tools.py` - Data manipulation functions
- **Statistical Tools**: `tools/statistical_tools.py` - Statistical analysis
- **Visualization Tools**: `tools/visualization_tools.py` - Chart creation
- **Formatting Tools**: `tools/formatting_tools.py` - Table formatting

## 📝 License

This project is open source and available for use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ using OpenAI Agents SDK**
