# 🧪 Comprehensive Test Cases for mock_order_data_analysis.csv

## 📊 Dataset Overview
- **File**: `mock_order_data_analysis.csv`
- **Columns**: OrderID, OrderDate, CustomerID, ProductID, Quantity, UnitPrice, TotalAmount, OrderStatus, PaymentMethod, ShippingAddress, CreatedDateTime, ModifiedDateTime
- **Data Types**: Mix of numeric (Quantity, UnitPrice, TotalAmount) and categorical (OrderStatus, PaymentMethod, etc.)

---

## ✅ Test Cases by Functionality

### 1. 📊 Statistics Tab Tests

#### Test 1.1: Basic Statistics
**Query**: `"Calculate comprehensive statistics for all numeric columns"`
**Expected**: Statistics table showing mean, median, std, min, max for Quantity, UnitPrice, TotalAmount

#### Test 1.2: Column-Specific Statistics
**Query**: `"Show mean and median for TotalAmount column"`
**Expected**: Mean and median of TotalAmount

#### Test 1.3: Distribution Analysis
**Query**: `"Analyze the distribution of TotalAmount column"`
**Expected**: Distribution analysis with skewness, kurtosis, percentiles

#### Test 1.4: Hypothesis Testing
**Query**: `"Perform hypothesis test on TotalAmount column"`
**Expected**: T-test results against mean

#### Test 1.5: Percentiles
**Query**: Click "📉 Percentiles" button
**Expected**: Percentile table for all numeric columns

---

### 2. 🔍 Data Analysis Tab Tests

#### Test 2.1: ORDER BY - Single Column Ascending
**Query**: `"Order by TotalAmount asc limit 10"`
**Expected**: Top 10 rows with lowest TotalAmount

#### Test 2.2: ORDER BY - Single Column Descending
**Query**: `"Order by TotalAmount desc limit 10"`
**Expected**: Top 10 rows with highest TotalAmount

#### Test 2.3: ORDER BY - Multiple Columns
**Query**: `"Order by OrderStatus desc, then by TotalAmount desc"`
**Expected**: Sorted by OrderStatus first, then TotalAmount

#### Test 2.4: GROUP BY - Simple
**Query**: `"Group by OrderStatus"`
**Expected**: Count of orders per status

#### Test 2.5: GROUP BY with Aggregation
**Query**: `"Group by OrderStatus calculate average TotalAmount"`
**Expected**: Average TotalAmount per OrderStatus

#### Test 2.6: GROUP BY with Multiple Aggregations
**Query**: `"Group by PaymentMethod, calculate sum and average of TotalAmount"`
**Expected**: Sum and average TotalAmount per PaymentMethod

#### Test 2.7: WHERE - Single Condition (Numeric)
**Query**: `"Filter where TotalAmount > 1000"`
**Expected**: All orders with TotalAmount greater than 1000

#### Test 2.8: WHERE - Single Condition (Categorical)
**Query**: `"Filter where OrderStatus == 'Delivered'"`
**Expected**: All delivered orders

#### Test 2.9: WHERE - Multiple Conditions (AND)
**Query**: `"Filter where TotalAmount > 1000 AND Quantity > 5"`
**Expected**: Orders meeting both conditions

#### Test 2.10: WHERE - Multiple Conditions (OR)
**Query**: `"Filter where OrderStatus == 'Delivered' OR OrderStatus == 'Shipped'"`
**Expected**: Orders that are either Delivered or Shipped

#### Test 2.11: WHERE with BETWEEN
**Query**: `"Filter where TotalAmount between 500 and 1500"`
**Expected**: Orders with TotalAmount in range

#### Test 2.12: Complex Query - GROUP BY + ORDER BY + LIMIT
**Query**: `"Group by OrderStatus, calculate average TotalAmount, order by average desc, limit 5"`
**Expected**: Top 5 OrderStatus by average TotalAmount

#### Test 2.13: Complex Query - WHERE + GROUP BY + ORDER BY
**Query**: `"Filter where TotalAmount > 500, group by PaymentMethod, calculate sum of TotalAmount, order by sum desc"`
**Expected**: Payment methods with highest total (filtered)

#### Test 2.14: Data Info
**Query**: Click "📋 Data Info" button
**Expected**: Comprehensive dataset information

#### Test 2.15: Data Quality
**Query**: Click "🔍 Data Quality" button
**Expected**: Data quality summary table

#### Test 2.16: Detect Outliers
**Query**: Click "🔍 Detect Outliers" button (on TotalAmount)
**Expected**: Outliers in TotalAmount column

#### Test 2.17: Missing Values
**Query**: Click "🔢 Missing Values" button
**Expected**: Columns with missing values and percentages

#### Test 2.18: Column Info
**Query**: Click "📊 Column Info" button
**Expected**: Data types for all columns

#### Test 2.19: Natural Language - Top Orders
**Query**: `"Show me the top 10 highest total amounts"`
**Expected**: Top 10 orders by TotalAmount

#### Test 2.20: Natural Language - Group Analysis
**Query**: `"What is the average order amount by payment method?"`
**Expected**: Average TotalAmount grouped by PaymentMethod

#### Test 2.21: Natural Language - Filter Analysis
**Query**: `"Show me all processing orders with total amount greater than 2000"`
**Expected**: Processing orders with TotalAmount > 2000

---

### 3. 📈 Visualizations Tab Tests

#### Test 3.1: Histogram
**Query**: `"Create a histogram of TotalAmount column"`
**Expected**: Histogram showing distribution of TotalAmount

#### Test 3.2: Scatter Plot
**Query**: `"Create a scatter plot of Quantity vs TotalAmount"`
**Expected**: Scatter plot showing relationship

#### Test 3.3: Correlation Heatmap
**Query**: `"Create a correlation heatmap"`
**Expected**: Heatmap showing correlations between numeric columns

#### Test 3.4: Bar Chart
**Query**: `"Create a bar chart of OrderStatus column"`
**Expected**: Bar chart showing count per OrderStatus

#### Test 3.5: Box Plot
**Query**: `"Create a box plot of TotalAmount column"`
**Expected**: Box plot showing distribution and outliers

#### Test 3.6: Line Plot
**Query**: `"Create a line plot of Quantity vs TotalAmount"`
**Expected**: Line plot showing trend

#### Test 3.7: Pair Plot
**Query**: `"Create a pair plot for Quantity, UnitPrice, TotalAmount"`
**Expected**: Pair plot matrix

---

### 4. 🔗 Feature Relationships Tab Tests

#### Test 4.1: Correlation Analysis
**Query**: `"Show correlations between all numeric features"`
**Expected**: Correlation matrix table

#### Test 4.2: Feature Relationships
**Query**: `"Analyze relationships between all feature pairs"`
**Expected**: Feature relationship table

#### Test 4.3: Correlation Heatmap
**Query**: Click "🔥 Correlation Heatmap" button
**Expected**: Visual correlation heatmap

#### Test 4.4: Feature Importance
**Query**: `"Calculate feature importance for TotalAmount column"`
**Expected**: Features ranked by correlation with TotalAmount

---

### 5. 💬 AI Chat Tab Tests

#### Test 5.1: General Insights
**Query**: `"What are the main insights from this dataset?"`
**Expected**: Comprehensive insights about the order data

#### Test 5.2: Top Rows
**Query**: `"Show me the top 10 rows"`
**Expected**: First 10 rows of data

#### Test 5.3: Missing Values Query
**Query**: `"What columns have missing values?"`
**Expected**: List of columns with nulls

#### Test 5.4: Summary Request
**Query**: `"Create a summary of all numeric columns"`
**Expected**: Summary statistics

#### Test 5.5: Relationship Query
**Query**: `"What is the relationship between Quantity and TotalAmount?"`
**Expected**: Analysis of relationship

---

## 🎯 Comprehensive Test Scenarios

### Scenario 1: Business Analysis
**Queries**:
1. `"Group by OrderStatus, calculate count and average TotalAmount"`
2. `"Show top 5 payment methods by total revenue"`
3. `"Filter where OrderStatus == 'Delivered', group by PaymentMethod, calculate sum of TotalAmount"`

### Scenario 2: Product Analysis
**Queries**:
1. `"Group by ProductID, calculate sum of Quantity and average UnitPrice"`
2. `"Order by Quantity desc limit 10"`
3. `"Filter where Quantity > 5, group by ProductID, calculate total revenue"`

### Scenario 3: Customer Analysis
**Queries**:
1. `"Group by CustomerID, calculate count of orders and sum of TotalAmount"`
2. `"Show top 10 customers by total spending"`
3. `"Filter where TotalAmount > 1000, group by CustomerID"`

### Scenario 4: Time-Based Analysis
**Queries**:
1. `"Group by OrderDate, calculate sum of TotalAmount"`
2. `"Order by OrderDate desc limit 20"`
3. `"Filter where OrderDate contains '2025-01', calculate average TotalAmount"`

### Scenario 5: Status Analysis
**Queries**:
1. `"Group by OrderStatus, calculate count, average TotalAmount, and sum of TotalAmount"`
2. `"Filter where OrderStatus == 'Processing', order by TotalAmount desc"`
3. `"Show distribution of orders by status"`

---

## 📋 Expected Results Checklist

### Data Quality Summary Should Show:
- ✅ All columns with their data types
- ✅ Null counts and percentages
- ✅ Unique value counts
- ✅ Duplicate counts
- ✅ Completeness percentages
- ✅ Summary metrics (Total Nulls, Total Duplicates, Avg Completeness)

### SQL-Like Operations Should Work:
- ✅ ORDER BY (ascending/descending)
- ✅ GROUP BY (single/multiple columns)
- ✅ WHERE (single/multiple conditions)
- ✅ LIMIT/TOP/FIRST
- ✅ Complex multi-step queries

### Statistical Analysis Should Provide:
- ✅ Descriptive statistics
- ✅ Distribution analysis
- ✅ Hypothesis testing
- ✅ Percentiles
- ✅ All in table format

### Visualizations Should Create:
- ✅ Histograms
- ✅ Scatter plots
- ✅ Correlation heatmaps
- ✅ Bar charts
- ✅ Box plots
- ✅ Line plots
- ✅ Pair plots

### Feature Relationships Should Show:
- ✅ Correlation matrices
- ✅ Feature relationship tables
- ✅ Feature importance rankings
- ✅ All in table format

---

## 🚀 How to Run Tests

1. **Upload the file**: Use sidebar to upload `mock_order_data_analysis.csv`
2. **Check Data Quality**: Verify the automatic data quality summary appears
3. **Test Each Tab**: Go through each tab and run the test queries
4. **Verify Results**: Check that results are in table format when applicable
5. **Test Complex Queries**: Try multi-step SQL-like queries

---

## 📝 Notes

- All queries should return results in table format when possible
- Natural language queries should be understood and executed correctly
- SQL-like operations should work seamlessly
- Visualizations should render properly
- Data quality summary should appear automatically

---

**Test File Location**: `~/Downloads/mock_order_data_analysis.csv`
**Application**: http://localhost:8501



