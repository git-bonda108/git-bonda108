"""
Automated Test Script for mock_order_data_analysis.csv
Tests all functionalities of the Multi-Agent Data Analysis System
"""
import pandas as pd
import sys
import os
sys.path.insert(0, '.')

from tools import data_tools, statistical_tools, formatting_tools

# Load test data
test_file = os.path.expanduser('~/Downloads/mock_order_data_analysis.csv')
if not os.path.exists(test_file):
    print(f"❌ Test file not found: {test_file}")
    sys.exit(1)

df = pd.read_csv(test_file)
print("=" * 70)
print("🧪 COMPREHENSIVE TEST SUITE FOR mock_order_data_analysis.csv")
print("=" * 70)

test_results = {'passed': 0, 'failed': 0}

def test(name, func, *args, **kwargs):
    """Run a test and track results"""
    try:
        result = func(*args, **kwargs)
        print(f"✅ PASS: {name}")
        test_results['passed'] += 1
        return True, result
    except Exception as e:
        print(f"❌ FAIL: {name}")
        print(f"   Error: {str(e)}")
        test_results['failed'] += 1
        return False, None

print("\n📊 TEST 1: Data Quality Summary")
print("-" * 70)
test("Data Quality Summary", data_tools.get_data_quality_summary, df)

print("\n🔍 TEST 2: SQL-Like Operations")
print("-" * 70)

# ORDER BY tests
test("ORDER BY desc", data_tools.execute_complex_query, df, "order by TotalAmount desc")
test("ORDER BY asc", data_tools.execute_complex_query, df, "order by TotalAmount asc")
test("ORDER BY with LIMIT", data_tools.execute_complex_query, df, "order by TotalAmount desc limit 10")

# WHERE tests
test("WHERE > condition", data_tools.execute_complex_query, df, "where TotalAmount > 1000")
test("WHERE < condition", data_tools.execute_complex_query, df, "where Quantity < 5")

# GROUP BY tests
test("GROUP BY", data_tools.execute_complex_query, df, "group by OrderStatus")

# Complex queries
test("ORDER BY + LIMIT", data_tools.execute_complex_query, df, "order by TotalAmount desc limit 5")
test("WHERE + ORDER BY", data_tools.execute_complex_query, df, "where TotalAmount > 1000 order by TotalAmount desc")

print("\n🔗 TEST 3: Multi-Condition Filtering")
print("-" * 70)
conditions = [
    {'column': 'TotalAmount', 'operator': '>', 'value': 1000},
    {'column': 'Quantity', 'operator': '>', 'value': 5}
]
test("Multi-filter AND", data_tools.multi_condition_filter, df, conditions, 'AND')
test("Multi-filter OR", data_tools.multi_condition_filter, df, conditions, 'OR')

print("\n📊 TEST 4: Advanced Grouping")
print("-" * 70)
agg_dict = {'TotalAmount': 'mean', 'Quantity': 'sum'}
test("Advanced GROUP BY", data_tools.advanced_group_by, df, 'OrderStatus', agg_dict)

print("\n📈 TEST 5: Statistical Analysis")
print("-" * 70)
test("Calculate Statistics", statistical_tools.calculate_statistics, df)
test("Analyze Correlations", statistical_tools.analyze_correlations, df)
test("Feature Relationships", statistical_tools.feature_relationships, df)
test("Distribution Analysis", statistical_tools.distribution_analysis, df, 'TotalAmount')
test("Feature Importance", statistical_tools.feature_importance, df, 'TotalAmount')

print("\n📋 TEST 6: Data Info")
print("-" * 70)
test("Get Data Info", data_tools.get_data_info, df)

print("\n" + "=" * 70)
print(f"📊 TEST RESULTS: {test_results['passed']} passed, {test_results['failed']} failed")
print("=" * 70)

if test_results['failed'] == 0:
    print("✅ ALL TESTS PASSED!")
else:
    print(f"⚠️  {test_results['failed']} test(s) failed")



