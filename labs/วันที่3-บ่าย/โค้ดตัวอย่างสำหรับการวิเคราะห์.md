# โค้ดตัวอย่างสำหรับการวิเคราะห์ข้อมูลกรณีศึกษา

เอกสารนี้รวบรวมโค้ด Python ตัวอย่างสำหรับการวิเคราะห์ข้อมูลในกรณีศึกษา TechRetail ที่ผู้เรียนสามารถนำไปปรับใช้และต่อยอดในการทำงานกับข้อมูลจริงได้

## 1. การนำเข้าข้อมูลและการเตรียมข้อมูล

```python
# นำเข้า libraries ที่จำเป็น
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
%matplotlib inline

# กำหนดรูปแบบการแสดงผลกราฟ
plt.style.use('seaborn-whitegrid')
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# นำเข้าข้อมูล
sales_df = pd.read_csv('sales_data.csv')
product_df = pd.read_csv('product_data.csv')
store_df = pd.read_csv('store_data.csv')
customer_df = pd.read_csv('customer_data.csv')
marketing_df = pd.read_csv('marketing_data.csv')

# แปลงคอลัมน์วันที่เป็น datetime format
sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])
marketing_df['campaign_start'] = pd.to_datetime(marketing_df['campaign_start'])
marketing_df['campaign_end'] = pd.to_datetime(marketing_df['campaign_end'])

# ตรวจสอบข้อมูลที่ขาดหาย
print("Missing values in each dataframe:")
print("Sales data:")
print(sales_df.isnull().sum())
print("\nProduct data:")
print(product_df.isnull().sum())
print("\nStore data:")
print(store_df.isnull().sum())
print("\nCustomer data:")
print(customer_df.isnull().sum())
print("\nMarketing data:")
print(marketing_df.isnull().sum())

# จัดการกับข้อมูลที่ขาดหาย (ตัวอย่าง)
sales_df = sales_df.dropna(subset=['sale_amount', 'product_id', 'store_id'])
product_df['description'] = product_df['description'].fillna('No description')

# เพิ่มคอลัมน์ที่จำเป็นสำหรับการวิเคราะห์
sales_df['year'] = sales_df['sale_date'].dt.year
sales_df['month'] = sales_df['sale_date'].dt.month
sales_df['quarter'] = sales_df['sale_date'].dt.quarter
sales_df['day'] = sales_df['sale_date'].dt.day
sales_df['weekday'] = sales_df['sale_date'].dt.weekday
sales_df['weekend'] = sales_df['weekday'].apply(lambda x: 1 if x >= 5 else 0)

# รวมข้อมูลขายกับข้อมูลสินค้าเพื่อคำนวณกำไร
sales_with_product = pd.merge(sales_df, product_df, on='product_id', how='left')
sales_with_product['profit'] = sales_with_product['sale_amount'] - (sales_with_product['quantity'] * sales_with_product['cost_price'])
sales_with_product['profit_margin'] = sales_with_product['profit'] / sales_with_product['sale_amount']

# รวมข้อมูลขายกับข้อมูลสาขา
sales_with_store = pd.merge(sales_with_product, store_df, on='store_id', how='left')

# ตรวจสอบข้อมูลที่รวมแล้ว
print("\nCombined data sample:")
print(sales_with_store.head())
print("\nCombined data info:")
print(sales_with_store.info())
print("\nBasic statistics:")
print(sales_with_store[['sale_amount', 'quantity', 'profit', 'profit_margin']].describe())
```

## 2. การวิเคราะห์แนวโน้มยอดขายและกำไร

```python
# วิเคราะห์แนวโน้มยอดขายรายเดือน
monthly_sales = sales_with_product.groupby([sales_with_product['sale_date'].dt.year, sales_with_product['sale_date'].dt.month]).agg({
    'sale_amount': 'sum',
    'profit': 'sum',
    'sale_id': 'count'
}).reset_index()

monthly_sales.columns = ['year', 'month', 'total_sales', 'total_profit', 'transaction_count']
monthly_sales['profit_margin'] = monthly_sales['total_profit'] / monthly_sales['total_sales']
monthly_sales['year_month'] = monthly_sales['year'].astype(str) + '-' + monthly_sales['month'].astype(str).str.zfill(2)
monthly_sales['avg_transaction_value'] = monthly_sales['total_sales'] / monthly_sales['transaction_count']

# สร้างกราฟแนวโน้มยอดขายและกำไรรายเดือน
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.plot(monthly_sales['year_month'], monthly_sales['total_sales'], marker='o', linewidth=2, color='blue')
plt.title('Monthly Sales Trend')
plt.xlabel('Year-Month')
plt.ylabel('Total Sales Amount')
plt.xticks(rotation=45)
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(monthly_sales['year_month'], monthly_sales['profit_margin'], marker='s', linewidth=2, color='green')
plt.title('Monthly Profit Margin Trend')
plt.xlabel('Year-Month')
plt.ylabel('Profit Margin')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# วิเคราะห์การเปลี่ยนแปลงเทียบกับปีก่อน (YoY comparison)
# สำหรับ 12 เดือนล่าสุด
last_12_months = monthly_sales.sort_values(['year', 'month'], ascending=False).head(12)
previous_12_months = monthly_sales.sort_values(['year', 'month'], ascending=False).iloc[12:24]

# รวมข้อมูลเพื่อเปรียบเทียบ
yoy_comparison = pd.DataFrame({
    'period': last_12_months['year_month'].values,
    'current_sales': last_12_months['total_sales'].values,
    'previous_sales': previous_12_months['total_sales'].values[::-1],
    'current_profit': last_12_months['total_profit'].values,
    'previous_profit': previous_12_months['total_profit'].values[::-1]
})

yoy_comparison['sales_yoy_change'] = (yoy_comparison['current_sales'] - yoy_comparison['previous_sales']) / yoy_comparison['previous_sales'] * 100
yoy_comparison['profit_yoy_change'] = (yoy_comparison['current_profit'] - yoy_comparison['previous_profit']) / yoy_comparison['previous_profit'] * 100

# แสดงกราฟเปรียบเทียบ YoY
plt.figure(figsize=(14, 6))
bar_width = 0.35
index = np.arange(len(yoy_comparison))

plt.bar(index, yoy_comparison['sales_yoy_change'], bar_width, label='Sales YoY Change (%)', color='blue')
plt.bar(index + bar_width, yoy_comparison['profit_yoy_change'], bar_width, label='Profit YoY Change (%)', color='green')

plt.title('Year-over-Year Changes in Sales and Profit')
plt.xlabel('Period')
plt.ylabel('Change (%)')
plt.xticks(index + bar_width / 2, yoy_comparison['period'], rotation=45)
plt.legend()
plt.axhline(y=0, color='r', linestyle='-', alpha=0.3)
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()

# วิเคราะห์แนวโน้มตามฤดูกาล (วันในสัปดาห์, เดือนในปี)
# วันในสัปดาห์
weekday_sales = sales_with_product.groupby('weekday').agg({
    'sale_amount': 'sum',
    'profit': 'sum',
    'sale_id': 'count'
}).reset_index()

weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_sales['weekday_name'] = weekday_sales['weekday'].apply(lambda x: weekday_names[x])
weekday_sales['avg_transaction_value'] = weekday_sales['sale_amount'] / weekday_sales['sale_id']

plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.bar(weekday_sales['weekday_name'], weekday_sales['sale_amount'], color='blue')
plt.title('Sales by Day of Week')
plt.xlabel('Day')
plt.ylabel('Total Sales')
plt.grid(True, axis='y')

plt.subplot(1, 2, 2)
plt.bar(weekday_sales['weekday_name'], weekday_sales['avg_transaction_value'], color='green')
plt.title('Average Transaction Value by Day of Week')
plt.xlabel('Day')
plt.ylabel('Avg Transaction Value')
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()
```

## 3. การวิเคราะห์หมวดหมู่สินค้าและประสิทธิภาพสินค้า

```python
# วิเคราะห์ยอดขายและกำไรตามหมวดหมู่สินค้า
category_performance = sales_with_product.groupby('category').agg({
    'sale_amount': 'sum',
    'profit': 'sum',
    'sale_id': 'count',
    'product_id': 'nunique'
}).reset_index()

category_performance.columns = ['category', 'total_sales', 'total_profit', 'transaction_count', 'product_count']
category_performance['profit_margin'] = category_performance['total_profit'] / category_performance['total_sales']
category_performance['avg_transaction_value'] = category_performance['total_sales'] / category_performance['transaction_count']
category_performance['sales_per_product'] = category_performance['total_sales'] / category_performance['product_count']

# จัดเรียงตามยอดขาย
category_performance_by_sales = category_performance.sort_values('total_sales', ascending=False)

# สร้างกราฟยอดขายตามหมวดหมู่
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
sns.barplot(x='category', y='total_sales', data=category_performance_by_sales, palette='viridis')
plt.title('Sales by Product Category')
plt.xlabel('Category')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.grid(True, axis='y')

plt.subplot(1, 2, 2)
sns.barplot(x='category', y='profit_margin', data=category_performance_by_sales, palette='viridis')
plt.title('Profit Margin by Product Category')
plt.xlabel('Category')
plt.ylabel('Profit Margin')
plt.xticks(rotation=45)
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()

# สร้าง heatmap เปรียบเทียบยอดขายและกำไรของแต่ละหมวดหมู่
plt.figure(figsize=(10, 8))
category_pivot = category_performance.pivot_table(
    index='category',
    values=['total_sales', 'total_profit', 'profit_margin', 'avg_transaction_value'],
    aggfunc='sum'
)

# Normalize the data for heatmap
category_pivot_norm = (category_pivot - category_pivot.mean()) / category_pivot.std()
sns.heatmap(category_pivot_norm, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Normalized Performance Metrics by Category')
plt.tight_layout()
plt.show()

# วิเคราะห์สินค้าขายดีและขายไม่ดี
product_performance = sales_with_product.groupby(['product_id', 'product_name', 'category']).agg({
    'sale_amount': 'sum',
    'profit': 'sum',
    'quantity': 'sum',
    'sale_id': 'count'
}).reset_index()

product_performance['profit_margin'] = product_performance['profit'] / product_performance['sale_amount']
product_performance['avg_price_per_unit'] = product_performance['sale_amount'] / product_performance['quantity']
product_performance['avg_quantity_per_transaction'] = product_performance['quantity'] / product_performance['sale_id']

# สินค้าขายดีที่สุด 10 อันดับแรกตามยอดขาย
top10_by_sales = product_performance.sort_values('sale_amount', ascending=False).head(10)
# สินค้าที่มีกำไรสูงสุด 10 อันดับแรก
top10_by_profit = product_performance.sort_values('profit', ascending=False).head(10)
# สินค้าที่มีอัตรากำไรสูงสุด 10 อันดับแรก (เฉพาะสินค้าที่มียอดขายเกินค่าเฉลี่ย)
avg_sales = product_performance['sale_amount'].mean()
top10_by_margin = product_performance[product_performance['sale_amount'] > avg_sales].sort_values('profit_margin', ascending=False).head(10)

# สินค้าที่ขายแย่ที่สุด 10 อันดับสุดท้ายตามยอดขาย
bottom10_by_sales = product_performance.sort_values('sale_amount').head(10)
# สินค้าที่มีกำไรต่ำสุด 10 อันดับสุดท้าย
bottom10_by_profit = product_performance.sort_values('profit').head(10)

# แสดงกราฟสินค้าขายดีที่สุด 10 อันดับแรก
plt.figure(figsize=(14, 8))
plt.subplot(2, 1, 1)
sns.barplot(x='product_name', y='sale_amount', data=top10_by_sales, palette='viridis')
plt.title('Top 10 Products by Sales')
plt.xlabel('Product')
plt.ylabel('Total Sales')
plt.xticks(rotation=45, ha='right')
plt.grid(True, axis='y')

plt.subplot(2, 1, 2)
sns.barplot(x='product_name', y='profit_margin', data=top10_by_margin, palette='viridis')
plt.title('Top 10 Products by Profit Margin (with Above Average Sales)')
plt.xlabel('Product')
plt.ylabel('Profit Margin')
plt.xticks(rotation=45, ha='right')
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()

# แสดงกราฟสินค้าที่ขายแย่ที่สุด 10 อันดับสุดท้าย
plt.figure(figsize=(14, 8))
plt.subplot(2, 1, 1)
sns.barplot(x='product_name', y='sale_amount', data=bottom10_by_sales, palette='viridis')
plt.title('Bottom 10 Products by Sales')
plt.xlabel('Product')
plt.ylabel('Total Sales')
plt.xticks(rotation=45, ha='right')
plt.grid(True, axis='y')

plt.subplot(2, 1, 2)
sns.barplot(x='product_name', y='profit', data=bottom10_by_profit, palette='viridis')
plt.title('Bottom 10 Products by Profit')
plt.xlabel('Product')
plt.ylabel('Total Profit')
plt.xticks(rotation=45, ha='right')
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()

# การวิเคราะห์ความสัมพันธ์ระหว่างราคาและยอดขาย (ตัวอย่างสำหรับหมวดหมู่หนึ่ง)
category_sample = "Smartphones"  # เปลี่ยนเป็นหมวดหมู่ที่ต้องการวิเคราะห์
category_products = product_performance[product_performance['category'] == category_sample]

plt.figure(figsize=(10, 6))
plt.scatter(category_products['avg_price_per_unit'], category_products['sale_amount'], 
           alpha=0.7, c=category_products['profit_margin'], cmap='viridis', s=100)
plt.colorbar(label='Profit Margin')
plt.title(f'Price vs Sales Amount for {category_sample} Category')
plt.xlabel('Average Price per Unit')
plt.ylabel('Total Sales Amount')
plt.grid(True)
plt.tight_layout()
plt.show()
```

## 4. การวิเคราะห์ประสิทธิภาพของสาขา

```python
# วิเคราะห์ประสิทธิภาพของสาขา
store_performance = sales_with_store.groupby(['store_id', 'store_name', 'region', 'store_type']).agg({
    'sale_amount': 'sum',
    'profit': 'sum',
    'sale_id': 'count',
    'sale_date': lambda x: (x.max() - x.min()).days + 1  # จำนวนวันที่มีการขาย
}).reset_index()

store_performance.columns = ['store_id', 'store_name', 'region', 'store_type', 'total_sales', 'total_profit', 'transaction_count', 'active_days']
store_performance['profit_margin'] = store_performance['total_profit'] / store_performance['total_sales']
store_performance['avg_transaction_value'] = store_performance['total_sales'] / store_performance['transaction_count']
store_performance['daily_avg_sales'] = store_performance['total_sales'] / store_performance['active_days']
store_performance['daily_avg_transactions'] = store_performance['transaction_count'] / store_performance['active_days']

# สาขาที่มียอดขายสูงสุด 10 อันดับแรก
top10_stores_by_sales = store_performance.sort_values('total_sales', ascending=False).head(10)
# สาขาที่มียอดขายต่ำสุด 10 อันดับสุดท้าย
bottom10_stores_by_sales = store_performance.sort_values('total_sales').head(10)

# สร้างกราฟเปรียบเทียบสาขาที่มียอดขายสูงสุดและต่ำสุด
plt.figure(figsize=(16, 8))
plt.subplot(2, 1, 1)
sns.barplot(x='store_name', y='total_sales', hue='store_type', data=top10_stores_by_sales, palette='viridis')
plt.title('Top 10 Stores by Sales')
plt.xlabel('Store')
plt.ylabel('Total Sales')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Store Type')
plt.grid(True, axis='y')

plt.subplot(2, 1, 2)
sns.barplot(x='store_name', y='total_sales', hue='store_type', data=bottom10_stores_by_sales, palette='viridis')
plt.title('Bottom 10 Stores by Sales')
plt.xlabel('Store')
plt.ylabel('Total Sales')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Store Type')
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()

# วิเคราะห์ประสิทธิภาพตามภูมิภาค
region_performance = store_performance.groupby('region').agg({
    'total_sales': 'sum',
    'total_profit': 'sum',
    'transaction_count': 'sum',
    'store_id': 'count'  # จำนวนสาขาในแต่ละภูมิภาค
}).reset_index()

region_performance.columns = ['region', 'total_sales', 'total_profit', 'transaction_count', 'store_count']
region_performance['profit_margin'] = region_performance['total_profit'] / region_performance['total_sales']
region_performance['sales_per_store'] = region_performance['total_sales'] / region_performance['store_count']
region_performance['transactions_per_store'] = region_performance['transaction_count'] / region_performance['store_count']

# สร้างกราฟประสิทธิภาพตามภูมิภาค
plt.figure(figsize=(16, 12))
plt.subplot(2, 2, 1)
sns.barplot(x='region', y='total_sales', data=region_performance, palette='viridis')
plt.title('Total Sales by Region')
plt.xlabel('Region')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.grid(True, axis='y')

plt.subplot(2, 2, 2)
sns.barplot(x='region', y='profit_margin', data=region_performance, palette='viridis')
plt.title('Profit Margin by Region')
plt.xlabel('Region')
plt.ylabel('Profit Margin')
plt.xticks(rotation=45)
plt.grid(True, axis='y')

plt.subplot(2, 2, 3)
sns.barplot(x='region', y='sales_per_store', data=region_performance, palette='viridis')
plt.title('Sales per Store by Region')
plt.xlabel('Region')
plt.ylabel('Sales per Store')
plt.xticks(rotation=45)
plt.grid(True, axis='y')

plt.subplot(2, 2, 4)
sns.barplot(x='region', y='store_count', data=region_performance, palette='viridis')
plt.title('Store Count by Region')
plt.xlabel('Region')
plt.ylabel('Number of Stores')
plt.xticks(rotation=45)
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()

# วิเคราะห์ประสิทธิภาพตามประเภทสาขา
store_type_performance = store_performance.groupby('store_type').agg({
    'total_sales': 'sum',
    'total_profit': 'sum',
    'transaction_count': 'sum',
    'store_id': 'count'  # จำนวนสาขาในแต่ละประเภท
}).reset_index()

store_type_performance.columns = ['store_type', 'total_sales', 'total_profit', 'transaction_count', 'store_count']
store_type_performance['profit_margin'] = store_type_performance['total_profit'] / store_type_performance['total_sales']
store_type_performance['sales_per_store'] = store_type_performance['total_sales'] / store_type_performance['store_count']
store_type_performance['transactions_per_store'] = store_type_performance['transaction_count'] / store_type_performance['store_count']

# สร้างกราฟประสิทธิภาพตามประเภทสาขา
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
sns.barplot(x='store_type', y='sales_per_store', data=store_type_performance, palette='viridis')
plt.title('Sales per Store by Store Type')
plt.xlabel('Store Type')
plt.ylabel('Sales per Store')
plt.grid(True, axis='y')

plt.subplot(1, 2, 2)
sns.barplot(x='store_type', y='profit_margin', data=store_type_performance, palette='viridis')
plt.title('Profit Margin by Store Type')
plt.xlabel('Store Type')
plt.ylabel('Profit Margin')
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()

# วิเคราะห์ความสัมพันธ์ระหว่างขนาดสาขาและยอดขาย
plt.figure(figsize=(10, 6))
sns.scatterplot(x='daily_avg_transactions', y='daily_avg_sales', 
                hue='store_type', size='profit_margin', sizes=(50, 200),
                data=store_performance, palette='viridis', alpha=0.7)
plt.title('Store Performance Analysis')
plt.xlabel('Daily Average Transactions')
plt.ylabel('Daily Average Sales')
plt.grid(True)
plt.tight_layout()
plt.show()
```

## 5. การวิเคราะห์กลุ่มลูกค้าและพฤติกรรมการซื้อ

```python
# รวมข้อมูลการขายและข้อมูลลูกค้า
sales_with_customer = pd.merge(sales_df, customer_df, on='customer_id', how='left')
sales_with_customer = pd.merge(sales_with_customer, product_df, on='product_id', how='left')

# วิเคราะห์ RFM (Recency, Frequency, Monetary)
# ใช้วันที่ล่าสุดในข้อมูลเป็นปัจจุบัน
today_date = sales_df['sale_date'].max()

# สร้าง customer summary สำหรับ RFM
customer_summary = sales_df.groupby('customer_id').agg({
    'sale_date': lambda x: (today_date - x.max()).days,  # Recency
    'sale_id': 'count',  # Frequency
    'sale_amount': 'sum'  # Monetary
}).reset_index()

customer_summary.columns = ['customer_id', 'recency', 'frequency', 'monetary']

# แบ่งคะแนน R, F, M เป็น 5 ช่วง (1-5)
customer_summary['r_score'] = pd.qcut(customer_summary['recency'], 5, labels=[5, 4, 3, 2, 1])  # ค่าต่ำ = ดี (วันน้อย)
customer_summary['f_score'] = pd.qcut(customer_summary['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])  # ค่าสูง = ดี
customer_summary['m_score'] = pd.qcut(customer_summary['monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])  # ค่าสูง = ดี

# คำนวณคะแนน RFM รวม
customer_summary['rfm_score'] = customer_summary['r_score'].astype(int) + customer_summary['f_score'].astype(int) + customer_summary['m_score'].astype(int)

# แบ่งกลุ่มลูกค้าตามคะแนน RFM
customer_summary['customer_segment'] = pd.qcut(customer_summary['rfm_score'], 3, labels=['Low Value', 'Medium Value', 'High Value'])

# เพิ่มข้อมูลลูกค้าเพิ่มเติม
customer_full = pd.merge(customer_summary, customer_df, on='customer_id', how='left')

# แสดงข้อมูลตัวอย่างของแต่ละกลุ่มลูกค้า
print("Sample data for each customer segment:")
for segment in customer_full['customer_segment'].unique():
    print(f"\n{segment} customers sample:")
    print(customer_full[customer_full['customer_segment'] == segment].head(3))

# วิเคราะห์การกระจายของกลุ่มลูกค้า
segment_distribution = customer_full['customer_segment'].value_counts().reset_index()
segment_distribution.columns = ['segment', 'count']

plt.figure(figsize=(10, 6))
sns.barplot(x='segment', y='count', data=segment_distribution, palette='viridis')
plt.title('Customer Segment Distribution')
plt.xlabel('Segment')
plt.ylabel('Number of Customers')
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()

# วิเคราะห์มูลค่าการซื้อตามกลุ่มลูกค้า
segment_value = customer_full.groupby('customer_segment').agg({
    'monetary': 'sum',
    'customer_id': 'count'
}).reset_index()

segment_value.columns = ['segment', 'total_monetary', 'customer_count']
segment_value['avg_monetary_per_customer'] = segment_value['total_monetary'] / segment_value['customer_count']
segment_value['pct_total_monetary'] = segment_value['total_monetary'] / segment_value['total_monetary'].sum() * 100

plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
sns.barplot(x='segment', y='total_monetary', data=segment_value, palette='viridis')
plt.title('Total Monetary Value by Segment')
plt.xlabel('Segment')
plt.ylabel('Total Monetary Value')
plt.grid(True, axis='y')

plt.subplot(1, 2, 2)
plt.pie(segment_value['total_monetary'], labels=segment_value['segment'], autopct='%1.1f%%', 
        startangle=90, shadow=True, colors=sns.color_palette('viridis', 3))
plt.title('Percentage of Total Monetary Value by Segment')
plt.axis('equal')
plt.tight_layout()
plt.show()

# วิเคราะห์พฤติกรรมการซื้อตามกลุ่มลูกค้าและหมวดหมู่สินค้า
segment_category = sales_with_customer.groupby(['customer_segment', 'category']).agg({
    'sale_amount': 'sum',
    'sale_id': 'count'
}).reset_index()

segment_category.columns = ['customer_segment', 'category', 'total_sales', 'transaction_count']
segment_category['avg_transaction_value'] = segment_category['total_sales'] / segment_category['transaction_count']

# Pivot the data for visualization
segment_category_pivot = segment_category.pivot(index='category', columns='customer_segment', values='total_sales')
segment_category_pivot = segment_category_pivot.fillna(0)

# สร้างกราฟเปรียบเทียบหมวดหมู่สินค้าตามกลุ่มลูกค้า
plt.figure(figsize=(12, 8))
segment_category_pivot.plot(kind='bar', colormap='viridis')
plt.title('Category Sales by Customer Segment')
plt.xlabel('Category')
plt.ylabel('Total Sales')
plt.legend(title='Customer Segment')
plt.grid(True, axis='y')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# วิเคราะห์ช่วงเวลาการซื้อตามกลุ่มลูกค้า
segment_time = sales_with_customer.groupby(['customer_segment', 'weekday']).agg({
    'sale_amount': 'sum',
    'sale_id': 'count'
}).reset_index()

segment_time.columns = ['customer_segment', 'weekday', 'total_sales', 'transaction_count']
segment_time['weekday_name'] = segment_time['weekday'].apply(lambda x: weekday_names[x])

# Pivot the data for visualization
segment_time_pivot = segment_time.pivot(index='weekday_name', columns='customer_segment', values='transaction_count')
segment_time_pivot = segment_time_pivot.fillna(0)
segment_time_pivot = segment_time_pivot.reindex(weekday_names)

# สร้างกราฟเปรียบเทียบช่วงเวลาการซื้อตามกลุ่มลูกค้า
plt.figure(figsize=(12, 6))
segment_time_pivot.plot(kind='line', marker='o', colormap='viridis', linewidth=2)
plt.title('Transaction Count by Day of Week and Customer Segment')
plt.xlabel('Day of Week')
plt.ylabel('Transaction Count')
plt.legend(title='Customer Segment')
plt.grid(True)
plt.tight_layout()
plt.show()
```

## 6. การวิเคราะห์ประสิทธิภาพของแคมเปญการตลาด

```python
# ฟังก์ชันเพื่อกำหนดแคมเปญสำหรับการขายแต่ละรายการ
def assign_campaign(sale_date):
    for idx, row in marketing_df.iterrows():
        if row['campaign_start'] <= sale_date <= row['campaign_end']:
            return row['campaign_id']
    return None

# ทำการสุ่มข้อมูลบางส่วนเพื่อลดเวลาในการประมวลผล (ในกรณีข้อมูลมีขนาดใหญ่)
sales_sample = sales_df.sample(frac=0.3, random_state=42) if len(sales_df) > 10000 else sales_df

# กำหนดแคมเปญให้กับข้อมูลการขาย
sales_sample['campaign_id'] = sales_sample['sale_date'].apply(assign_campaign)

# รวมข้อมูลการขายกับข้อมูลแคมเปญ
sales_with_campaign = pd.merge(sales_sample, marketing_df, on='campaign_id', how='left')
sales_with_campaign = pd.merge(sales_with_campaign, product_df, on='product_id', how='left')

# คำนวณกำไรสำหรับการวิเคราะห์ ROI
sales_with_campaign['profit'] = sales_with_campaign['sale_amount'] - (sales_with_campaign['quantity'] * sales_with_campaign['cost_price'])

# วิเคราะห์ประสิทธิภาพของแคมเปญ
campaign_performance = sales_with_campaign.groupby(['campaign_id', 'campaign_name', 'campaign_type']).agg({
    'sale_amount': 'sum',
    'profit': 'sum',
    'sale_id': 'count'
}).reset_index()

# เพิ่มข้อมูลงบประมาณแคมเปญ
campaign_performance = pd.merge(campaign_performance, marketing_df[['campaign_id', 'campaign_cost']], on='campaign_id', how='left')
campaign_performance['ROI'] = (campaign_performance['profit'] - campaign_performance['campaign_cost']) / campaign_performance['campaign_cost']
campaign_performance['sales_per_cost'] = campaign_performance['sale_amount'] / campaign_performance['campaign_cost']

# จัดเรียงตาม ROI
campaign_performance_sorted = campaign_performance.sort_values('ROI', ascending=False)

# สร้างกราฟประสิทธิภาพของแคมเปญตาม ROI
plt.figure(figsize=(14, 6))
sns.barplot(x='campaign_name', y='ROI', hue='campaign_type', data=campaign_performance_sorted, palette='viridis')
plt.title('Campaign ROI Analysis')
plt.xlabel('Campaign')
plt.ylabel('ROI')
plt.axhline(y=0, color='r', linestyle='--')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Campaign Type')
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()

# วิเคราะห์ประสิทธิภาพตามประเภทแคมเปญ
campaign_type_performance = campaign_performance.groupby('campaign_type').agg({
    'sale_amount': 'sum',
    'profit': 'sum',
    'campaign_cost': 'sum',
    'campaign_id': 'count'
}).reset_index()

campaign_type_performance.columns = ['campaign_type', 'total_sales', 'total_profit', 'total_cost', 'campaign_count']
campaign_type_performance['ROI'] = (campaign_type_performance['total_profit'] - campaign_type_performance['total_cost']) / campaign_type_performance['total_cost']
campaign_type_performance['avg_sales_per_campaign'] = campaign_type_performance['total_sales'] / campaign_type_performance['campaign_count']
campaign_type_performance['avg_cost_per_campaign'] = campaign_type_performance['total_cost'] / campaign_type_performance['campaign_count']

# สร้างกราฟประสิทธิภาพตามประเภทแคมเปญ
plt.figure(figsize=(14, 10))
plt.subplot(2, 2, 1)
sns.barplot(x='campaign_type', y='ROI', data=campaign_type_performance, palette='viridis')
plt.title('ROI by Campaign Type')
plt.xlabel('Campaign Type')
plt.ylabel('ROI')
plt.axhline(y=0, color='r', linestyle='--')
plt.grid(True, axis='y')

plt.subplot(2, 2, 2)
sns.barplot(x='campaign_type', y='total_sales', data=campaign_type_performance, palette='viridis')
plt.title('Total Sales by Campaign Type')
plt.xlabel('Campaign Type')
plt.ylabel('Total Sales')
plt.grid(True, axis='y')

plt.subplot(2, 2, 3)
sns.barplot(x='campaign_type', y='avg_sales_per_campaign', data=campaign_type_performance, palette='viridis')
plt.title('Average Sales per Campaign')
plt.xlabel('Campaign Type')
plt.ylabel('Avg Sales per Campaign')
plt.grid(True, axis='y')

plt.subplot(2, 2, 4)
sns.barplot(x='campaign_type', y='avg_cost_per_campaign', data=campaign_type_performance, palette='viridis')
plt.title('Average Cost per Campaign')
plt.xlabel('Campaign Type')
plt.ylabel('Avg Cost per Campaign')
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()

# วิเคราะห์ผลกระทบของแคมเปญต่อยอดขายในแต่ละช่วงเวลา
# เลือกแคมเปญตัวอย่าง
sample_campaign_id = campaign_performance_sorted.iloc[0]['campaign_id']
sample_campaign = marketing_df[marketing_df['campaign_id'] == sample_campaign_id].iloc[0]

# กำหนดช่วงเวลาสำหรับการวิเคราะห์
pre_campaign_start = sample_campaign['campaign_start'] - pd.Timedelta(days=15)
post_campaign_end = sample_campaign['campaign_end'] + pd.Timedelta(days=15)

# กรองข้อมูลการขายในช่วงเวลาที่กำหนด
time_range_sales = sales_df[(sales_df['sale_date'] >= pre_campaign_start) & 
                           (sales_df['sale_date'] <= post_campaign_end)]

# จัดกลุ่มข้อมูลตามวัน
daily_sales = time_range_sales.groupby(time_range_sales['sale_date'].dt.date).agg({
    'sale_amount': 'sum',
    'sale_id': 'count'
}).reset_index()

# เพิ่มสถานะของแคมเปญ (ก่อน/ระหว่าง/หลัง)
daily_sales['campaign_status'] = daily_sales['sale_date'].apply(
    lambda x: 'During Campaign' if (sample_campaign['campaign_start'].date() <= x <= sample_campaign['campaign_end'].date())
    else ('Before Campaign' if x < sample_campaign['campaign_start'].date() else 'After Campaign')
)

# สร้างกราฟวิเคราะห์ผลกระทบของแคมเปญ
plt.figure(figsize=(14, 6))
sns.lineplot(x='sale_date', y='sale_amount', hue='campaign_status', data=daily_sales, marker='o')
plt.title(f'Sales Before, During, and After Campaign: {sample_campaign["campaign_name"]}')
plt.xlabel('Date')
plt.ylabel('Daily Sales Amount')
plt.axvline(x=sample_campaign['campaign_start'].date(), color='g', linestyle='--', label='Campaign Start')
plt.axvline(x=sample_campaign['campaign_end'].date(), color='r', linestyle='--', label='Campaign End')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# สรุปผลกระทบของแคมเปญ
campaign_impact = daily_sales.groupby('campaign_status').agg({
    'sale_amount': ['sum', 'mean'],
    'sale_id': ['sum', 'mean']
}).reset_index()

campaign_impact.columns = ['campaign_status', 'total_sales', 'avg_daily_sales', 'total_transactions', 'avg_daily_transactions']
print("\nCampaign Impact Summary:")
print(campaign_impact)

# คำนวณการเปลี่ยนแปลงเปรียบเทียบกับช่วงก่อนแคมเปญ
before_stats = campaign_impact[campaign_impact['campaign_status'] == 'Before Campaign']
if not before_stats.empty:
    before_avg_sales = before_stats.iloc[0]['avg_daily_sales']
    before_avg_transactions = before_stats.iloc[0]['avg_daily_transactions']
    
    for status in ['During Campaign', 'After Campaign']:
        status_stats = campaign_impact[campaign_impact['campaign_status'] == status]
        if not status_stats.empty:
            status_avg_sales = status_stats.iloc[0]['avg_daily_sales']
            status_avg_transactions = status_stats.iloc[0]['avg_daily_transactions']
            
            sales_change_pct = (status_avg_sales - before_avg_sales) / before_avg_sales * 100
            transactions_change_pct = (status_avg_transactions - before_avg_transactions) / before_avg_transactions * 100
            
            print(f"\n{status} vs Before Campaign:")
            print(f"Average Daily Sales Change: {sales_change_pct:.2f}%")
            print(f"Average Daily Transactions Change: {transactions_change_pct:.2f}%")
```

## 7. การสรุปข้อมูลสำหรับการนำเสนอ

```python
# สรุปข้อค้นพบสำคัญ
# 1. แนวโน้มยอดขายและกำไร
print("1. Sales and Profit Trends Summary:")
print("-" * 50)
# - คำนวณการเปลี่ยนแปลงของยอดขายและกำไรในช่วง 6 เดือนล่าสุดเทียบกับช่วงเดียวกันของปีก่อน
last_6_months = monthly_sales.sort_values(['year', 'month'], ascending=False).head(6)
previous_6_months = monthly_sales.sort_values(['year', 'month'], ascending=False).iloc[12:18]

last_6m_sales = last_6_months['total_sales'].sum()
prev_6m_sales = previous_6_months['total_sales'].sum()
sales_yoy_change = (last_6m_sales - prev_6m_sales) / prev_6m_sales * 100

last_6m_profit = last_6_months['total_profit'].sum()
prev_6m_profit = previous_6_months['total_profit'].sum()
profit_yoy_change = (last_6m_profit - prev_6m_profit) / prev_6m_profit * 100

last_6m_margin = last_6m_profit / last_6m_sales
prev_6m_margin = prev_6m_profit / prev_6m_sales
margin_change = last_6m_margin - prev_6m_margin

print(f"Last 6 months total sales: {last_6m_sales:,.2f}")
print(f"YoY Sales change: {sales_yoy_change:.2f}%")
print(f"Last 6 months profit margin: {last_6m_margin:.2%}")
print(f"YoY Profit margin change: {margin_change:.2%}")

# แสดงเดือนที่มียอดขายสูงสุดและต่ำสุดในช่วง 12 เดือนที่ผ่านมา
last_12_months = monthly_sales.sort_values(['year', 'month'], ascending=False).head(12)
best_month = last_12_months.loc[last_12_months['total_sales'].idxmax()]
worst_month = last_12_months.loc[last_12_months['total_sales'].idxmin()]

print(f"\nBest performing month: {best_month['year_month']} with sales of {best_month['total_sales']:,.2f}")
print(f"Worst performing month: {worst_month['year_month']} with sales of {worst_month['total_sales']:,.2f}")

# 2. ประสิทธิภาพของหมวดหมู่สินค้า
print("\n2. Product Category Performance Summary:")
print("-" * 50)
best_category = category_performance_by_sales.iloc[0]
worst_category = category_performance_by_sales.iloc[-1]
best_margin_category = category_performance.sort_values('profit_margin', ascending=False).iloc[0]
worst_margin_category = category_performance.sort_values('profit_margin').iloc[0]

print(f"Best performing category by sales: {best_category['category']} with sales of {best_category['total_sales']:,.2f}")
print(f"Worst performing category by sales: {worst_category['category']} with sales of {worst_category['total_sales']:,.2f}")
print(f"Best performing category by margin: {best_margin_category['category']} with margin of {best_margin_category['profit_margin']:.2%}")
print(f"Worst performing category by margin: {worst_margin_category['category']} with margin of {worst_margin_category['profit_margin']:.2%}")

# 3. ประสิทธิภาพของสาขา
print("\n3. Store Performance Summary:")
print("-" * 50)
best_store = store_performance.sort_values('total_sales', ascending=False).iloc[0]
worst_store = store_performance.sort_values('total_sales').iloc[0]
best_daily_sales_store = store_performance.sort_values('daily_avg_sales', ascending=False).iloc[0]

best_region = region_performance.sort_values('total_sales', ascending=False).iloc[0]
worst_region = region_performance.sort_values('total_sales').iloc[0]

print(f"Best performing store: {best_store['store_name']} ({best_store['store_type']}) with sales of {best_store['total_sales']:,.2f}")
print(f"Worst performing store: {worst_store['store_name']} ({worst_store['store_type']}) with sales of {worst_store['total_sales']:,.2f}")
print(f"Best performing region: {best_region['region']} with sales of {best_region['total_sales']:,.2f}")
print(f"Worst performing region: {worst_region['region']} with sales of {worst_region['total_sales']:,.2f}")

# 4. การวิเคราะห์ลูกค้า
print("\n4. Customer Analysis Summary:")
print("-" * 50)
segment_counts = customer_full['customer_segment'].value_counts()
high_value_count = segment_counts.get('High Value', 0)
high_value_pct = high_value_count / len(customer_full) * 100

high_value_monetary = customer_full[customer_full['customer_segment'] == 'High Value']['monetary'].sum()
total_monetary = customer_full['monetary'].sum()
high_value_monetary_pct = high_value_monetary / total_monetary * 100

print(f"Number of customers: {len(customer_full)}")
print(f"High value customers: {high_value_count} ({high_value_pct:.2f}% of total customers)")
print(f"High value customers contribute {high_value_monetary_pct:.2f}% of total sales")

# 5. ประสิทธิภาพของแคมเปญการตลาด
if 'campaign_performance' in locals():
    print("\n5. Marketing Campaign Performance Summary:")
    print("-" * 50)
    best_campaign = campaign_performance.sort_values('ROI', ascending=False).iloc[0]
    worst_campaign = campaign_performance.sort_values('ROI').iloc[0]
    
    best_type = campaign_type_performance.sort_values('ROI', ascending=False).iloc[0]
    worst_type = campaign_type_performance.sort_values('ROI').iloc[0]
    
    print(f"Best performing campaign: {best_campaign['campaign_name']} with ROI of {best_campaign['ROI']:.2f}")
    print(f"Worst performing campaign: {worst_campaign['campaign_name']} with ROI of {worst_campaign['ROI']:.2f}")
    print(f"Best performing campaign type: {best_type['campaign_type']} with average ROI of {best_type['ROI']:.2f}")
    print(f"Worst performing campaign type: {worst_type['campaign_type']} with average ROI of {worst_type['ROI']:.2f}")
```

## 8. การเตรียมข้อมูลสำหรับ Power BI

```python
# สร้างไฟล์ CSV ที่รวมข้อมูลสำหรับนำเข้าใน Power BI
# 1. ข้อมูลการขายพร้อมข้อมูลสินค้าและสาขา
sales_for_powerbi = sales_with_store.copy()
# เพิ่มคอลัมน์ที่จำเป็น เช่น ปี เดือน ไตรมาส
sales_for_powerbi['year'] = sales_for_powerbi['sale_date'].dt.year
sales_for_powerbi['quarter'] = sales_for_powerbi['sale_date'].dt.quarter
sales_for_powerbi['month'] = sales_for_powerbi['sale_date'].dt.month
sales_for_powerbi['month_name'] = sales_for_powerbi['sale_date'].dt.strftime('%B')
sales_for_powerbi['week'] = sales_for_powerbi['sale_date'].dt.isocalendar().week
sales_for_powerbi['day'] = sales_for_powerbi['sale_date'].dt.day
sales_for_powerbi['weekday'] = sales_for_powerbi['sale_date'].dt.weekday
sales_for_powerbi['weekday_name'] = sales_for_powerbi['weekday'].apply(lambda x: weekday_names[x])
sales_for_powerbi['weekend'] = sales_for_powerbi['weekday'].apply(lambda x: 1 if x >= 5 else 0)

# 2. ข้อมูลลูกค้าพร้อม segment
if 'customer_full' in locals():
    customer_for_powerbi = customer_full.copy()
    # เลือกคอลัมน์ที่ต้องการ
    customer_columns = ['customer_id', 'recency', 'frequency', 'monetary', 'customer_segment', 
                         'age', 'gender', 'city', 'member_since']  # ปรับตามคอลัมน์ที่มีในข้อมูลจริง
    
    customer_for_powerbi = customer_for_powerbi[customer_columns]

# 3. ข้อมูลสินค้าพร้อมประสิทธิภาพ
product_performance_for_powerbi = product_performance.copy()

# 4. ข้อมูลสาขาพร้อมประสิทธิภาพ
store_performance_for_powerbi = store_performance.copy()

# 5. ข้อมูลแคมเปญพร้อมประสิทธิภาพ
if 'campaign_performance' in locals():
    campaign_performance_for_powerbi = campaign_performance.copy()

# บันทึกไฟล์ CSV
sales_for_powerbi.to_csv('sales_analysis.csv', index=False)
if 'customer_for_powerbi' in locals():
    customer_for_powerbi.to_csv('customer_analysis.csv', index=False)
product_performance_for_powerbi.to_csv('product_analysis.csv', index=False)
store_performance_for_powerbi.to_csv('store_analysis.csv', index=False)
if 'campaign_performance_for_powerbi' in locals():
    campaign_performance_for_powerbi.to_csv('campaign_analysis.csv', index=False)

print("Data exported successfully for Power BI import.")
```

## หมายเหตุสำหรับการใช้งานโค้ด

1. โค้ดตัวอย่างนี้อาจต้องปรับเปลี่ยนให้เข้ากับโครงสร้างข้อมูลจริงที่ใช้ในกรณีศึกษา
2. ควรตรวจสอบชื่อคอลัมน์และประเภทข้อมูลให้ตรงกับข้อมูลจริงก่อนใช้งาน
3. บางส่วนของโค้ดอาจต้องปรับแต่งเพิ่มเติมตามความซับซ้อนของข้อมูลและความต้องการในการวิเคราะห์
4. สำหรับชุดข้อมูลขนาดใหญ่ ควรพิจารณาเทคนิคการเพิ่มประสิทธิภาพ เช่น การสุ่มตัวอย่างข้อมูล หรือการใช้ libraries ที่เหมาะสม เช่น dask สำหรับการประมวลผลแบบขนาน
5. การใช้งาน visualization libraries นอกเหนือจาก matplotlib และ seaborn เช่น plotly อาจช่วยให้การนำเสนอข้อมูลมีความน่าสนใจและโต้ตอบได้มากขึ้น

ผู้เรียนสามารถคัดลอกและปรับแต่งโค้ดเหล่านี้เพื่อใช้ในการวิเคราะห์ข้อมูลตามความต้องการของกรณีศึกษา
