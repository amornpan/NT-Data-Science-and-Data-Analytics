# วิธีแสดงแผนภาพ Mermaid ใน Google Colab

Google Colab ไม่รองรับการแสดงผลแผนภาพ Mermaid โดยตรง แต่เราสามารถใช้วิธีการแสดงผลผ่าน URL จาก mermaid.ink แทน

## วิธีที่ 1: ใช้โค้ดแปลง Mermaid เป็น URL

```python
# โค้ด Mermaid ที่ต้องการแสดงผล
mermaid_code = """
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
"""

# แปลงเป็น URL
import base64
import zlib

encoded_data = base64.urlsafe_b64encode(
    zlib.compress(mermaid_code.encode('utf-8'), 9)
).decode('ascii')

mermaid_url = f"https://mermaid.ink/img/pako:{encoded_data}"

# แสดงแผนภาพ
from IPython.display import Image
Image(mermaid_url)
```

## วิธีที่ 2: ใช้ Mermaid Live Editor

1. ไปที่ [Mermaid Live Editor](https://mermaid.live/)
2. ใส่โค้ด Mermaid ของคุณ
3. คลิกที่ "Share" และคัดลอก URL ของรูปภาพ
4. นำ URL มาใช้ใน Google Colab:

```python
from IPython.display import Image
Image("https://mermaid.ink/img/pako:...")  # URL ที่ได้จาก Mermaid Live Editor
```

## วิธีที่ 3: อัพโหลดรูปภาพ

1. สร้างแผนภาพด้วย [Mermaid Live Editor](https://mermaid.live/)
2. ดาวน์โหลดเป็นรูปภาพ PNG หรือ SVG
3. อัพโหลดรูปภาพลงใน Google Colab:

```python
from google.colab import files
uploaded = files.upload()  # อัพโหลดไฟล์รูปภาพ

from IPython.display import Image
Image('ชื่อไฟล์ที่อัพโหลด.png')  # แสดงรูปภาพ
```

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
