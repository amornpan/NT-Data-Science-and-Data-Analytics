# วิธีแสดงแผนภาพ Mermaid เป็น SVG ใน Google Colab

Google Colab ไม่รองรับการแสดงผลแผนภาพ Mermaid โดยตรง แต่เราสามารถแสดงผลเป็น SVG ได้ซึ่งมีคุณภาพสูงกว่าและสามารถขยายได้โดยไม่แตก

## วิธีที่แนะนำ: ใช้ mermaid_svg_helper.py

เราได้เตรียมไฟล์ `mermaid_svg_helper.py` ที่มีฟังก์ชัน `display_mermaid_as_svg()` ไว้ให้คุณแล้ว

### ขั้นตอนการใช้งาน:

1. **ดาวน์โหลด mermaid_svg_helper.py จาก GitHub**:
   ```python
   # ดาวน์โหลดไฟล์ mermaid_svg_helper.py จาก GitHub
   !wget https://raw.githubusercontent.com/amornpan/NT-Data-Science-and-Data-Analytics/master/mermaid_svg_helper.py
   ```

2. **ใช้ฟังก์ชัน display_mermaid_as_svg**:
   ```python
   from mermaid_svg_helper import display_mermaid_as_svg
   
   # โค้ด Mermaid ที่ต้องการแสดงผล
   mermaid_code = """
   erDiagram
       CUSTOMERS ||--o{ ORDERS : places
       ORDERS ||--o{ ORDER_ITEMS : contains
       PRODUCTS ||--o{ ORDER_ITEMS : included_in
   """
   
   # แสดงแผนภาพเป็น SVG
   display_mermaid_as_svg(mermaid_code)
   ```

## วิธีอื่นๆ:

### วิธีที่ 1: แปลงเป็น SVG ด้วยโค้ด

```python
# โค้ด Mermaid ที่ต้องการแสดงผล
mermaid_code = """
erDiagram
    CUSTOMERS ||--o{ ORDERS : places
    ORDERS ||--o{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : included_in
"""

# แปลงเป็น URL สำหรับ SVG
import base64
import zlib
import requests
from IPython.display import SVG

encoded_data = base64.urlsafe_b64encode(
    zlib.compress(mermaid_code.encode('utf-8'), 9)
).decode('ascii')

mermaid_svg_url = f"https://mermaid.ink/svg/pako:{encoded_data}"

# ดึงเนื้อหา SVG
response = requests.get(mermaid_svg_url)
svg_content = response.text

# แสดงผล SVG
SVG(data=svg_content)
```

### วิธีที่ 2: ใช้ Mermaid Live Editor

1. ไปที่ [Mermaid Live Editor](https://mermaid.live/)
2. คัดลอกโค้ด Mermaid ของคุณลงไป
3. คลิกที่ "Share" ด้านบนขวา
4. คลิกที่ "SVG" และคัดลอก URL
5. นำ URL มาใช้ใน Colab:

```python
import requests
from IPython.display import SVG

# ดึงเนื้อหา SVG จาก URL
response = requests.get("https://mermaid.ink/svg/...")
svg_content = response.text

# แสดงผล SVG
SVG(data=svg_content)
```

### วิธีที่ 3: บันทึกเป็นไฟล์ SVG และอัพโหลด

1. ไปที่ [Mermaid Live Editor](https://mermaid.live/)
2. คัดลอกโค้ด Mermaid ของคุณลงไป
3. คลิก "Download SVG"
4. อัพโหลดไฟล์ SVG ลงใน Colab:

```python
from google.colab import files
uploaded = files.upload()  # เลือกไฟล์ SVG ที่ดาวน์โหลดไว้

# แสดงไฟล์ SVG
from IPython.display import SVG
filename = next(iter(uploaded.keys()))  # รับชื่อไฟล์ที่อัพโหลด
SVG(filename=filename)
```

## ข้อดีของการใช้ SVG เทียบกับ PNG

1. **คุณภาพสูง**: SVG เป็นกราฟิกแบบเวกเตอร์ สามารถขยายได้โดยไม่แตกหรือมีขอบไม่ชัด
2. **ไฟล์ขนาดเล็กกว่า**: โดยเฉพาะสำหรับแผนภาพที่ไม่ซับซ้อนมาก
3. **แก้ไขได้**: คุณสามารถแก้ไขโค้ด SVG ได้โดยตรงในกรณีที่ต้องการปรับแต่งเพิ่มเติม
4. **ขยายได้**: SVG สามารถขยายได้ไม่จำกัดโดยไม่สูญเสียคุณภาพ เหมาะสำหรับการนำเสนอบนหน้าจอขนาดต่างๆ

## ตัวอย่างโค้ด Mermaid สำหรับแผนภาพ ER

```
erDiagram
    CUSTOMERS ||--o{ ORDERS : places
    ORDERS ||--o{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : included_in
    
    CUSTOMERS {
        int customer_id PK
        string first_name
        string last_name
        string email
        string phone
    }
    
    PRODUCTS {
        int product_id PK
        string product_name
        string category
        float price
        int stock
    }
    
    ORDERS {
        int order_id PK
        int customer_id FK
        date order_date
        float total_amount
    }
    
    ORDER_ITEMS {
        int order_item_id PK
        int order_id FK
        int product_id FK
        int quantity
        float price
    }
```
