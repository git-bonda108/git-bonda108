# ⚡ Quick Test Reference for mock_order_data_analysis.csv

## 🚀 Quick Start

1. **Upload File**: Use sidebar → Upload `~/Downloads/mock_order_data_analysis.csv`
2. **Check Data Quality**: Automatically shown - should show 0 nulls, 100% completeness
3. **Test Each Tab**: Use queries below

---

## 📋 Essential Test Queries

### 🔍 Data Analysis Tab (Most Important)

#### ORDER BY Tests
```
"Order by TotalAmount desc limit 10"
"Order by Quantity asc limit 20"
"Sort by UnitPrice descending"
```

#### GROUP BY Tests
```
"Group by OrderStatus"
"Group by PaymentMethod calculate average TotalAmount"
"Group by ProductID, calculate sum of Quantity and average UnitPrice"
```

#### WHERE Tests
```
"Filter where TotalAmount > 2000"
"Filter where OrderStatus == 'Delivered'"
"Filter where Quantity > 5 AND TotalAmount > 1000"
```

#### Complex Queries
```
"Group by PaymentMethod, calculate sum of TotalAmount, order by sum desc, limit 3"
"Filter where TotalAmount > 500, group by OrderStatus, calculate average TotalAmount"
"Group by ProductID, calculate sum of Quantity, order by sum desc limit 5"
```

### 📊 Statistics Tab
```
"Calculate comprehensive statistics for all numeric columns"
"Analyze the distribution of TotalAmount column"
"Show mean and median for Quantity column"
```

### 📈 Visualizations Tab
```
"Create a histogram of TotalAmount column"
"Create a scatter plot of Quantity vs TotalAmount"
"Create a correlation heatmap"
"Create a bar chart of OrderStatus column"
```

### 🔗 Feature Relationships Tab
```
"Show correlations between all numeric features"
"Analyze relationships between all feature pairs"
"Calculate feature importance for TotalAmount column"
```

### 💬 AI Chat Tab
```
"What are the main insights from this dataset?"
"Which payment method has the highest average order value?"
"Show me the top 10 highest total amounts"
"What is the relationship between Quantity and TotalAmount?"
```

---

## ✅ Verification Checklist

After uploading, verify:
- [ ] Data Quality Summary shows 0 nulls
- [ ] All 12 columns visible
- [ ] 500 rows loaded
- [ ] ORDER BY works
- [ ] GROUP BY works
- [ ] WHERE conditions work
- [ ] Visualizations render
- [ ] Statistics calculate correctly

---

## 📊 Expected Dataset Stats

- **Rows**: 500
- **Columns**: 12
- **Numeric**: Quantity, UnitPrice, TotalAmount
- **Mean TotalAmount**: ~1362.58
- **Mean Quantity**: ~5.43
- **OrderStatus**: Delivered, Processing, Shipped
- **PaymentMethod**: PayPal, Bank Transfer, Debit Card, Credit Card

---

## 🎯 Top 10 Test Queries to Run

1. `"Order by TotalAmount desc limit 10"` - Top orders
2. `"Group by OrderStatus calculate average TotalAmount"` - Status analysis
3. `"Filter where TotalAmount > 2000"` - High-value orders
4. `"Group by PaymentMethod, calculate sum of TotalAmount, order by sum desc"` - Payment analysis
5. `"Create a scatter plot of Quantity vs TotalAmount"` - Visualization
6. `"Show correlations between all numeric features"` - Relationships
7. `"Group by ProductID, calculate sum of Quantity"` - Product analysis
8. `"Filter where OrderStatus == 'Delivered' AND TotalAmount > 1000"` - Multi-condition
9. `"What are the main insights from this dataset?"` - AI analysis
10. `"Create a correlation heatmap"` - Visual correlation

---

**File Location**: `~/Downloads/mock_order_data_analysis.csv`
**Application**: http://localhost:8501



