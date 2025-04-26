
import os
import re
import json
import nbformat as nbf
from pathlib import Path

# กำหนดโฟลเดอร์ที่ต้องการค้นหา notebooks
dirs_to_scan = [
    "labs",
    "Day1-Morning",
    "Day1-Afternoon",
    "Day2-Morning",
    "Day2-Afternoon",
    "Day3-Morning",
    "Day3-Afternoon"
]

def extract_mermaid_from_code(code):
    """สกัดโค้ด Mermaid จากเซลล์โค้ด"""
    if '```mermaid' in code or 'erDiagram' in code:
        # กรณีที่เป็น code block mermaid
        mermaid_pattern = r'```mermaid\s+(.*?)\s+```'
        mermaid_match = re.search(mermaid_pattern, code, re.DOTALL)
        
        if mermaid_match:
            return mermaid_match.group(1).strip()
        
        # กรณีที่เป็นโค้ด erDiagram โดยตรง
        er_pattern = r'erDiagram\s+(.*?)(?=$|```)'
        er_match = re.search(er_pattern, code, re.DOTALL)
        
        if er_match:
            return "erDiagram " + er_match.group(1).strip()
    
    return None

def generate_mermaid_url(mermaid_code):
    """สร้าง URL สำหรับแสดงผล Mermaid จาก mermaid.ink"""
    import base64
    import zlib
    
    # Remove leading and trailing whitespace
    mermaid_code = mermaid_code.strip()
    
    # Encode as bytes, compress with zlib, and base64 encode
    encoded_data = base64.urlsafe_b64encode(
        zlib.compress(mermaid_code.encode('utf-8'), 9)
    ).decode('ascii')
    
    return f"https://mermaid.ink/img/pako:{encoded_data}"

def fix_notebook(notebook_path):
    """แก้ไข Notebook ให้แสดงแผนภาพ Mermaid ผ่าน URL"""
    try:
        print(f"กำลังตรวจสอบ: {notebook_path}")
        
        # อ่านไฟล์ notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbf.read(f, as_version=4)
        
        modified = False
        
        # ตรวจสอบและแก้ไขแต่ละเซลล์
        for i, cell in enumerate(notebook.cells):
            if cell.cell_type == 'code' and ('```mermaid' in cell.source or 'erDiagram' in cell.source):
                mermaid_code = extract_mermaid_from_code(cell.source)
                
                if mermaid_code:
                    # สร้าง URL สำหรับแสดงผล Mermaid
                    mermaid_url = generate_mermaid_url(mermaid_code)
                    
                    # สร้างเซลล์มาร์กดาวน์สำหรับแสดงคำอธิบาย
                    explanation_cell = nbf.v4.new_markdown_cell(
                        """**หมายเหตุ:** แผนภาพ Mermaid ไม่สามารถแสดงผลได้โดยตรงใน Google Colab 
เราจึงใช้การแสดงผลผ่าน URL จาก mermaid.ink แทน"""
                    )
                    
                    # สร้างเซลล์โค้ดสำหรับแสดงผล Mermaid ผ่าน URL
                    display_cell = nbf.v4.new_code_cell(
                        f"""# แสดงแผนภาพ Mermaid ผ่าน URL
from IPython.display import Image
Image("{mermaid_url}")"""
                    )
                    
                    # คอมเมนต์โค้ด Mermaid เดิม
                    code_lines = cell.source.splitlines()
                    commented_code = ["# " + line for line in code_lines]
                    commented_code.insert(0, "# โค้ด Mermaid เดิม (ถูกคอมเมนต์ไว้)")
                    commented_code.append("")
                    commented_code.append("# หากต้องการแก้ไขแผนภาพ สามารถใช้โค้ดด้านล่างนี้แทน")
                    commented_code.append(f"""# mermaid_code = \"\"\"
# {mermaid_code}
# \"\"\"
# 
# import base64
# import zlib
# 
# # สร้าง URL สำหรับแสดงผล Mermaid
# encoded_data = base64.urlsafe_b64encode(
#     zlib.compress(mermaid_code.encode('utf-8'), 9)
# ).decode('ascii')
# mermaid_url = f"https://mermaid.ink/img/pako:{encoded_data}"
# 
# # แสดงแผนภาพ
# from IPython.display import Image
# Image(mermaid_url)""")
                    
                    cell.source = "\n".join(commented_code)
                    
                    # แทรกเซลล์ใหม่หลังจากเซลล์ปัจจุบัน
                    notebook.cells.insert(i + 1, explanation_cell)
                    notebook.cells.insert(i + 2, display_cell)
                    
                    modified = True
                    i += 2  # ข้ามเซลล์ที่เพิ่งเพิ่มเข้าไป
        
        if modified:
            # บันทึกไฟล์ notebook
            with open(notebook_path, 'w', encoding='utf-8') as f:
                nbf.write(notebook, f)
            
            print(f"  ✅ แก้ไขสำเร็จ")
            return True
        else:
            print(f"  ℹ️ ไม่พบโค้ด Mermaid ที่ต้องแก้ไข")
            return False
    except Exception as e:
        print(f"  ❌ เกิดข้อผิดพลาด: {str(e)}")
        return False

def find_and_fix_notebooks():
    """ค้นหาและแก้ไข notebooks ทั้งหมด"""
    base_dir = Path.cwd()
    fixed_count = 0
    total_count = 0
    
    for dir_name in dirs_to_scan:
        dir_path = base_dir / dir_name
        if not dir_path.exists():
            continue
        
        print(f"\nกำลังค้นหา notebooks ใน {dir_path}...")
        
        # ค้นหา notebooks ในโฟลเดอร์และโฟลเดอร์ย่อย
        for path in dir_path.glob('**/*.ipynb'):
            # ข้ามโฟลเดอร์ .ipynb_checkpoints
            if '.ipynb_checkpoints' in str(path):
                continue
                
            total_count += 1
            if fix_notebook(path):
                fixed_count += 1
    
    print(f"\nเสร็จสิ้น! แก้ไข {fixed_count}/{total_count} notebooks ที่มีแผนภาพ Mermaid")

def create_mermaid_guide():
    """สร้างคู่มือสำหรับการใช้งาน Mermaid ใน Google Colab"""
    guide_content = """# วิธีแสดงแผนภาพ Mermaid ใน Google Colab

Google Colab ไม่รองรับการแสดงผลแผนภาพ Mermaid โดยตรง แต่เราสามารถใช้วิธีการแสดงผลผ่าน URL จาก mermaid.ink แทน

## วิธีที่ 1: ใช้โค้ดแปลง Mermaid เป็น URL

```python
# โค้ด Mermaid ที่ต้องการแสดงผล
mermaid_code = \"\"\"
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
\"\"\"

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
"""
    
    guide_path = Path.cwd() / "MERMAID_GUIDE.md"
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"สร้างคู่มือการใช้งาน Mermaid ใน Google Colab ที่ {guide_path}")

if __name__ == "__main__":
    print("===== เริ่มการแก้ไขแผนภาพ Mermaid ใน Notebooks =====\n")
    
    # ค้นหาและแก้ไข notebooks
    find_and_fix_notebooks()
    
    # สร้างคู่มือการใช้งาน Mermaid
    create_mermaid_guide()
    
    print("\n===== เสร็จสิ้นการแก้ไขแผนภาพ Mermaid =====")
    print("\nคำแนะนำเพิ่มเติม:")
    print("1. สคริปต์นี้จะแก้ไข notebooks ที่มีโค้ด Mermaid โดยเพิ่มเซลล์สำหรับแสดงผลผ่าน URL")
    print("2. โค้ด Mermaid เดิมจะถูกคอมเมนต์ไว้ และมีคำอธิบายเพิ่มเติม")
    print("3. หากต้องการแก้ไขแผนภาพ สามารถดูคำแนะนำได้จากไฟล์ MERMAID_GUIDE.md")
    print("4. อย่าลืมอัพโหลดการเปลี่ยนแปลงไปยัง GitHub repository")
