# พื้นฐาน Python สำหรับการวิเคราะห์ข้อมูล

## เนื้อหาสำหรับการนำเสนอ

### 1. แนะนำ Google Colab สำหรับการเขียนโค้ด Python

#### Google Colab คืออะไร
- แพลตฟอร์มสำหรับการเขียนและรันโค้ด Python บนคลาวด์
- พัฒนาโดย Google Research
- ใช้งานได้ฟรีผ่านเว็บเบราว์เซอร์
- ไม่ต้องติดตั้งโปรแกรมใดๆ บนเครื่องคอมพิวเตอร์

#### ข้อดีของ Google Colab
- มาพร้อมกับไลบรารีสำหรับการวิเคราะห์ข้อมูลที่ติดตั้งไว้แล้ว (pandas, numpy, matplotlib, etc.)
- มี GPU และ TPU ฟรีสำหรับการประมวลผลที่ซับซ้อน
- สามารถแชร์และทำงานร่วมกันได้ง่าย
- บันทึกอัตโนมัติใน Google Drive
- เชื่อมต่อกับ Google Drive, GitHub และแหล่งข้อมูลอื่นๆ ได้

#### ส่วนประกอบของ Google Colab
- **Notebooks**: ไฟล์ที่รวมทั้งโค้ดและเอกสารไว้ด้วยกัน
- **Cells**: แต่ละส่วนของ Notebook แบ่งเป็น:
  - **Code Cells**: สำหรับเขียนและรันโค้ด Python
  - **Text Cells**: สำหรับเขียนคำอธิบายในรูปแบบ Markdown
- **Runtime**: สภาพแวดล้อมสำหรับรันโค้ด Python

#### วิธีการใช้งาน Google Colab
- การสร้าง Notebook ใหม่
- การเพิ่ม Code Cell และ Text Cell
- การรันโค้ด (Run Cell)
- การบันทึกและดาวน์โหลด Notebook
- การเชื่อมต่อกับ Google Drive
- การนำเข้าและส่งออกข้อมูล

### 2. พื้นฐาน Python ที่จำเป็นสำหรับการวิเคราะห์ข้อมูล

#### ตัวแปรและประเภทข้อมูล

##### การประกาศตัวแปรใน Python
```python
# การประกาศตัวแปร
name = "John"  # ตัวแปรประเภท string
age = 30       # ตัวแปรประเภท integer
height = 175.5 # ตัวแปรประเภท float
is_student = True  # ตัวแปรประเภท boolean

# การแสดงค่าตัวแปร
print(name)
print(f"อายุ: {age}, ส่วนสูง: {height} cm")

# การตรวจสอบประเภทข้อมูล
print(type(name))     # <class 'str'>
print(type(age))      # <class 'int'>
print(type(height))   # <class 'float'>
print(type(is_student))  # <class 'bool'>
```

##### ประเภทข้อมูลพื้นฐานใน Python
- **int**: ตัวเลขจำนวนเต็ม เช่น 1, 100, -10
- **float**: ตัวเลขทศนิยม เช่น 3.14, 2.5, -0.7
- **str**: ข้อความ เช่น "Hello", 'Python'
- **bool**: ค่าความจริง (True หรือ False)
- **None**: ค่าว่าง (Null)

##### การแปลงประเภทข้อมูล
```python
# แปลงเป็น int
x = int("10")      # str -> int: 10
y = int(10.9)      # float -> int: 10 (ตัดทศนิยม)

# แปลงเป็น float
a = float("3.14")  # str -> float: 3.14
b = float(5)       # int -> float: 5.0

# แปลงเป็น string
c = str(42)        # int -> str: "42"
d = str(3.14)      # float -> str: "3.14"

# แปลงเป็น boolean
e = bool(1)        # int -> bool: True
f = bool(0)        # int -> bool: False
g = bool("")       # str -> bool: False (string ว่าง)
h = bool("hello")  # str -> bool: True (string ไม่ว่าง)
```

#### ลิสต์และดิกชันนารี

##### ลิสต์ (List)
- โครงสร้างข้อมูลสำหรับเก็บข้อมูลหลายค่าในตัวแปรเดียว
- สามารถเก็บข้อมูลต่างประเภทได้
- มีลำดับ (Ordered) และแก้ไขได้ (Mutable)

```python
# การสร้างลิสต์
fruits = ["apple", "banana", "orange"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

# การเข้าถึงสมาชิกในลิสต์
print(fruits[0])   # "apple" (index เริ่มที่ 0)
print(fruits[-1])  # "orange" (index ติดลบนับจากท้าย)

# การใช้ slicing
print(numbers[1:3])  # [2, 3] (เริ่มที่ index 1 จนถึง 3-1)

# การเปลี่ยนค่าในลิสต์
fruits[1] = "mango"
print(fruits)  # ["apple", "mango", "orange"]

# การหาความยาวของลิสต์
print(len(fruits))  # 3

# การเพิ่มสมาชิกในลิสต์
fruits.append("grape")  # เพิ่มที่ท้ายลิสต์
print(fruits)  # ["apple", "mango", "orange", "grape"]

# การลบสมาชิกในลิสต์
fruits.remove("mango")  # ลบตามค่า
print(fruits)  # ["apple", "orange", "grape"]

del fruits[0]  # ลบตาม index
print(fruits)  # ["orange", "grape"]
```

##### ดิกชันนารี (Dictionary)
- โครงสร้างข้อมูลสำหรับเก็บข้อมูลในรูปแบบคู่ key-value
- key ต้องไม่ซ้ำกันและไม่สามารถเปลี่ยนแปลงได้ (immutable)
- ไม่มีลำดับที่แน่นอน

```python
# การสร้างดิกชันนารี
person = {
    "name": "John",
    "age": 30,
    "city": "Bangkok",
    "is_student": False
}

# การเข้าถึงค่าใน dictionary
print(person["name"])   # "John"
print(person.get("age"))  # 30

# การเปลี่ยนค่าใน dictionary
person["age"] = 31
print(person)  # {"name": "John", "age": 31, "city": "Bangkok", "is_student": False}

# การเพิ่ม key-value ใหม่
person["email"] = "john@example.com"
print(person)  # {"name": "John", "age": 31, "city": "Bangkok", "is_student": False, "email": "john@example.com"}

# การลบ key-value
del person["is_student"]
print(person)  # {"name": "John", "age": 31, "city": "Bangkok", "email": "john@example.com"}

# การตรวจสอบว่ามี key ใน dictionary หรือไม่
print("name" in person)  # True
print("phone" in person)  # False

# การวนลูปผ่าน keys และ values
for key in person:
    print(key, ":", person[key])

# หรือใช้ .items() เพื่อวนลูปผ่านทั้ง key และ value
for key, value in person.items():
    print(key, ":", value)
```

#### การเขียนเงื่อนไขและลูป

##### การเขียนเงื่อนไข (Conditional Statements)
```python
# if, else, elif

age = 18

if age < 13:
    print("เด็ก")
elif age < 18:
    print("วัยรุ่น")
else:
    print("ผู้ใหญ่")  # จะแสดงผลนี้

# การใช้ and, or, not
temperature = 25
humidity = 80

if temperature > 30 and humidity > 70:
    print("ร้อนและชื้น")
elif temperature > 30 or humidity > 70:
    print("ร้อนหรือชื้น")  # จะแสดงผลนี้
else:
    print("สภาพอากาศปกติ")

# การใช้ in กับ list
fruits = ["apple", "banana", "orange"]
if "banana" in fruits:
    print("มีกล้วย")  # จะแสดงผลนี้
```

##### การเขียนลูป (Loops)
```python
# for loop กับ list
fruits = ["apple", "banana", "orange"]
for fruit in fruits:
    print(fruit)
# apple
# banana
# orange

# for loop กับ range
for i in range(5):  # range(5) = 0, 1, 2, 3, 4
    print(i)
# 0
# 1
# 2
# 3
# 4

# for loop กับ dictionary
person = {"name": "John", "age": 30, "city": "Bangkok"}
for key in person:
    print(key, ":", person[key])
# name : John
# age : 30
# city : Bangkok

# while loop
count = 0
while count < 5:
    print(count)
    count += 1
# 0
# 1
# 2
# 3
# 4

# break และ continue
for i in range(10):
    if i == 3:
        continue  # ข้ามการทำงานที่เหลือในลูปนี้และไปทำลูปถัดไป
    if i == 7:
        break  # ออกจากลูปทันที
    print(i)
# 0
# 1
# 2
# 4
# 5
# 6
```

### 3. การนำเข้าไลบรารี Python สำหรับการวิเคราะห์ข้อมูล

#### ไลบรารีพื้นฐานที่ใช้บ่อยในการวิเคราะห์ข้อมูล

##### NumPy: ไลบรารีสำหรับการคำนวณเชิงตัวเลข
```python
import numpy as np

# สร้าง array
arr = np.array([1, 2, 3, 4, 5])
print(arr)  # [1 2 3 4 5]

# การคำนวณพื้นฐาน
print(np.mean(arr))  # ค่าเฉลี่ย: 3.0
print(np.std(arr))   # ส่วนเบี่ยงเบนมาตรฐาน: 1.4142...
print(np.sum(arr))   # ผลรวม: 15
print(np.max(arr))   # ค่าสูงสุด: 5
print(np.min(arr))   # ค่าต่ำสุด: 1

# การสร้าง array ขนาดใหญ่
zeros = np.zeros(5)  # [0. 0. 0. 0. 0.]
ones = np.ones(5)    # [1. 1. 1. 1. 1.]
rng = np.arange(0, 10, 2)  # [0 2 4 6 8]

# การคำนวณกับ array
arr2 = arr * 2       # [2 4 6 8 10]
arr3 = arr + arr2    # [3 6 9 12 15]
```

##### Pandas: ไลบรารีสำหรับการจัดการและวิเคราะห์ข้อมูล
```python
import pandas as pd

# สร้าง DataFrame
data = {
    'Name': ['John', 'Anna', 'Peter', 'Linda'],
    'Age': [28, 34, 29, 42],
    'City': ['New York', 'Paris', 'Berlin', 'London']
}
df = pd.DataFrame(data)
print(df)
#     Name  Age      City
# 0   John   28  New York
# 1   Anna   34     Paris
# 2  Peter   29    Berlin
# 3  Linda   42    London

# การเข้าถึงข้อมูลใน DataFrame
print(df['Name'])  # เข้าถึงคอลัมน์ 'Name'
print(df.iloc[0])  # เข้าถึงแถวที่ 0

# การกรองข้อมูล
adults = df[df['Age'] > 30]
print(adults)
#     Name  Age    City
# 1   Anna   34   Paris
# 3  Linda   42  London

# การสรุปข้อมูล
print(df.describe())  # สถิติเชิงพรรณนาของข้อมูลตัวเลข
print(df['Age'].mean())  # ค่าเฉลี่ยของอายุ: 33.25
```

##### Matplotlib: ไลบรารีสำหรับการสร้างกราฟและการแสดงผลข้อมูล
```python
import matplotlib.pyplot as plt

# สร้างข้อมูลตัวอย่าง
x = [1, 2, 3, 4, 5]
y = [10, 15, 13, 18, 20]

# สร้างกราฟเส้น
plt.figure(figsize=(8, 4))  # กำหนดขนาดรูป
plt.plot(x, y, 'b-o')  # 'b-o' คือ blue line with circle markers
plt.title('ตัวอย่างกราฟเส้น')
plt.xlabel('แกน X')
plt.ylabel('แกน Y')
plt.grid(True)
plt.show()

# สร้างกราฟแท่ง
plt.figure(figsize=(8, 4))
plt.bar(x, y, color='green')
plt.title('ตัวอย่างกราฟแท่ง')
plt.xlabel('แกน X')
plt.ylabel('แกน Y')
plt.show()
```

### 4. ตัวอย่างการใช้งาน Python สำหรับการวิเคราะห์ข้อมูลพื้นฐาน

#### การนำเข้าข้อมูลจาก CSV

```python
import pandas as pd

# นำเข้าข้อมูล CSV
df = pd.read_csv('sales_data.csv')

# แสดง 5 แถวแรก
print(df.head())

# ตรวจสอบขนาดของข้อมูล
print(df.shape)  # (จำนวนแถว, จำนวนคอลัมน์)

# ตรวจสอบประเภทข้อมูลในแต่ละคอลัมน์
print(df.dtypes)

# ตรวจสอบข้อมูลเบื้องต้น
print(df.info())  # แสดงข้อมูลทั่วไปของ DataFrame
print(df.describe())  # สถิติเชิงพรรณนาของคอลัมน์ตัวเลข
```

#### การจัดการข้อมูลที่ขาดหาย (Missing Data)

```python
import pandas as pd
import numpy as np

# สร้างข้อมูลที่มีค่าขาดหาย
data = {
    'A': [1, 2, np.nan, 4],
    'B': [5, np.nan, np.nan, 8],
    'C': [9, 10, 11, 12]
}
df = pd.DataFrame(data)
print(df)
#      A    B   C
# 0  1.0  5.0   9
# 1  2.0  NaN  10
# 2  NaN  NaN  11
# 3  4.0  8.0  12

# ตรวจสอบข้อมูลที่ขาดหาย
print(df.isnull())  # แสดงเป็น True ถ้าเป็นค่า NaN
print(df.isnull().sum())  # นับจำนวนค่า NaN ในแต่ละคอลัมน์

# วิธีการจัดการกับข้อมูลที่ขาดหาย
df_dropna = df.dropna()  # ลบแถวที่มีค่า NaN
print(df_dropna)

df_fillna = df.fillna(0)  # แทนที่ค่า NaN ด้วย 0
print(df_fillna)

df_fillna_mean = df.fillna(df.mean())  # แทนที่ค่า NaN ด้วยค่าเฉลี่ยของคอลัมน์
print(df_fillna_mean)
```

#### การวิเคราะห์ข้อมูลพื้นฐาน

```python
import pandas as pd
import matplotlib.pyplot as plt

# สร้างข้อมูลตัวอย่าง
data = {
    'Product': ['A', 'B', 'C', 'D', 'E'],
    'Sales': [100, 150, 80, 200, 120],
    'Profit': [20, 30, 15, 40, 25]
}
df = pd.DataFrame(data)

# การคำนวณสถิติพื้นฐาน
print("ยอดขายเฉลี่ย:", df['Sales'].mean())
print("กำไรเฉลี่ย:", df['Profit'].mean())
print("ยอดขายสูงสุด:", df['Sales'].max())
print("กำไรต่ำสุด:", df['Profit'].min())
print("ส่วนเบี่ยงเบนมาตรฐานของยอดขาย:", df['Sales'].std())

# การหาความสัมพันธ์ระหว่างยอดขายและกำไร
correlation = df['Sales'].corr(df['Profit'])
print("ค่าสหสัมพันธ์ระหว่างยอดขายและกำไร:", correlation)

# การสร้างกราฟแท่งเปรียบเทียบยอดขายและกำไร
df.plot(x='Product', y=['Sales', 'Profit'], kind='bar', figsize=(10, 6))
plt.title('ยอดขายและกำไรตามประเภทสินค้า')
plt.xlabel('สินค้า')
plt.ylabel('จำนวน')
plt.legend(['ยอดขาย', 'กำไร'])
plt.xticks(rotation=0)
plt.show()
```

### 5. Workshop: การวิเคราะห์ข้อมูลด้วย Python ใน Google Colab

#### ขั้นตอนการทำ Workshop
1. เปิด Google Colab และสร้าง Notebook ใหม่
2. นำเข้าไลบรารีที่จำเป็น (pandas, numpy, matplotlib)
3. นำเข้าชุดข้อมูลตัวอย่าง
4. ทำความสะอาดข้อมูลเบื้องต้น
5. วิเคราะห์ข้อมูลและสร้างกราฟแสดงผล
6. แปลความหมายจากผลลัพธ์

#### ตัวอย่างโค้ด Workshop

```python
# 1. นำเข้าไลบรารีที่จำเป็น
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 2. นำเข้าชุดข้อมูลตัวอย่าง (เช่น Titanic Dataset)
# สามารถใช้ชุดข้อมูลที่มีอยู่ใน seaborn
titanic = sns.load_dataset('titanic')

# 3. สำรวจข้อมูลเบื้องต้น
print(titanic.head())
print(titanic.info())
print(titanic.describe())

# 4. ทำความสะอาดข้อมูล
# ตรวจสอบข้อมูลที่ขาดหาย
print(titanic.isnull().sum())

# เติมค่าที่ขาดหายในคอลัมน์ 'age' ด้วยค่าเฉลี่ย
titanic['age'].fillna(titanic['age'].mean(), inplace=True)

# ลบคอลัมน์ที่ไม่จำเป็นหรือมีข้อมูลขาดหายมาก
titanic.drop(['deck', 'embark_town'], axis=1, inplace=True)

# 5. วิเคราะห์ข้อมูล
# วิเคราะห์อัตราการรอดชีวิตโดยรวม
survival_rate = titanic['survived'].mean() * 100
print(f"อัตราการรอดชีวิตโดยรวม: {survival_rate:.2f}%")

# วิเคราะห์อัตราการรอดชีวิตตามเพศ
survival_by_sex = titanic.groupby('sex')['survived'].mean() * 100
print("อัตราการรอดชีวิตตามเพศ:")
print(survival_by_sex)

# วิเคราะห์อัตราการรอดชีวิตตามชั้นโดยสาร
survival_by_class = titanic.groupby('class')['survived'].mean() * 100
print("อัตราการรอดชีวิตตามชั้นโดยสาร:")
print(survival_by_class)

# 6. แสดงผลด้วยกราฟ
# กราฟแท่งแสดงอัตราการรอดชีวิตตามเพศ
plt.figure(figsize=(10, 6))
sns.barplot(x='sex', y='survived', data=titanic)
plt.title('อัตราการรอดชีวิตตามเพศ')
plt.xlabel('เพศ')
plt.ylabel('อัตราการรอดชีวิต')
plt.show()

# กราฟแท่งแสดงอัตราการรอดชีวิตตามชั้นโดยสาร
plt.figure(figsize=(10, 6))
sns.barplot(x='class', y='survived', data=titanic)
plt.title('อัตราการรอดชีวิตตามชั้นโดยสาร')
plt.xlabel('ชั้นโดยสาร')
plt.ylabel('อัตราการรอดชีวิต')
plt.show()

# กราฟกระจายแสดงความสัมพันธ์ระหว่างอายุและค่าโดยสาร
plt.figure(figsize=(10, 6))
sns.scatterplot(x='age', y='fare', hue='survived', data=titanic)
plt.title('ความสัมพันธ์ระหว่างอายุและค่าโดยสาร แยกตามการรอดชีวิต')
plt.xlabel('อายุ (ปี)')
plt.ylabel('ค่าโดยสาร')
plt.legend(title='รอดชีวิต', labels=['ไม่รอด', 'รอด'])
plt.show()
```

## แนวทางการนำเสนอ
- ใช้การสอนแบบ hands-on โดยให้ผู้เข้าอบรมทำตามไปพร้อมกัน
- แสดงตัวอย่างการเขียนโค้ดจริงบน Google Colab
- เน้นการเรียนรู้ผ่านการปฏิบัติ (Learning by Doing)
- ใช้ตัวอย่างจากข้อมูลจริงที่เข้าใจง่าย
- ให้ผู้เข้าอบรมทดลองเขียนโค้ดด้วยตนเองในส่วนของ Workshop
- เปิดโอกาสให้ถามคำถามและช่วยแก้ไขปัญหาระหว่างการฝึกปฏิบัติ