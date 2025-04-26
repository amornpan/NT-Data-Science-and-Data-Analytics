# กรณีศึกษา – วิเคราะห์ข้อมูลจากสถานการณ์จริง

## บทนำ

ในช่วงบ่ายของวันที่ 3 นี้ เราจะนำความรู้ทั้งหมดที่ได้เรียนมาประยุกต์ใช้กับกรณีศึกษาจากสถานการณ์จริง จุดประสงค์คือเพื่อให้ผู้เรียนได้ฝึกใช้ทักษะการวิเคราะห์ข้อมูลด้วย Python, SQL และเครื่องมือ Business Intelligence ในการแก้ปัญหาธุรกิจที่สมจริง กรณีศึกษานี้จะเน้นที่การวิเคราะห์ข้อมูล การสร้าง visualization และ dashboard รวมถึงการนำเสนอผลลัพธ์และข้อเสนอแนะ

## โจทย์กรณีศึกษา: บริษัท TechRetail

### ข้อมูลบริษัท

**TechRetail** เป็นบริษัทจำหน่ายอุปกรณ์อิเล็กทรอนิกส์และเทคโนโลยีที่มีหลายสาขาทั่วประเทศไทย บริษัทมีการดำเนินธุรกิจทั้งในรูปแบบร้านค้าปลีกและช่องทางออนไลน์ 

ประเภทสินค้าของบริษัทได้แก่:
- สมาร์ทโฟนและแท็บเล็ต
- คอมพิวเตอร์และแล็ปท็อป
- อุปกรณ์เสริม (เช่น หูฟัง, ลำโพง, แบตเตอรี่สำรอง)
- กล้องและอุปกรณ์ถ่ายภาพ
- สมาร์ทโฮมและอุปกรณ์อัจฉริยะ

### สถานการณ์ปัญหา

ในช่วง 12 เดือนที่ผ่านมา บริษัท TechRetail ประสบปัญหาด้านยอดขายและกำไรที่ไม่เป็นไปตามเป้าหมาย ถึงแม้ว่าจะมีการลงทุนในด้านการตลาดและการเปิดสาขาใหม่ก็ตาม ผู้บริหารต้องการวิเคราะห์ข้อมูลเพื่อระบุปัญหาและหาแนวทางแก้ไข โดยมีคำถามสำคัญดังนี้:

1. อะไรคือสาเหตุหลักที่ทำให้ยอดขายและกำไรไม่เป็นไปตามเป้าหมาย?
2. กลุ่มสินค้าใดที่มีประสิทธิภาพดีที่สุดและแย่ที่สุด?
3. สาขาใดที่มีประสิทธิภาพสูงและต่ำ และเพราะอะไร?
4. พฤติกรรมการซื้อของลูกค้าเปลี่ยนแปลงไปอย่างไรบ้าง?
5. ควรมีการปรับกลยุทธ์ทางธุรกิจอย่างไรเพื่อปรับปรุงผลการดำเนินงาน?

### ชุดข้อมูลที่มี

บริษัทได้ให้ชุดข้อมูลต่อไปนี้สำหรับการวิเคราะห์:

1. **sales_data.csv** - ข้อมูลการขายรายวันย้อนหลัง 2 ปี
2. **product_data.csv** - ข้อมูลสินค้าทั้งหมดในระบบ
3. **store_data.csv** - ข้อมูลสาขาทั้งหมดของบริษัท
4. **customer_data.csv** - ข้อมูลลูกค้าและการซื้อสินค้า
5. **marketing_data.csv** - ข้อมูลแคมเปญการตลาดและงบประมาณ

## ขั้นตอนการทำงาน

### ส่วนที่ 1: การเตรียมและสำรวจข้อมูล (1 ชั่วโมง)

#### 1.1 การนำเข้าและตรวจสอบข้อมูล

```python
# นำเข้า library ที่จำเป็น
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
%matplotlib inline

# กำหนดรูปแบบการแสดงผลกราฟ
plt.style.use('seaborn-whitegrid')
sns.set(style="whitegrid")

# นำเข้าข้อมูล
sales_df = pd.read_csv('sales_data.csv')
product_df = pd.read_csv('product_data.csv')
store_df = pd.read_csv('store_data.csv')
customer_df = pd.read_csv('customer_data.csv')
marketing_df = pd.read_csv('marketing_data.csv')

# ตรวจสอบข้อมูลแต่ละชุด
print("Sales Data Shape:", sales_df.shape)
print("\nProduct Data Shape:", product_df.shape)
print("\nStore Data Shape:", store_df.shape)
print("\nCustomer Data Shape:", customer_df.shape)
print("\nMarketing Data Shape:", marketing_df.shape)

# ดูข้อมูลตัวอย่างและประเภทข้อมูล
print("\nSales Data Sample:")
print(sales_df.head())
print("\nSales Data Info:")
print(sales_df.info())
```

#### 1.2 การเตรียมข้อมูล

```python
# แปลงคอลัมน์วันที่เป็น datetime
sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])
marketing_df['campaign_start'] = pd.to_datetime(marketing_df['campaign_start'])
marketing_df['campaign_end'] = pd.to_datetime(marketing_df['campaign_end'])

# ตรวจสอบและจัดการค่า missing values
print("\nMissing values in Sales data:")
print(sales_df.isnull().sum())

# แทนที่ค่า missing หรือลบแถวที่มีค่า missing ตามความเหมาะสม
sales_df = sales_df.dropna(subset=['sale_amount', 'product_id', 'store_id'])

# เพิ่มคอลัมน์ที่จำเป็นสำหรับการวิเคราะห์
sales_df['year'] = sales_df['sale_date'].dt.year
sales_df['month'] = sales_df['sale_date'].dt.month
sales_df['day'] = sales_df['sale_date'].dt.day
sales_df['weekday'] = sales_df['sale_date'].dt.weekday
sales_df['weekend'] = sales_df['weekday'].apply(lambda x: 1 if x >= 5 else 0)

# คำนวณกำไรสำหรับแต่ละธุรกรรม (เชื่อมกับข้อมูลสินค้า)
sales_with_product = pd.merge(sales_df, product_df, on='product_id', how='left')
sales_with_product['profit'] = sales_with_product['sale_amount'] - (sales_with_product['quantity'] * sales_with_product['cost_price'])

# ตรวจสอบผลลัพธ์
print("\nSales with profit calculation:")
print(sales_with_product.head())
```

#### 1.3 การสำรวจข้อมูลเบื้องต้น

```python
# วิเคราะห์แนวโน้มยอดขายรายเดือน
monthly_sales = sales_with_product.groupby([sales_with_product['sale_date'].dt.year, sales_with_product['sale_date'].dt.month])['sale_amount'].sum().reset_index()
monthly_sales.columns = ['year', 'month', 'total_sales']
monthly_sales['year_month'] = monthly_sales['year'].astype(str) + '-' + monthly_sales['month'].astype(str)

plt.figure(figsize=(14,6))
plt.plot(monthly_sales['year_month'], monthly_sales['total_sales'], marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Year-Month')
plt.ylabel('Total Sales Amount')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# วิเคราะห์ยอดขายตามหมวดหมู่สินค้า
category_sales = sales_with_product.groupby('category')['sale_amount'].sum().sort_values(ascending=False)

plt.figure(figsize=(10,6))
category_sales.plot(kind='bar')
plt.title('Sales by Product Category')
plt.xlabel('Category')
plt.ylabel('Total Sales Amount')
plt.tight_layout()
plt.show()

# วิเคราะห์ประสิทธิภาพของสาขา
store_performance = sales_with_product.groupby('store_id')['sale_amount'].sum().reset_index()
store_details = pd.merge(store_performance, store_df, on='store_id', how='left')
store_details = store_details.sort_values('sale_amount', ascending=False)

plt.figure(figsize=(12,6))
plt.bar(store_details['store_name'], store_details['sale_amount'])
plt.title('Sales by Store')
plt.xlabel('Store')
plt.ylabel('Total Sales Amount')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
```

### ส่วนที่ 2: การวิเคราะห์ข้อมูลเชิงลึก (1.5 ชั่วโมง)

#### 2.1 การวิเคราะห์แนวโน้มและฤดูกาล

```python
# สร้างกราฟแนวโน้มยอดขายและกำไรรายเดือน
monthly_metrics = sales_with_product.groupby([sales_with_product['sale_date'].dt.year, sales_with_product['sale_date'].dt.month])[['sale_amount', 'profit']].sum().reset_index()
monthly_metrics.columns = ['year', 'month', 'total_sales', 'total_profit']
monthly_metrics['year_month'] = monthly_metrics['year'].astype(str) + '-' + monthly_metrics['month'].astype(str)
monthly_metrics['profit_margin'] = monthly_metrics['total_profit'] / monthly_metrics['total_sales']

fig, ax1 = plt.subplots(figsize=(14,6))

color = 'tab:blue'
ax1.set_xlabel('Year-Month')
ax1.set_ylabel('Total Sales', color=color)
ax1.plot(monthly_metrics['year_month'], monthly_metrics['total_sales'], color=color, marker='o')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Profit Margin', color=color)
ax2.plot(monthly_metrics['year_month'], monthly_metrics['profit_margin'], color=color, marker='s')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Monthly Sales and Profit Margin Trend')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# วิเคราะห์ฤดูกาลการขาย (สัปดาห์ในเดือน, วันในสัปดาห์)
# วันในสัปดาห์
weekday_sales = sales_with_product.groupby('weekday')['sale_amount'].sum()
weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

plt.figure(figsize=(10,6))
weekday_sales.index = weekday_names
weekday_sales.plot(kind='bar')
plt.title('Sales by Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Total Sales Amount')
plt.tight_layout()
plt.show()

# เดือนในปี
monthly_avg = sales_with_product.groupby(sales_with_product['sale_date'].dt.month)['sale_amount'].mean()
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

plt.figure(figsize=(10,6))
monthly_avg.index = month_names
monthly_avg.plot(kind='bar')
plt.title('Average Sales by Month')
plt.xlabel('Month')
plt.ylabel('Average Sales Amount')
plt.tight_layout()
plt.show()
```

#### 2.2 การวิเคราะห์ช่องทางการขายและประสิทธิภาพของสินค้า

```python
# เปรียบเทียบประสิทธิภาพระหว่างช่องทางการขาย
channel_performance = sales_with_product.groupby('sales_channel')[['sale_amount', 'profit']].sum()
channel_performance['profit_margin'] = channel_performance['profit'] / channel_performance['sale_amount']

plt.figure(figsize=(10,6))
channel_performance['sale_amount'].plot(kind='bar', position=0, width=0.3, color='blue', label='Sales')
channel_performance['profit'].plot(kind='bar', position=1, width=0.3, color='green', label='Profit')
plt.title('Performance by Sales Channel')
plt.xlabel('Sales Channel')
plt.ylabel('Amount')
plt.legend()
plt.tight_layout()
plt.show()

# วิเคราะห์ประสิทธิภาพของสินค้า
# Top 10 products by sales
top_products = sales_with_product.groupby(['product_id', 'product_name'])['sale_amount'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12,6))
top_products.plot(kind='bar')
plt.title('Top 10 Products by Sales')
plt.xlabel('Product')
plt.ylabel('Total Sales Amount')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Product profitability analysis
product_profitability = sales_with_product.groupby(['product_id', 'product_name'])[['sale_amount', 'profit']].sum()
product_profitability['profit_margin'] = product_profitability['profit'] / product_profitability['sale_amount']
product_profitability = product_profitability.sort_values('profit_margin', ascending=False)

# Top 10 most profitable products
plt.figure(figsize=(12,6))
product_profitability.head(10)['profit_margin'].plot(kind='bar')
plt.title('Top 10 Products by Profit Margin')
plt.xlabel('Product')
plt.ylabel('Profit Margin')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Bottom 10 least profitable products
plt.figure(figsize=(12,6))
product_profitability.tail(10)['profit_margin'].plot(kind='bar')
plt.title('Bottom 10 Products by Profit Margin')
plt.xlabel('Product')
plt.ylabel('Profit Margin')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

#### 2.3 การวิเคราะห์ลูกค้าและพฤติกรรมการซื้อ

```python
# เชื่อมข้อมูลลูกค้าและการซื้อ
customer_sales = pd.merge(sales_df, customer_df, on='customer_id', how='left')

# วิเคราะห์ RFM (Recency, Frequency, Monetary)
# 1. Recency - วันที่ซื้อล่าสุด
latest_date = sales_df['sale_date'].max()
customer_recency = sales_df.groupby('customer_id')['sale_date'].max().reset_index()
customer_recency['recency'] = (latest_date - customer_recency['sale_date']).dt.days

# 2. Frequency - จำนวนครั้งที่ซื้อ
customer_frequency = sales_df.groupby('customer_id')['sale_id'].count().reset_index()
customer_frequency.columns = ['customer_id', 'frequency']

# 3. Monetary - มูลค่าการซื้อรวม
customer_monetary = sales_df.groupby('customer_id')['sale_amount'].sum().reset_index()
customer_monetary.columns = ['customer_id', 'monetary']

# รวมข้อมูล RFM
rfm = pd.merge(customer_recency, customer_frequency, on='customer_id')
rfm = pd.merge(rfm, customer_monetary, on='customer_id')

# สร้างคะแนน RFM
rfm['R_score'] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])  # ค่าน้อย = ดีกว่า
rfm['F_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])  # ค่ามาก = ดีกว่า
rfm['M_score'] = pd.qcut(rfm['monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])  # ค่ามาก = ดีกว่า

# คำนวณคะแนนรวม
rfm['RFM_score'] = rfm['R_score'].astype(int) + rfm['F_score'].astype(int) + rfm['M_score'].astype(int)

# แบ่งกลุ่มลูกค้า
rfm['customer_segment'] = pd.qcut(rfm['RFM_score'], 3, labels=['Low Value', 'Mid Value', 'High Value'])

# วิเคราะห์การกระจายตัวของกลุ่มลูกค้า
segment_counts = rfm['customer_segment'].value_counts()

plt.figure(figsize=(10,6))
segment_counts.plot(kind='bar')
plt.title('Customer Segments Distribution')
plt.xlabel('Segment')
plt.ylabel('Number of Customers')
plt.tight_layout()
plt.show()

# วิเคราะห์มูลค่าการซื้อตามกลุ่มลูกค้า
segment_value = rfm.groupby('customer_segment')['monetary'].sum()

plt.figure(figsize=(10,6))
segment_value.plot(kind='bar')
plt.title('Total Monetary Value by Customer Segment')
plt.xlabel('Segment')
plt.ylabel('Total Purchase Value')
plt.tight_layout()
plt.show()
```

#### 2.4 การวิเคราะห์ประสิทธิภาพของแคมเปญการตลาด

```python
# เชื่อมข้อมูลการขายกับข้อมูลแคมเปญการตลาด
# (หมายเหตุ: ต้องเชื่อมโดยดูว่าการขายเกิดขึ้นในช่วงเวลาของแคมเปญหรือไม่)

# ฟังก์ชั่นสำหรับระบุว่าการขายเกิดขึ้นในช่วงแคมเปญใด
def find_campaign(sale_date):
    for idx, row in marketing_df.iterrows():
        if row['campaign_start'] <= sale_date <= row['campaign_end']:
            return row['campaign_id']
    return None

# ใช้วิธีอื่นที่มีประสิทธิภาพมากกว่าในกรณีข้อมูลมีขนาดใหญ่
sales_sample = sales_df.sample(1000)  # ตัวอย่างเพื่อความเร็ว
sales_sample['campaign_id'] = sales_sample['sale_date'].apply(find_campaign)

# วิเคราะห์ประสิทธิภาพของแต่ละแคมเปญ
campaign_performance = sales_sample.groupby('campaign_id')['sale_amount'].sum().reset_index()
campaign_details = pd.merge(campaign_performance, marketing_df, on='campaign_id', how='left')
campaign_details['ROI'] = (campaign_details['sale_amount'] - campaign_details['campaign_cost']) / campaign_details['campaign_cost']

# แสดงผล ROI ของแต่ละแคมเปญ
plt.figure(figsize=(12,6))
plt.bar(campaign_details['campaign_name'], campaign_details['ROI'])
plt.title('ROI by Marketing Campaign')
plt.xlabel('Campaign')
plt.ylabel('ROI')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# วิเคราะห์ประสิทธิภาพตามประเภทแคมเปญ
campaign_type_perf = campaign_details.groupby('campaign_type')['ROI'].mean()

plt.figure(figsize=(10,6))
campaign_type_perf.plot(kind='bar')
plt.title('Average ROI by Campaign Type')
plt.xlabel('Campaign Type')
plt.ylabel('Average ROI')
plt.tight_layout()
plt.show()
```

### ส่วนที่ 3: การสร้าง Dashboard ด้วย Power BI (1 ชั่วโมง)

ในส่วนนี้ ผู้เรียนจะนำข้อมูลที่ได้วิเคราะห์มาสร้าง Dashboard ใน Power BI โดยมีขั้นตอนดังนี้:

#### 3.1 การนำเข้าข้อมูลใน Power BI
1. เปิดโปรแกรม Power BI Desktop
2. นำเข้าข้อมูลจากไฟล์ CSV ทั้ง 5 ไฟล์
3. ตรวจสอบและปรับแต่งประเภทข้อมูลให้ถูกต้อง
4. สร้างความสัมพันธ์ระหว่างตาราง (Data Relationships)

#### 3.2 การสร้าง Dashboard สำหรับภาพรวมธุรกิจ
Dashboard นี้ควรประกอบด้วย:

1. **KPI Cards**:
   - ยอดขายรวม
   - กำไรรวม
   - อัตรากำไร
   - จำนวนธุรกรรม
   - ยอดขายเฉลี่ยต่อธุรกรรม

2. **แนวโน้มการขายและกำไร**:
   - แผนภูมิเส้นแสดงแนวโน้มยอดขายและกำไรรายเดือน
   - แผนภูมิแท่งเปรียบเทียบยอดขายกับเป้าหมาย

3. **การวิเคราะห์สินค้า**:
   - แผนภูมิแท่งแสดงยอดขายตามหมวดหมู่สินค้า
   - Heat map แสดงความสัมพันธ์ระหว่างยอดขายและกำไรของแต่ละหมวดหมู่

4. **การวิเคราะห์สาขา**:
   - แผนที่แสดงที่ตั้งและประสิทธิภาพของสาขา
   - แผนภูมิแท่งแสดงประสิทธิภาพของแต่ละสาขา

5. **การวิเคราะห์ลูกค้า**:
   - แผนภูมิวงกลมแสดงสัดส่วนลูกค้าแต่ละกลุ่ม
   - แผนภูมิแท่งแสดงมูลค่าการซื้อตามกลุ่มลูกค้า

#### 3.3 การตั้งค่า Interactive Features
1. สร้าง Slicers สำหรับการกรองข้อมูลตาม:
   - ช่วงเวลา
   - หมวดหมู่สินค้า
   - ภูมิภาคหรือสาขา
   - ช่องทางการขาย

2. ตั้งค่า Drill-down และ Drill-through:
   - สามารถ Drill-down จากมุมมองรายปี > รายไตรมาส > รายเดือน > รายวัน
   - สามารถ Drill-through จากหมวดหมู่สินค้าไปยังรายละเอียดของแต่ละสินค้า

3. ตั้งค่า Bookmarks สำหรับมุมมองต่างๆ:
   - มุมมองภาพรวมธุรกิจ
   - มุมมองการวิเคราะห์สินค้า
   - มุมมองการวิเคราะห์สาขา
   - มุมมองการวิเคราะห์ลูกค้า

### ส่วนที่ 4: การวิเคราะห์ผลและการนำเสนอข้อเสนอแนะ (0.5 ชั่วโมง)

จากการวิเคราะห์ข้อมูลและ Dashboard ที่สร้างขึ้น ผู้เรียนต้องเตรียมสรุปผลการวิเคราะห์และจัดทำข้อเสนอแนะ โดยควรครอบคลุมประเด็นต่อไปนี้:

#### 4.1 สรุปข้อค้นพบสำคัญ (Key Findings)

1. **แนวโน้มยอดขายและกำไร**:
   - สรุปแนวโน้มยอดขายและกำไรในช่วง 12 เดือนที่ผ่านมา
   - ระบุช่วงเวลาที่มียอดขายสูงและต่ำ พร้อมอธิบายปัจจัยที่อาจมีผล

2. **การวิเคราะห์สินค้า**:
   - ระบุหมวดหมู่และสินค้าที่มีประสิทธิภาพดีที่สุดและแย่ที่สุด
   - วิเคราะห์สาเหตุที่ทำให้สินค้าบางรายการมีประสิทธิภาพต่ำ

3. **การวิเคราะห์สาขา**:
   - ระบุสาขาที่มีประสิทธิภาพสูงและต่ำ
   - วิเคราะห์ปัจจัยที่ส่งผลต่อประสิทธิภาพของสาขา

4. **การวิเคราะห์ลูกค้า**:
   - อธิบายพฤติกรรมการซื้อของกลุ่มลูกค้าแต่ละกลุ่ม
   - ระบุโอกาสในการเพิ่มยอดขายจากกลุ่มลูกค้าแต่ละกลุ่ม

5. **การวิเคราะห์แคมเปญการตลาด**:
   - ระบุแคมเปญและประเภทแคมเปญที่มีประสิทธิภาพสูงและต่ำ
   - วิเคราะห์ ROI ของแคมเปญแต่ละประเภท

#### 4.2 ข้อเสนอแนะ (Recommendations)

จากข้อค้นพบข้างต้น ให้จัดทำข้อเสนอแนะเพื่อปรับปรุงผลการดำเนินงานของบริษัท โดยแบ่งเป็น:

1. **ข้อเสนอแนะระยะสั้น (0-3 เดือน)**:
   - มาตรการเร่งด่วนเพื่อแก้ไขปัญหาที่มีผลกระทบสูง
   - การปรับกลยุทธ์ทางการตลาดเพื่อเพิ่มยอดขายในระยะสั้น

2. **ข้อเสนอแนะระยะกลาง (3-6 เดือน)**:
   - การปรับปรุงประสิทธิภาพของสาขาและช่องทางการขาย
   - การปรับสัดส่วนสินค้าและกลยุทธ์ราคา

3. **ข้อเสนอแนะระยะยาว (6-12 เดือน)**:
   - กลยุทธ์การเติบโตทางธุรกิจในระยะยาว
   - การพัฒนาระบบและกระบวนการเพื่อเพิ่มประสิทธิภาพ

#### 4.3 แผนการติดตามผล (Follow-up Plan)

นำเสนอแผนการติดตามผลการดำเนินการตามข้อเสนอแนะ:

1. **KPI ที่ต้องติดตาม**:
   - ระบุ KPI หลักที่ต้องติดตามสำหรับแต่ละข้อเสนอแนะ
   - กำหนดเป้าหมายและระยะเวลาที่ชัดเจน

2. **ความถี่ในการติดตาม**:
   - กำหนดความถี่ในการติดตามผลและปรับแผน
   - ระบุผู้รับผิดชอบในการติดตามผล

3. **การปรับแผน**:
   - กำหนดเงื่อนไขในการปรับแผนหากผลการดำเนินงานไม่เป็นไปตามเป้าหมาย
   - เตรียมแผนสำรองสำหรับสถานการณ์ต่างๆ

## การนำเสนอผลงาน

หลังจากเสร็จสิ้นการวิเคราะห์และจัดทำข้อเสนอแนะ ผู้เรียนจะต้องนำเสนอผลงานต่อกลุ่ม โดยมีเวลานำเสนอกลุ่มละ 15 นาที ซึ่งควรครอบคลุมเนื้อหาดังนี้:

1. **ภาพรวมของกรณีศึกษาและวัตถุประสงค์** (2 นาที)
2. **วิธีการวิเคราะห์และเครื่องมือที่ใช้** (3 นาที)
3. **นำเสนอ Dashboard และอธิบายข้อค้นพบสำคัญ** (5 นาที)
4. **นำเสนอข้อเสนอแนะและแผนการติดตามผล** (5 นาที)

การนำเสนอควรมีความชัดเจน กระชับ และเน้นที่ข้อค้นพบและข้อเสนอแนะที่มีผลกระทบสูงต่อธุรกิจ รวมถึงแสดงให้เห็นถึงการใช้ข้อมูลในการตัดสินใจทางธุรกิจอย่างมีประสิทธิภาพ

## การประเมินผล

กรณีศึกษานี้จะประเมินผลจากปัจจัยต่อไปนี้:

1. **ความถูกต้องของการวิเคราะห์ข้อมูล** (30%)
   - ความถูกต้องของวิธีการและผลการวิเคราะห์
   - ความครอบคลุมของประเด็นที่วิเคราะห์

2. **คุณภาพของ Dashboard** (30%)
   - การออกแบบและความสวยงาม
   - ความสามารถในการสื่อสารข้อมูลอย่างมีประสิทธิภาพ
   - ความสามารถในการโต้ตอบและการกรองข้อมูล

3. **คุณภาพของข้อเสนอแนะ** (30%)
   - ความสอดคล้องของข้อเสนอแนะกับผลการวิเคราะห์
   - ความเป็นไปได้และความเฉพาะเจาะจงของข้อเสนอแนะ
   - ความครอบคลุมของข้อเสนอแนะในระยะสั้น กลาง และยาว

4. **การนำเสนอ** (10%)
   - ความชัดเจนและความน่าสนใจของการนำเสนอ
   - การตอบคำถามและการแสดงความเข้าใจในเนื้อหา
   - การบริหารเวลาในการนำเสนอ

## สรุป

กรณีศึกษานี้เป็นโอกาสให้ผู้เรียนได้ประยุกต์ใช้ความรู้ด้านการวิเคราะห์ข้อมูล, Python, SQL และ Business Intelligence Tools ในสถานการณ์ธุรกิจจริง การทำงานนี้จะช่วยให้ผู้เรียนเข้าใจกระบวนการทั้งหมดตั้งแต่การเตรียมข้อมูล การวิเคราะห์ การสร้าง Dashboard ไปจนถึงการนำเสนอข้อเสนอแนะที่มีประสิทธิภาพ ซึ่งเป็นทักษะสำคัญสำหรับนักวิเคราะห์ข้อมูลและนักวิทยาศาสตร์ข้อมูลในสภาพแวดล้อมธุรกิจจริง
