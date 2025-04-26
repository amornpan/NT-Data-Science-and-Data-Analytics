# การแสดงแผนภาพ Mermaid ใน Google Colab

Google Colab ไม่รองรับการแสดงผลแผนภาพ Mermaid โดยตรง แต่มีวิธีแก้ไขดังนี้

## วิธีที่แนะนำ: ใช้ mermaid_helper.py

ผมได้สร้างไฟล์ `mermaid_helper.py` ที่มีฟังก์ชัน `display_mermaid()` ไว้ให้คุณแล้ว

### ขั้นตอนการใช้งาน:

1. **อัพโหลด mermaid_helper.py ไปยัง Google Colab**:
   ```python
   # อัพโหลดไฟล์ mermaid_helper.py
   from google.colab import files
   uploaded = files.upload()  # เลือกไฟล์ mermaid_helper.py
   ```

2. **ใช้ฟังก์ชัน display_mermaid**:
   ```python
   from mermaid_helper import display_mermaid
   
   # โค้ด Mermaid ที่ต้องการแสดงผล
   mermaid_code = """
   erDiagram
       CUSTOMERS ||--o{ ORDERS : places
       ORDERS ||--o{ ORDER_ITEMS : contains
       PRODUCTS ||--o{ ORDER_ITEMS : included_in
   """
   
   # แสดงแผนภาพ
   display_mermaid(mermaid_code)
   ```

## วิธีอื่นๆ:

### วิธีที่ 1: แปลงเป็น URL ด้วยโค้ด

```python
# โค้ด Mermaid ที่ต้องการแสดงผล
mermaid_code = """
erDiagram
    CUSTOMERS ||--o{ ORDERS : places
    ORDERS ||--o{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : included_in
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

### วิธีที่ 2: ใช้ Mermaid Live Editor

1. ไปที่ [Mermaid Live Editor](https://mermaid.live/)
2. คัดลอกโค้ด Mermaid ของคุณลงไป
3. คลิกที่ "Share" ด้านบนขวา
4. คัดลอก URL จากช่อง "Image Link"
5. นำ URL มาใช้ใน Colab:

```python
from IPython.display import Image
Image("https://mermaid.ink/img/...URL ที่คัดลอกมา...")
```

### วิธีที่ 3: บันทึกเป็นรูปภาพและอัพโหลด

1. ไปที่ [Mermaid Live Editor](https://mermaid.live/)
2. คัดลอกโค้ด Mermaid ของคุณลงไป
3. คลิก "Download PNG" หรือ "Download SVG"
4. อัพโหลดรูปภาพลงใน Colab:

```python
from google.colab import files
uploaded = files.upload()  # เลือกรูปภาพที่ดาวน์โหลดไว้

# แสดงรูปภาพ
from IPython.display import Image
Image('ชื่อไฟล์ที่อัพโหลด.png')
```

## การรันสคริปต์ปรับแต่ง notebook อัตโนมัติ

หากต้องการแก้ไข notebooks ทั้งหมดในโปรเจคอัตโนมัติ ให้รันสคริปต์ `fix_mermaid_diagrams.py`:

```bash
python fix_mermaid_diagrams.py
```

สคริปต์นี้จะ:
1. ค้นหา notebooks ทั้งหมดที่มีโค้ด Mermaid
2. คอมเมนต์โค้ด Mermaid เดิม
3. เพิ่มเซลล์ใหม่สำหรับแสดงแผนภาพผ่าน URL
4. สร้างคู่มือการใช้งาน Mermaid ใน Google Colab
