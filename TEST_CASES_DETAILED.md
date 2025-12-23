# 🧪 Detailed Test Cases for mock_order_data_analysis.csv

## 📊 Dataset Information
- **File**: `~/Downloads/mock_order_data_analysis.csv`
- **Rows**: 500
- **Columns**: 12
- **Numeric Columns**: Quantity, UnitPrice, TotalAmount
- **Categorical Columns**: OrderID, OrderDate, CustomerID, ProductID, OrderStatus, PaymentMethod, ShippingAddress, CreatedDateTime, ModifiedDateTime
- **Missing Values**: None (clean dataset)

---

## ✅ Test Cases by Tab

### 📊 TAB 1: Statistics

#### Test Case 1.1: Basic Statistics
**Action**: Click "📊 Summary Stats" button OR query: `"Calculate comprehensive statistics for all numeric columns"`
**Expected Result**: 
- Table showing statistics for Quantity, UnitPrice, TotalAmount
- Columns: count, mean, median, std, min, max, q25, q75, skewness, kurtosis
- Mean TotalAmount should be around 1362.58
- Mean Quantity should be around 5.43

#### Test Case 1.2: Distribution Analysis
**Query**: `"Analyze the distribution of TotalAmount column"`
**Expected Result**:
- Distribution type (Normal/Skewed)
- Skewness and kurtosis values
- Percentiles (25th, 50th, 75th, 90th, 95th, 99th)
- IQR and range

#### Test Case 1.3: Hypothesis Testing
**Query**: `"Perform hypothesis test on TotalAmount column"`
**Expected Result**:
- T-test results
- P-value
- Significance indicator
- Mean comparison

#### Test Case 1.4: Percentiles
**Action**: Click "📉 Percentiles" button
**Expected Result**:
- Percentile table for all numeric columns
- 25th, 50th, 75th, 90th, 95th, 99th percentiles

---

### 🔍 TAB 2: Data Analysis

#### Test Case 2.1: ORDER BY - Descending
**Query**: `"Order by TotalAmount desc limit 10"`
**Expected Result**:
- Table with 10 rows
- Highest TotalAmount values first
- Should show orders with TotalAmount around 4000-5000

#### Test Case 2.2: ORDER BY - Ascending
**Query**: `"Order by TotalAmount asc limit 10"`
**Expected Result**:
- Table with 10 rows
- Lowest TotalAmount values first
- Should show orders with TotalAmount around 12-400

#### Test Case 2.3: GROUP BY - Simple Count
**Query**: `"Group by OrderStatus"`
**Expected Result**:
- Table showing count per OrderStatus
- Should show: Delivered, Processing, Shipped, (possibly others)
- Counts should sum to 500

#### Test Case 2.4: GROUP BY with Average
**Query**: `"Group by OrderStatus calculate average TotalAmount"`
**Expected Result**:
- Table with OrderStatus and average TotalAmount
- Average should be calculated correctly per status

#### Test Case 2.5: GROUP BY with Sum
**Query**: `"Group by PaymentMethod, calculate sum of TotalAmount"`
**Expected Result**:
- Table with PaymentMethod and sum of TotalAmount
- Should show: PayPal, Bank Transfer, Debit Card, Credit Card
- Sums should be reasonable (total should be around 681,288)

#### Test Case 2.6: WHERE - Numeric Greater Than
**Query**: `"Filter where TotalAmount > 2000"`
**Expected Result**:
- Filtered dataframe
- All rows with TotalAmount > 2000
- Should be less than 500 rows

#### Test Case 2.7: WHERE - Numeric Less Than
**Query**: `"Filter where Quantity < 3"`
**Expected Result**:
- Filtered dataframe
- All rows with Quantity < 3
- Should show orders with Quantity 1 or 2

#### Test Case 2.8: WHERE - Categorical Equal
**Query**: `"Filter where OrderStatus == 'Delivered'"`
**Expected Result**:
- Filtered dataframe
- Only Delivered orders
- Should show multiple rows

#### Test Case 2.9: WHERE - Multiple Conditions AND
**Query**: `"Filter where TotalAmount > 1000 AND Quantity > 5"`
**Expected Result**:
- Filtered dataframe
- Orders meeting both conditions
- Should be subset of data

#### Test Case 2.10: WHERE - Multiple Conditions OR
**Query**: `"Filter where OrderStatus == 'Delivered' OR OrderStatus == 'Shipped'"`
**Expected Result**:
- Filtered dataframe
- Orders that are Delivered OR Shipped
- Should be more rows than single condition

#### Test Case 2.11: Complex - GROUP BY + ORDER BY + LIMIT
**Query**: `"Group by PaymentMethod, calculate average TotalAmount, order by average desc, limit 3"`
**Expected Result**:
- Table with top 3 PaymentMethods
- Sorted by average TotalAmount descending
- Should show highest average payment methods first

#### Test Case 2.12: Complex - WHERE + GROUP BY + ORDER BY
**Query**: `"Filter where TotalAmount > 500, group by OrderStatus, calculate sum of TotalAmount, order by sum desc"`
**Expected Result**:
- Filtered and grouped data
- Sum of TotalAmount per OrderStatus (filtered)
- Sorted by sum descending

#### Test Case 2.13: Natural Language - Top Orders
**Query**: `"Show me the top 10 highest total amounts"`
**Expected Result**:
- Top 10 orders by TotalAmount
- Should match "Order by TotalAmount desc limit 10"

#### Test Case 2.14: Natural Language - Average by Group
**Query**: `"What is the average order amount by payment method?"`
**Expected Result**:
- Average TotalAmount per PaymentMethod
- Should match GROUP BY with average

#### Test Case 2.15: Data Quality Button
**Action**: Click "🔍 Data Quality" button
**Expected Result**:
- Data quality summary table
- All 12 columns with quality metrics
- Should show 100% completeness (no nulls)

#### Test Case 2.16: Missing Values Button
**Action**: Click "🔢 Missing Values" button
**Expected Result**:
- Table showing columns with missing values
- Should be empty (no missing values in this dataset)
- Or show "No missing values" message

---

### 📈 TAB 3: Visualizations

#### Test Case 3.1: Histogram
**Query**: `"Create a histogram of TotalAmount column"`
**Expected Result**:
- Histogram chart displayed
- Shows distribution of TotalAmount
- Bins showing frequency

#### Test Case 3.2: Scatter Plot
**Query**: `"Create a scatter plot of Quantity vs TotalAmount"`
**Expected Result**:
- Scatter plot displayed
- Quantity on x-axis, TotalAmount on y-axis
- Shows relationship between variables

#### Test Case 3.3: Correlation Heatmap
**Query**: `"Create a correlation heatmap"` OR Click "🔥 Heatmap" button
**Expected Result**:
- Correlation heatmap displayed
- Shows correlations between Quantity, UnitPrice, TotalAmount
- Color-coded correlation values

#### Test Case 3.4: Bar Chart
**Query**: `"Create a bar chart of OrderStatus column"`
**Expected Result**:
- Bar chart displayed
- Shows count per OrderStatus
- Bars for each status category

#### Test Case 3.5: Box Plot
**Query**: `"Create a box plot of TotalAmount column"`
**Expected Result**:
- Box plot displayed
- Shows distribution, quartiles, outliers
- Whiskers showing range

#### Test Case 3.6: Line Plot
**Query**: `"Create a line plot of Quantity vs TotalAmount"`
**Expected Result**:
- Line plot displayed
- Shows trend/relationship
- Connected data points

#### Test Case 3.7: Pair Plot
**Query**: `"Create a pair plot for Quantity, UnitPrice, TotalAmount"`
**Expected Result**:
- Pair plot matrix displayed
- Shows relationships between all three variables
- Multiple subplots

---

### 🔗 TAB 4: Feature Relationships

#### Test Case 4.1: Correlation Analysis
**Query**: `"Show correlations between all numeric features"` OR Click "🔗 Correlations" button
**Expected Result**:
- Correlation table
- Correlations between Quantity, UnitPrice, TotalAmount
- Should show strong correlation between UnitPrice*Quantity and TotalAmount

#### Test Case 4.2: Feature Relationships
**Query**: `"Analyze relationships between all feature pairs"` OR Click "📊 Feature Relationships" button
**Expected Result**:
- Feature relationship table
- Shows relationships between numeric columns
- Correlation strength indicators

#### Test Case 4.3: Correlation Heatmap
**Action**: Click "🔥 Correlation Heatmap" button
**Expected Result**:
- Visual correlation heatmap
- Color-coded correlation matrix

#### Test Case 4.4: Feature Importance
**Query**: `"Calculate feature importance for TotalAmount column"`
**Expected Result**:
- Feature importance table
- Quantity and UnitPrice ranked by correlation with TotalAmount
- Should show UnitPrice as highly important

---

### 💬 TAB 5: AI Chat

#### Test Case 5.1: General Insights
**Query**: `"What are the main insights from this dataset?"`
**Expected Result**:
- Comprehensive insights about the order data
- Key findings and patterns
- Data summary

#### Test Case 5.2: Top Rows
**Query**: `"Show me the top 10 rows"`
**Expected Result**:
- First 10 rows of the dataset
- All columns displayed

#### Test Case 5.3: Missing Values Query
**Query**: `"What columns have missing values?"`
**Expected Result**:
- Response indicating no missing values
- Or list of columns with nulls if any

#### Test Case 5.4: Summary Request
**Query**: `"Create a summary of all numeric columns"`
**Expected Result**:
- Summary statistics table
- Mean, median, std for Quantity, UnitPrice, TotalAmount

#### Test Case 5.5: Relationship Query
**Query**: `"What is the relationship between Quantity and TotalAmount?"`
**Expected Result**:
- Analysis of relationship
- Correlation value
- Interpretation of relationship

#### Test Case 5.6: Business Question
**Query**: `"Which payment method has the highest average order value?"`
**Expected Result**:
- PaymentMethod with highest average TotalAmount
- Should use GROUP BY and ORDER BY operations

#### Test Case 5.7: Complex Business Question
**Query**: `"Show me the top 5 products by total revenue"`
**Expected Result**:
- Top 5 ProductID by sum of TotalAmount
- Should use GROUP BY, aggregation, and ORDER BY

---

## 🎯 Business Scenario Tests

### Scenario A: Sales Analysis
**Test Queries**:
1. `"Group by OrderStatus, calculate count and average TotalAmount"`
   - Expected: Count and average per status
   
2. `"Show top 10 orders by total amount"`
   - Expected: Top 10 orders sorted by TotalAmount desc

3. `"Filter where OrderStatus == 'Delivered', group by PaymentMethod, calculate sum of TotalAmount"`
   - Expected: Revenue by payment method for delivered orders

### Scenario B: Product Analysis
**Test Queries**:
1. `"Group by ProductID, calculate sum of Quantity and average UnitPrice"`
   - Expected: Product performance metrics

2. `"Order by Quantity desc limit 10"`
   - Expected: Top 10 orders by quantity

3. `"Filter where Quantity > 8, group by ProductID, calculate total revenue"`
   - Expected: High-quantity product revenue

### Scenario C: Customer Analysis
**Test Queries**:
1. `"Group by CustomerID, calculate count of orders and sum of TotalAmount"`
   - Expected: Customer purchase summary

2. `"Show top 10 customers by total spending"`
   - Expected: Top customers by TotalAmount sum

3. `"Filter where TotalAmount > 2000, group by CustomerID"`
   - Expected: High-value customers

### Scenario D: Payment Analysis
**Test Queries**:
1. `"Group by PaymentMethod, calculate count, average, and sum of TotalAmount"`
   - Expected: Comprehensive payment method analysis

2. `"Filter where PaymentMethod == 'Credit Card', order by TotalAmount desc"`
   - Expected: Credit card orders sorted

3. `"Group by PaymentMethod, calculate average TotalAmount, order by average desc"`
   - Expected: Payment methods ranked by average order value

---

## ✅ Verification Checklist

### Data Quality Summary
- [ ] Shows all 12 columns
- [ ] Shows 0 nulls for all columns (100% completeness)
- [ ] Shows correct data types
- [ ] Shows unique value counts
- [ ] Summary metrics display correctly

### SQL-Like Operations
- [ ] ORDER BY works (asc/desc)
- [ ] GROUP BY works
- [ ] WHERE conditions work (>, <, ==, !=)
- [ ] LIMIT works
- [ ] Multiple WHERE conditions work (AND/OR)
- [ ] Complex multi-step queries work

### Statistical Analysis
- [ ] Statistics calculated correctly
- [ ] Distribution analysis works
- [ ] Hypothesis testing works
- [ ] Percentiles displayed

### Visualizations
- [ ] Histogram renders
- [ ] Scatter plot renders
- [ ] Heatmap renders
- [ ] Bar chart renders
- [ ] Box plot renders
- [ ] Line plot renders
- [ ] Pair plot renders

### Feature Relationships
- [ ] Correlations calculated
- [ ] Feature relationships shown
- [ ] Feature importance calculated
- [ ] All results in table format

### Natural Language Queries
- [ ] Simple queries work
- [ ] Complex queries work
- [ ] SQL-like queries work
- [ ] Mixed queries work

---

## 📝 Expected Values (for verification)

Based on dataset analysis:
- **Total Rows**: 500
- **Mean TotalAmount**: ~1362.58
- **Mean Quantity**: ~5.43
- **Mean UnitPrice**: ~250.55
- **Max TotalAmount**: ~4965.50
- **Min TotalAmount**: ~12.27
- **OrderStatus values**: Delivered, Processing, Shipped, (possibly others)
- **PaymentMethod values**: PayPal, Bank Transfer, Debit Card, Credit Card
- **ProductID count**: 20 unique products
- **CustomerID count**: 50 unique customers

---

## 🚀 Running the Tests

1. **Start the application**: `streamlit run data-insights.py`
2. **Upload the file**: Use sidebar to upload `~/Downloads/mock_order_data_analysis.csv`
3. **Verify Data Quality**: Check that summary shows 0 nulls, 100% completeness
4. **Test each tab**: Go through all 5 tabs systematically
5. **Run test queries**: Use the queries listed above
6. **Verify results**: Check that results match expected outcomes

---

**Test File**: `~/Downloads/mock_order_data_analysis.csv`
**Application**: http://localhost:8501
**Total Test Cases**: 50+



