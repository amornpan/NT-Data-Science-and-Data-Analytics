# พื้นฐาน SQL สำหรับการวิเคราะห์ข้อมูล

## เนื้อหาสำหรับการนำเสนอ

### 1. ความรู้พื้นฐานเกี่ยวกับฐานข้อมูลและ SQL

#### ฐานข้อมูลคืออะไร
- ฐานข้อมูล (Database) คือ ระบบจัดเก็บข้อมูลอิเล็กทรอนิกส์ที่ออกแบบมาเพื่อจัดเก็บ จัดการ และเรียกใช้ข้อมูลได้อย่างมีประสิทธิภาพ
- ฐานข้อมูลช่วยให้สามารถจัดการข้อมูลขนาดใหญ่ได้อย่างมีระบบ
- เป็นแหล่งเก็บข้อมูลที่สำคัญขององค์กรส่วนใหญ่

#### ฐานข้อมูลเชิงสัมพันธ์ (Relational Database)
- จัดเก็บข้อมูลในรูปแบบตาราง (Tables) ที่มีความสัมพันธ์กัน
- แต่ละตารางประกอบด้วยแถว (Rows) และคอลัมน์ (Columns)
- มีการกำหนดความสัมพันธ์ระหว่างตารางผ่านคีย์หลัก (Primary Key) และคีย์นอก (Foreign Key)

#### SQL คืออะไร
- SQL (Structured Query Language) คือภาษาที่ใช้ในการจัดการและเรียกใช้ข้อมูลในฐานข้อมูลเชิงสัมพันธ์
- เป็นภาษามาตรฐานที่ใช้กับระบบจัดการฐานข้อมูลส่วนใหญ่
- สามารถใช้ SQL ในการสร้าง อ่าน อัพเดต และลบข้อมูล (CRUD: Create, Read, Update, Delete)

#### ระบบจัดการฐานข้อมูลที่นิยมใช้
- MySQL
- PostgreSQL
- Microsoft SQL Server
- Oracle Database
- SQLite
- Google BigQuery

### 2. การใช้ SQL เบื้องต้นใน Google Colab

#### การเชื่อมต่อกับฐานข้อมูลใน Google Colab
- Google Colab สามารถเชื่อมต่อกับฐานข้อมูลได้หลายวิธี
- สำหรับการเรียนรู้ เราสามารถใช้ SQLite ซึ่งเป็นฐานข้อมูลแบบไฟล์เดียว

```python
import sqlite3
import pandas as pd

# สร้างการเชื่อมต่อกับฐานข้อมูล SQLite (จะสร้างไฟล์ใหม่ถ้ายังไม่มี)
conn = sqlite3.connect('sample_database.db')

# สร้าง cursor สำหรับการทำงานกับฐานข้อมูล
cursor = conn.cursor()

# สร้างตารางตัวอย่าง
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE,
    age INTEGER,
    city TEXT
)
''')

# สร้างตารางสินค้า
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    price REAL NOT NULL,
    category TEXT
)
''')

# สร้างตารางคำสั่งซื้อ
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    total_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
)
''')

# ยืนยันการเปลี่ยนแปลง
conn.commit()

# เพิ่มข้อมูลตัวอย่างลงในตาราง customers
cursor.executemany('''
INSERT OR IGNORE INTO customers (customer_id, first_name, last_name, email, age, city)
VALUES (?, ?, ?, ?, ?, ?)
''', [
    (1, 'John', 'Smith', 'john.smith@example.com', 35, 'Bangkok'),
    (2, 'Mary', 'Johnson', 'mary.j@example.com', 28, 'Chiang Mai'),
    (3, 'Robert', 'Brown', 'robert.b@example.com', 42, 'Bangkok'),
    (4, 'Linda', 'Davis', 'linda.d@example.com', 31, 'Phuket'),
    (5, 'Michael', 'Wilson', 'michael.w@example.com', 25, 'Bangkok')
])

# เพิ่มข้อมูลตัวอย่างลงในตาราง products
cursor.executemany('''
INSERT OR IGNORE INTO products (product_id, product_name, price, category)
VALUES (?, ?, ?, ?)
''', [
    (1, 'Laptop', 25000, 'Electronics'),
    (2, 'Smartphone', 15000, 'Electronics'),
    (3, 'Headphones', 2500, 'Electronics'),
    (4, 'T-shirt', 500, 'Clothing'),
    (5, 'Jeans', 1200, 'Clothing')
])

# เพิ่มข้อมูลตัวอย่างลงในตาราง orders
cursor.executemany('''
INSERT OR IGNORE INTO orders (order_id, customer_id, order_date, total_amount)
VALUES (?, ?, ?, ?)
''', [
    (1, 1, '2023-01-15', 27500),
    (2, 2, '2023-01-16', 15000),
    (3, 3, '2023-01-20', 2500),
    (4, 1, '2023-02-01', 1700),
    (5, 4, '2023-02-05', 15500),
    (6, 5, '2023-02-10', 25000),
    (7, 3, '2023-02-15', 15000)
])

# ยืนยันการเปลี่ยนแปลง
conn.commit()
```

#### การทดสอบการเชื่อมต่อและแสดงข้อมูล
```python
# ทดสอบค้นหาข้อมูลและแสดงผลด้วย pandas
df_customers = pd.read_sql_query("SELECT * FROM customers", conn)
print("ข้อมูลลูกค้า:")
print(df_customers)

df_products = pd.read_sql_query("SELECT * FROM products", conn)
print("\nข้อมูลสินค้า:")
print(df_products)

df_orders = pd.read_sql_query("SELECT * FROM orders", conn)
print("\nข้อมูลคำสั่งซื้อ:")
print(df_orders)

# ปิดการเชื่อมต่อ
conn.close()
```

### 3. คำสั่ง SELECT พื้นฐาน

#### รูปแบบคำสั่ง SELECT
```sql
SELECT คอลัมน์ที่ต้องการ
FROM ชื่อตาราง
WHERE เงื่อนไข
ORDER BY คอลัมน์ที่ต้องการเรียงลำดับ
LIMIT จำนวนแถวที่ต้องการ;
```

#### การเลือกคอลัมน์ที่ต้องการ
```python
import sqlite3
import pandas as pd

# เชื่อมต่อกับฐานข้อมูล
conn = sqlite3.connect('sample_database.db')

# เลือกทุกคอลัมน์
query1 = "SELECT * FROM customers"
df1 = pd.read_sql_query(query1, conn)
print("เลือกทุกคอลัมน์:")
print(df1)

# เลือกบางคอลัมน์
query2 = "SELECT first_name, last_name, city FROM customers"
df2 = pd.read_sql_query(query2, conn)
print("\nเลือกบางคอลัมน์:")
print(df2)

# เปลี่ยนชื่อคอลัมน์ด้วย AS
query3 = "SELECT first_name AS ชื่อ, last_name AS นามสกุล, city AS เมือง FROM customers"
df3 = pd.read_sql_query(query3, conn)
print("\nเปลี่ยนชื่อคอลัมน์:")
print(df3)

# การใช้ DISTINCT เพื่อเลือกค่าที่ไม่ซ้ำ
query4 = "SELECT DISTINCT city FROM customers"
df4 = pd.read_sql_query(query4, conn)
print("\nเมืองที่ไม่ซ้ำกัน:")
print(df4)
```

#### การคำนวณในคำสั่ง SELECT
```python
# การคำนวณในคำสั่ง SELECT
query5 = "SELECT product_name, price, price * 0.07 AS vat, price * 1.07 AS price_with_vat FROM products"
df5 = pd.read_sql_query(query5, conn)
print("\nการคำนวณในคำสั่ง SELECT:")
print(df5)
```

### 4. การกรองข้อมูลด้วย WHERE

#### รูปแบบการใช้ WHERE
```sql
SELECT คอลัมน์ที่ต้องการ
FROM ชื่อตาราง
WHERE เงื่อนไข;
```

#### ตัวดำเนินการเปรียบเทียบ (Comparison Operators)
- `=` เท่ากับ
- `<>` หรือ `!=` ไม่เท่ากับ
- `>` มากกว่า
- `<` น้อยกว่า
- `>=` มากกว่าหรือเท่ากับ
- `<=` น้อยกว่าหรือเท่ากับ

#### ตัวอย่างการใช้ WHERE
```python
# ตัวอย่างการใช้ WHERE

# กรองลูกค้าที่อยู่ในกรุงเทพ
query6 = "SELECT * FROM customers WHERE city = 'Bangkok'"
df6 = pd.read_sql_query(query6, conn)
print("\nลูกค้าที่อยู่ในกรุงเทพ:")
print(df6)

# กรองสินค้าที่มีราคามากกว่า 10000
query7 = "SELECT * FROM products WHERE price > 10000"
df7 = pd.read_sql_query(query7, conn)
print("\nสินค้าที่มีราคามากกว่า 10000:")
print(df7)

# กรองคำสั่งซื้อที่มียอดรวมระหว่าง 10000 และ 20000
query8 = "SELECT * FROM orders WHERE total_amount >= 10000 AND total_amount <= 20000"
df8 = pd.read_sql_query(query8, conn)
print("\nคำสั่งซื้อที่มียอดรวมระหว่าง 10000 และ 20000:")
print(df8)
```

#### การใช้ AND, OR, NOT
```python
# การใช้ AND, OR, NOT

# ลูกค้าที่อยู่ในกรุงเทพและอายุมากกว่า 30
query9 = "SELECT * FROM customers WHERE city = 'Bangkok' AND age > 30"
df9 = pd.read_sql_query(query9, conn)
print("\nลูกค้าที่อยู่ในกรุงเทพและอายุมากกว่า 30:")
print(df9)

# ลูกค้าที่อยู่ในกรุงเทพหรือเชียงใหม่
query10 = "SELECT * FROM customers WHERE city = 'Bangkok' OR city = 'Chiang Mai'"
df10 = pd.read_sql_query(query10, conn)
print("\nลูกค้าที่อยู่ในกรุงเทพหรือเชียงใหม่:")
print(df10)

# ลูกค้าที่ไม่ได้อยู่ในกรุงเทพ
query11 = "SELECT * FROM customers WHERE NOT city = 'Bangkok'"
df11 = pd.read_sql_query(query11, conn)
print("\nลูกค้าที่ไม่ได้อยู่ในกรุงเทพ:")
print(df11)
```

#### การใช้ BETWEEN, IN, LIKE
```python
# การใช้ BETWEEN, IN, LIKE

# อายุระหว่าง 25 และ 35
query12 = "SELECT * FROM customers WHERE age BETWEEN 25 AND 35"
df12 = pd.read_sql_query(query12, conn)
print("\nลูกค้าที่มีอายุระหว่าง 25 และ 35:")
print(df12)

# เมืองที่อยู่ในรายการที่กำหนด
query13 = "SELECT * FROM customers WHERE city IN ('Bangkok', 'Phuket')"
df13 = pd.read_sql_query(query13, conn)
print("\nลูกค้าที่อยู่ในกรุงเทพหรือภูเก็ต:")
print(df13)

# ชื่อที่ขึ้นต้นด้วย 'M'
query14 = "SELECT * FROM customers WHERE first_name LIKE 'M%'"
df14 = pd.read_sql_query(query14, conn)
print("\nลูกค้าที่ชื่อขึ้นต้นด้วยตัว M:")
print(df14)

# อีเมลที่มีคำว่า 'example.com'
query15 = "SELECT * FROM customers WHERE email LIKE '%example.com'"
df15 = pd.read_sql_query(query15, conn)
print("\nลูกค้าที่มีอีเมลลงท้ายด้วย example.com:")
print(df15)
```

### 5. การจัดเรียงข้อมูลด้วย ORDER BY

#### รูปแบบการใช้ ORDER BY
```sql
SELECT คอลัมน์ที่ต้องการ
FROM ชื่อตาราง
WHERE เงื่อนไข
ORDER BY คอลัมน์ที่ต้องการเรียงลำดับ [ASC|DESC];
```

#### ตัวอย่างการใช้ ORDER BY
```python
# การจัดเรียงข้อมูลด้วย ORDER BY

# เรียงตามอายุจากน้อยไปมาก (ASC)
query16 = "SELECT * FROM customers ORDER BY age ASC"
df16 = pd.read_sql_query(query16, conn)
print("\nลูกค้าเรียงตามอายุจากน้อยไปมาก:")
print(df16)

# เรียงตามอายุจากมากไปน้อย (DESC)
query17 = "SELECT * FROM customers ORDER BY age DESC"
df17 = pd.read_sql_query(query17, conn)
print("\nลูกค้าเรียงตามอายุจากมากไปน้อย:")
print(df17)

# เรียงตามเมืองและอายุ
query18 = "SELECT * FROM customers ORDER BY city ASC, age DESC"
df18 = pd.read_sql_query(query18, conn)
print("\nลูกค้าเรียงตามเมือง และอายุจากมากไปน้อย:")
print(df18)
```

### 6. การจัดกลุ่มข้อมูลด้วย GROUP BY

#### รูปแบบการใช้ GROUP BY
```sql
SELECT คอลัมน์ที่ต้องการ, ฟังก์ชันการรวม(คอลัมน์)
FROM ชื่อตาราง
WHERE เงื่อนไข
GROUP BY คอลัมน์ที่ต้องการจัดกลุ่ม
HAVING เงื่อนไขสำหรับกลุ่ม;
```

#### ฟังก์ชันการรวม (Aggregate Functions)
- `COUNT()` นับจำนวนแถว
- `SUM()` รวมค่า
- `AVG()` ค่าเฉลี่ย
- `MAX()` ค่าสูงสุด
- `MIN()` ค่าต่ำสุด

#### ตัวอย่างการใช้ GROUP BY
```python
# การจัดกลุ่มข้อมูลด้วย GROUP BY

# นับจำนวนลูกค้าในแต่ละเมือง
query19 = "SELECT city, COUNT(*) AS customer_count FROM customers GROUP BY city"
df19 = pd.read_sql_query(query19, conn)
print("\nจำนวนลูกค้าในแต่ละเมือง:")
print(df19)

# หาอายุเฉลี่ยของลูกค้าในแต่ละเมือง
query20 = "SELECT city, AVG(age) AS average_age FROM customers GROUP BY city"
df20 = pd.read_sql_query(query20, conn)
print("\nอายุเฉลี่ยของลูกค้าในแต่ละเมือง:")
print(df20)

# หายอดสั่งซื้อรวมของลูกค้าแต่ละคน
query21 = """
SELECT c.customer_id, c.first_name, c.last_name, SUM(o.total_amount) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY total_spent DESC
"""
df21 = pd.read_sql_query(query21, conn)
print("\nยอดสั่งซื้อรวมของลูกค้าแต่ละคน:")
print(df21)

# หาจำนวนคำสั่งซื้อและยอดรวมในแต่ละเดือน
query22 = """
SELECT substr(order_date, 1, 7) AS month, 
       COUNT(*) AS order_count, 
       SUM(total_amount) AS total_sales
FROM orders
GROUP BY month
ORDER BY month
"""
df22 = pd.read_sql_query(query22, conn)
print("\nจำนวนคำสั่งซื้อและยอดรวมในแต่ละเดือน:")
print(df22)
```

#### การใช้ HAVING
```python
# การใช้ HAVING เพื่อกรองผลลัพธ์หลังการจัดกลุ่ม

# เมืองที่มีลูกค้ามากกว่า 1 คน
query23 = """
SELECT city, COUNT(*) AS customer_count 
FROM customers 
GROUP BY city 
HAVING customer_count > 1
"""
df23 = pd.read_sql_query(query23, conn)
print("\nเมืองที่มีลูกค้ามากกว่า 1 คน:")
print(df23)

# ลูกค้าที่มียอดสั่งซื้อรวมมากกว่า 20000
query24 = """
SELECT c.customer_id, c.first_name, c.last_name, SUM(o.total_amount) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
HAVING total_spent > 20000
ORDER BY total_spent DESC
"""
df24 = pd.read_sql_query(query24, conn)
print("\nลูกค้าที่มียอดสั่งซื้อรวมมากกว่า 20000:")
print(df24)

# ปิดการเชื่อมต่อ
conn.close()
```

### 7. ฟังก์ชันที่ใช้บ่อยใน SQL

#### ฟังก์ชันเกี่ยวกับข้อความ (String Functions)
- `UPPER()` แปลงเป็นตัวพิมพ์ใหญ่
- `LOWER()` แปลงเป็นตัวพิมพ์เล็ก
- `LENGTH()` หาความยาวของข้อความ
- `SUBSTR()` หาข้อความย่อย
- `TRIM()` ตัดช่องว่างที่อยู่ต้นและท้ายข้อความ
- `CONCAT()` หรือ `||` รวมข้อความ

```python
# เชื่อมต่อกับฐานข้อมูล
conn = sqlite3.connect('sample_database.db')

# ฟังก์ชันเกี่ยวกับข้อความ
query25 = """
SELECT 
    first_name,
    UPPER(first_name) AS upper_name,
    LOWER(first_name) AS lower_name,
    LENGTH(first_name) AS name_length,
    SUBSTR(first_name, 1, 3) AS name_substring,
    first_name || ' ' || last_name AS full_name
FROM customers
"""
df25 = pd.read_sql_query(query25, conn)
print("\nฟังก์ชันเกี่ยวกับข้อความ:")
print(df25)
```

#### ฟังก์ชันเกี่ยวกับตัวเลข (Numeric Functions)
- `ROUND()` ปัดทศนิยม
- `ABS()` ค่าสัมบูรณ์
- `RANDOM()` สุ่มตัวเลข

```python
# ฟังก์ชันเกี่ยวกับตัวเลข
query26 = """
SELECT 
    product_name,
    price,
    ROUND(price, 0) AS price_rounded,
    ABS(price - 10000) AS price_difference,
    RANDOM() AS random_value
FROM products
"""
df26 = pd.read_sql_query(query26, conn)
print("\nฟังก์ชันเกี่ยวกับตัวเลข:")
print(df26)
```

#### ฟังก์ชันเกี่ยวกับวันที่ (Date Functions)
- `DATE()` แปลงเป็นวันที่
- `STRFTIME()` จัดรูปแบบวันที่และเวลา

```python
# ฟังก์ชันเกี่ยวกับวันที่
query27 = """
SELECT 
    order_id,
    order_date,
    STRFTIME('%Y', order_date) AS year,
    STRFTIME('%m', order_date) AS month,
    STRFTIME('%d', order_date) AS day
FROM orders
"""
df27 = pd.read_sql_query(query27, conn)
print("\nฟังก์ชันเกี่ยวกับวันที่:")
print(df27)

# ปิดการเชื่อมต่อ
conn.close()
```

### 8. Workshop: การใช้ SQL ใน Google Colab

#### กรณีศึกษา: การวิเคราะห์ข้อมูลการขาย

```python
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# เชื่อมต่อกับฐานข้อมูล
conn = sqlite3.connect('sample_database.db')

# สร้างตารางใหม่สำหรับรายละเอียดคำสั่งซื้อ
cursor = conn.cursor()

# สร้างตารางรายละเอียดคำสั่งซื้อ
cursor.execute('''
CREATE TABLE IF NOT EXISTS order_details (
    order_detail_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    subtotal REAL,
    FOREIGN KEY (order_id) REFERENCES orders (order_id),
    FOREIGN KEY (product_id) REFERENCES products (product_id)
)
''')

# เพิ่มข้อมูลตัวอย่างลงในตาราง order_details
cursor.executemany('''
INSERT OR IGNORE INTO order_details (order_detail_id, order_id, product_id, quantity, subtotal)
VALUES (?, ?, ?, ?, ?)
''', [
    (1, 1, 1, 1, 25000),
    (2, 1, 3, 1, 2500),
    (3, 2, 2, 1, 15000),
    (4, 3, 3, 1, 2500),
    (5, 4, 4, 2, 1000),
    (6, 4, 5, 1, 700),
    (7, 5, 2, 1, 15000),
    (8, 5, 3, 1, 500),
    (9, 6, 1, 1, 25000),
    (10, 7, 2, 1, 15000)
])

# ยืนยันการเปลี่ยนแปลง
conn.commit()

# ตรวจสอบข้อมูลที่เพิ่ม
df_details = pd.read_sql_query("SELECT * FROM order_details", conn)
print("ข้อมูลรายละเอียดคำสั่งซื้อ:")
print(df_details)

# 1. วิเคราะห์ยอดขายตามประเภทสินค้า
query_1 = """
SELECT 
    p.category,
    SUM(od.subtotal) AS total_sales
FROM 
    order_details od
JOIN 
    products p ON od.product_id = p.product_id
GROUP BY 
    p.category
ORDER BY 
    total_sales DESC
"""
df_sales_by_category = pd.read_sql_query(query_1, conn)
print("\n1. ยอดขายตามประเภทสินค้า:")
print(df_sales_by_category)

# แสดงกราฟแท่งยอดขายตามประเภทสินค้า
plt.figure(figsize=(10, 6))
plt.bar(df_sales_by_category['category'], df_sales_by_category['total_sales'])
plt.title('ยอดขายตามประเภทสินค้า')
plt.xlabel('ประเภทสินค้า')
plt.ylabel('ยอดขาย (บาท)')
plt.show()

# 2. วิเคราะห์สินค้าขายดี
query_2 = """
SELECT 
    p.product_name,
    SUM(od.quantity) AS total_quantity,
    SUM(od.subtotal) AS total_sales
FROM 
    order_details od
JOIN 
    products p ON od.product_id = p.product_id
GROUP BY 
    p.product_id
ORDER BY 
    total_quantity DESC
"""
df_top_products = pd.read_sql_query(query_2, conn)
print("\n2. สินค้าขายดี:")
print(df_top_products)

# 3. วิเคราะห์ลูกค้าที่มียอดสั่งซื้อสูงสุด
query_3 = """
SELECT 
    c.first_name || ' ' || c.last_name AS customer_name,
    c.city,
    COUNT(o.order_id) AS order_count,
    SUM(o.total_amount) AS total_spent
FROM 
    customers c
JOIN 
    orders o ON c.customer_id = o.customer_id
GROUP BY 
    c.customer_id
ORDER BY 
    total_spent DESC
"""
df_top_customers = pd.read_sql_query(query_3, conn)
print("\n3. ลูกค้าที่มียอดสั่งซื้อสูงสุด:")
print(df_top_customers)

# 4. วิเคราะห์ยอดขายตามเมือง
query_4 = """
SELECT 
    c.city,
    COUNT(o.order_id) AS order_count,
    SUM(o.total_amount) AS total_sales
FROM 
    customers c
JOIN 
    orders o ON c.customer_id = o.customer_id
GROUP BY 
    c.city
ORDER BY 
    total_sales DESC
"""
df_sales_by_city = pd.read_sql_query(query_4, conn)
print("\n4. ยอดขายตามเมือง:")
print(df_sales_by_city)

# แสดงกราฟวงกลมยอดขายตามเมือง
plt.figure(figsize=(10, 6))
plt.pie(df_sales_by_city['total_sales'], labels=df_sales_by_city['city'], autopct='%1.1f%%')
plt.title('สัดส่วนยอดขายตามเมือง')
plt.axis('equal')
plt.show()

# 5. วิเคราะห์แนวโน้มยอดขายตามเดือน
query_5 = """
SELECT 
    substr(order_date, 1, 7) AS month,
    COUNT(order_id) AS order_count,
    SUM(total_amount) AS total_sales
FROM 
    orders
GROUP BY 
    month
ORDER BY 
    month
"""
df_sales_by_month = pd.read_sql_query(query_5, conn)
print("\n5. แนวโน้มยอดขายตามเดือน:")
print(df_sales_by_month)

# แสดงกราฟเส้นแนวโน้มยอดขายตามเดือน
plt.figure(figsize=(10, 6))
plt.plot(df_sales_by_month['month'], df_sales_by_month['total_sales'], marker='o')
plt.title('แนวโน้มยอดขายตามเดือน')
plt.xlabel('เดือน')
plt.ylabel('ยอดขาย (บาท)')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# ปิดการเชื่อมต่อ
conn.close()
```

## แนวทางการนำเสนอ
- สอนแบบ hands-on โดยให้ผู้เข้าอบรมพิมพ์ตามและทดลองเปลี่ยนคำสั่ง SQL
- แสดงผลลัพธ์ของคำสั่ง SQL ทันทีเพื่อให้เห็นผลลัพธ์ที่ได้
- อธิบายหลักการและเหตุผลของแต่ละคำสั่ง
- เน้นตัวอย่างที่เกี่ยวข้องกับข้อมูลธุรกิจที่พบได้ในชีวิตจริง
- ให้ผู้เข้าอบรมทดลองเขียนคำสั่ง SQL ด้วยตนเองในช่วง Workshop
- เปิดโอกาสให้ซักถามและแก้ไขปัญหาที่พบระหว่างการฝึกปฏิบัติ