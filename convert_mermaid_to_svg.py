
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

def generate_mermaid_svg_url(mermaid_code):
    """สร้าง URL สำหรับแสดงผล Mermaid เป็น SVG จาก mermaid.ink"""
    import base64
    import zlib
    
    # Remove leading and trailing whitespace
    mermaid_code = mermaid_code.strip()
    
    # Encode as bytes, compress with zlib, and base64 encode
    encoded_data = base64.urlsafe_b64encode(
        zlib.compress(mermaid_code.encode('utf-8'), 9)
    ).decode('ascii')
    
    return f"https://mermaid.ink/svg/pako:{encoded_data}"

def fix_notebook(notebook_path):
    """แก้ไข Notebook ให้แสดงแผนภาพ Mermaid เป็น SVG"""
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
                    # สร้าง URL สำหรับแสดงผล Mermaid เป็น SVG
                    mermaid_svg_url = generate_mermaid_svg_url(mermaid_code)
                    
                    # สร้างเซลล์มาร์กดาวน์สำหรับแสดงคำอธิบาย
                    explanation_cell = nbf.v4.new_markdown_cell(
                        """**หมายเหตุ:** แผนภาพ Mermaid ไม่สามารถแสดงผลได้โดยตรงใน Google Colab 
เราจึงใช้การแสดงผลเป็น SVG ผ่าน mermaid.ink แทน ซึ่งมีคุณภาพสูงกว่าและสามารถขยายได้โดยไม่แตก"""
                    )
                    
                    # สร้างเซลล์โค้ดสำหรับแสดงผล Mermaid เป็น SVG
                    display_cell = nbf.v4.new_code_cell(
                        f"""# แสดงแผนภาพ Mermaid เป็น SVG
import requests
from IPython.display import SVG

# ดึงเนื้อหา SVG จาก URL
response = requests.get("{mermaid_svg_url}")
svg_content = response.text

# แสดงผล SVG
SVG(data=svg_content)"""
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
# import requests
# from IPython.display import SVG
# 
# # สร้าง URL สำหรับ SVG จาก mermaid.ink
# encoded_data = base64.urlsafe_b64encode(
#     zlib.compress(mermaid_code.encode('utf-8'), 9)
# ).decode('ascii')
# mermaid_svg_url = f"https://mermaid.ink/svg/pako:{encoded_data}"
# 
# # ดึงเนื้อหา SVG
# response = requests.get(mermaid_svg_url)
# svg_content = response.text
# 
# # แสดงผล SVG
# SVG(data=svg_content)""")
                    
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

def create_mermaid_svg_helper():
    """สร้างไฟล์ Helper สำหรับการแสดงแผนภาพ Mermaid เป็น SVG"""
    helper_content = """
# Helper สำหรับการแสดงแผนภาพ Mermaid เป็น SVG ใน Google Colab

def display_mermaid_as_svg(mermaid_code):
    """
    แสดงแผนภาพ Mermaid เป็น SVG ใน Google Colab
    
    Parameters:
    mermaid_code (str): โค้ด Mermaid ที่ต้องการแสดงผล
    
    Returns:
    IPython.display.SVG: แสดง SVG แผนภาพ Mermaid
    """
    import base64
    import zlib
    import requests
    from IPython.display import SVG, display, HTML
    
    # ตรวจสอบว่ารันอยู่บน Google Colab หรือไม่
    try:
        import google.colab
        is_colab = True
    except:
        is_colab = False
    
    # ถ้ารันบน Colab ให้ใช้ SVG จาก mermaid.ink
    if is_colab:
        # ลบช่องว่างหน้าและหลังข้อความ
        mermaid_code = mermaid_code.strip()
        
        # แปลงเป็น URL สำหรับ SVG
        encoded_data = base64.urlsafe_b64encode(
            zlib.compress(mermaid_code.encode('utf-8'), 9)
        ).decode('ascii')
        
        mermaid_svg_url = f"https://mermaid.ink/svg/pako:{encoded_data}"
        
        # ดึงเนื้อหา SVG
        response = requests.get(mermaid_svg_url)
        svg_content = response.text
        
        print("กำลังแสดงแผนภาพ Mermaid เป็น SVG...")
        return SVG(data=svg_content)
    
    # ถ้าไม่ได้รันบน Colab ให้ใช้ JavaScript โดยตรง
    else:
        display(HTML('''
        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
        <script>
            mermaid.initialize({startOnLoad:true});
        </script>
        '''))
        
        display(HTML(f'''
        <div class="mermaid">
        {mermaid_code}
        </div>
        '''))
        return None

# ตัวอย่างการใช้งาน
"""
# ตัวอย่างการใช้งาน:
from mermaid_svg_helper import display_mermaid_as_svg

# โค้ด Mermaid ที่ต้องการแสดงผล
mermaid_code = '''
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
'''

# แสดงแผนภาพเป็น SVG
display_mermaid_as_svg(mermaid_code)
"""
    
    helper_path = Path.cwd() / "mermaid_svg_helper.py"
    with open(helper_path, 'w', encoding='utf-8') as f:
        f.write(helper_content)
    
    print(f"สร้างไฟล์ Helper สำหรับการแสดงแผนภาพ Mermaid เป็น SVG ที่ {helper_path}")

def create_svg_guide():
    """สร้างคู่มือสำหรับการใช้งาน SVG ใน Google Colab"""
    guide_content = """# วิธีแสดงแผนภาพ Mermaid เป็น SVG ใน Google Colab

Google Colab ไม่รองรับการแสดงผลแผนภาพ Mermaid โดยตรง แต่เราสามารถแสดงผลเป็น SVG ได้ซึ่งมีคุณภาพสูงกว่าและสามารถขยายได้โดยไม่แตก

## วิธีที่แนะนำ: ใช้ mermaid_svg_helper.py

ผมได้สร้างไฟล์ `mermaid_svg_helper.py` ที่มีฟังก์ชัน `display_mermaid_as_svg()` ไว้ให้คุณแล้ว

### ขั้นตอนการใช้งาน:

1. **อัพโหลด mermaid_svg_helper.py ไปยัง Google Colab**:
   ```python
   # อัพโหลดไฟล์ mermaid_svg_helper.py
   from google.colab import files
   uploaded = files.upload()  # เลือกไฟล์ mermaid_svg_helper.py
   ```

2. **ใช้ฟังก์ชัน display_mermaid_as_svg**:
   ```python
   from mermaid_svg_helper import display_mermaid_as_svg
   
   # โค้ด Mermaid ที่ต้องการแสดงผล
   mermaid_code = \"\"\"
   erDiagram
       CUSTOMERS ||--o{ ORDERS : places
       ORDERS ||--o{ ORDER_ITEMS : contains
       PRODUCTS ||--o{ ORDER_ITEMS : included_in
   \"\"\"
   
   # แสดงแผนภาพเป็น SVG
   display_mermaid_as_svg(mermaid_code)
   ```

## วิธีอื่นๆ:

### วิธีที่ 1: แปลงเป็น SVG ด้วยโค้ด

```python
# โค้ด Mermaid ที่ต้องการแสดงผล
mermaid_code = \"\"\"
erDiagram
    CUSTOMERS ||--o{ ORDERS : places
    ORDERS ||--o{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : included_in
\"\"\"

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
4. **โต้ตอบได้**: SVG สามารถเพิ่มการโต้ตอบหรือแอนิเมชันได้ (แต่อาจมีข้อจำกัดบางอย่างใน Colab)

## การรันสคริปต์ปรับแต่ง notebook อัตโนมัติ

หากต้องการแก้ไข notebooks ทั้งหมดในโปรเจคอัตโนมัติ ให้รันสคริปต์ `convert_mermaid_to_svg.py`:

```bash
python convert_mermaid_to_svg.py
```

สคริปต์นี้จะ:
1. ค้นหา notebooks ทั้งหมดที่มีโค้ด Mermaid
2. คอมเมนต์โค้ด Mermaid เดิม
3. เพิ่มเซลล์ใหม่สำหรับแสดงแผนภาพเป็น SVG ผ่าน URL
4. สร้างไฟล์ Helper สำหรับการแสดงแผนภาพ Mermaid เป็น SVG
"""
    
    guide_path = Path.cwd() / "MERMAID_SVG_GUIDE.md"
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"สร้างคู่มือการแสดงแผนภาพ Mermaid เป็น SVG ที่ {guide_path}")

if __name__ == "__main__":
    print("===== เริ่มการแก้ไขแผนภาพ Mermaid เป็น SVG ใน Notebooks =====\n")
    
    # ค้นหาและแก้ไข notebooks
    find_and_fix_notebooks()
    
    # สร้างไฟล์ Helper
    create_mermaid_svg_helper()
    
    # สร้างคู่มือการใช้งาน
    create_svg_guide()
    
    print("\n===== เสร็จสิ้นการแก้ไขแผนภาพ Mermaid เป็น SVG =====")
    print("\nคำแนะนำเพิ่มเติม:")
    print("1. สคริปต์นี้จะแก้ไข notebooks ที่มีโค้ด Mermaid โดยเพิ่มเซลล์สำหรับแสดงผลเป็น SVG")
    print("2. โค้ด Mermaid เดิมจะถูกคอมเมนต์ไว้ และมีคำอธิบายเพิ่มเติม")
    print("3. หากต้องการแก้ไขแผนภาพ สามารถดูคำแนะนำได้จากไฟล์ MERMAID_SVG_GUIDE.md")
    print("4. อย่าลืมอัพโหลดการเปลี่ยนแปลงไปยัง GitHub repository")
    print("5. ไฟล์ mermaid_svg_helper.py สามารถใช้ได้กับทุก notebook ในโปรเจค")
