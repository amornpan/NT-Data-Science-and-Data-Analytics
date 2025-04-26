
import os
import json
import re
import nbformat as nbf
from pathlib import Path

# ตั้งค่าตัวแปรพื้นฐาน
GITHUB_USERNAME = "amornpan"
GITHUB_BRANCH = "master"  # ใช้ master แทน main
REPO_NAME = "NT-Data-Science-and-Data-Analytics"

# ตรวจสอบโครงสร้างไดเรกทอรี
base_dir = Path.cwd()
notebook_dirs = [
    base_dir / "labs",
    base_dir / "Day1-Morning",
    base_dir / "Day1-Afternoon",
    base_dir / "Day2-Morning",
    base_dir / "Day2-Afternoon",
    base_dir / "Day3-Morning",
    base_dir / "Day3-Afternoon"
]

# โค้ดสำหรับเซลล์แรกของ notebook (setup cell)
setup_cell_code = """# ติดตั้งแพ็คเกจที่จำเป็น (รันเฉพาะบน Google Colab)
import sys
if 'google.colab' in sys.modules:
    # ติดตั้งแพ็คเกจที่จำเป็น
    !pip install pandas numpy matplotlib seaborn scikit-learn plotly
    
    # สำหรับไฟล์ข้อมูล - ให้ดาวน์โหลดจาก GitHub หรือ Google Drive
    # หากต้องการดาวน์โหลดไฟล์จาก GitHub Repository:
    # !git clone https://github.com/amornpan/NT-Data-Science-and-Data-Analytics.git
    # !cp -r NT-Data-Science-and-Data-Analytics/data ./
    
    print("✅ เตรียมพร้อมใช้งานบน Google Colab แล้ว!")
"""

# คำอธิบายการเข้าถึงไฟล์
file_access_md = """## การเข้าถึงไฟล์ข้อมูล

หากมีการใช้ไฟล์ข้อมูลใน notebook นี้ คุณสามารถเลือกวิธีการเข้าถึงไฟล์ได้ดังนี้:

1. **อัพโหลดไฟล์โดยตรง**: ใช้เมนูด้านซ้าย (ไอคอนรูปโฟลเดอร์) ในการอัพโหลดไฟล์จากเครื่องของคุณ
2. **ใช้ Google Drive**: เชื่อมต่อกับ Google Drive โดยการรันเซลล์ด้านล่าง
3. **ดาวน์โหลดจาก GitHub**: หากข้อมูลอยู่ใน Repository ให้ใช้เซลล์ถัดไป
"""

# โค้ดสำหรับเซลล์เข้าถึง Google Drive
drive_cell_code = """# เชื่อมต่อกับ Google Drive (รันเซลล์นี้หากต้องการเข้าถึงไฟล์จาก Drive)
from google.colab import drive
drive.mount('/content/drive')

# ตัวอย่างการอ่านไฟล์จาก Google Drive
# import pandas as pd
# df = pd.read_csv('/content/drive/My Drive/path/to/your/file.csv')
"""

# โค้ดสำหรับเซลล์ดาวน์โหลดไฟล์จาก GitHub
github_cell_code = """# ดาวน์โหลดไฟล์จาก GitHub (รันเซลล์นี้หากต้องการดาวน์โหลดไฟล์จาก GitHub)
# แก้ไข path ให้ถูกต้อง

# !wget https://raw.githubusercontent.com/amornpan/NT-Data-Science-and-Data-Analytics/master/data/example.csv
# !ls -la  # ตรวจสอบว่าไฟล์ถูกดาวน์โหลดมาแล้ว
"""

def modify_notebook_for_colab(notebook_path):
    """แก้ไข notebook เพื่อให้ทำงานได้บน Google Colab"""
    try:
        print(f"กำลังแก้ไข: {notebook_path}")
        
        # อ่านไฟล์ notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbf.read(f, as_version=4)
        
        # ตรวจสอบว่ามีเซลล์ setup แล้วหรือไม่
        has_setup_cell = False
        for cell in notebook.cells:
            if cell.cell_type == 'code' and 'google.colab' in cell.source:
                has_setup_cell = True
                break
        
        # เพิ่มเซลล์ setup หากยังไม่มี
        if not has_setup_cell:
            setup_cell = nbf.v4.new_code_cell(setup_cell_code)
            notebook.cells.insert(0, setup_cell)
            
            # เพิ่มเซลล์การเข้าถึงไฟล์
            md_cell = nbf.v4.new_markdown_cell(file_access_md)
            drive_cell = nbf.v4.new_code_cell(drive_cell_code)
            github_cell = nbf.v4.new_code_cell(github_cell_code)
            
            notebook.cells.insert(1, md_cell)
            notebook.cells.insert(2, drive_cell)
            notebook.cells.insert(3, github_cell)
        
        # เพิ่มคำเตือนสำหรับการอ้างอิงไฟล์ท้องถิ่น (หากมี)
        has_file_reference_note = False
        for i, cell in enumerate(notebook.cells):
            if (cell.cell_type == 'markdown' and 
                "หมายเหตุสำหรับการใช้งานบน Google Colab" in cell.source):
                has_file_reference_note = True
                break
                
            if cell.cell_type == 'code':
                # ตรวจสอบการอ้างอิงไฟล์ท้องถิ่น
                if (("open(" in cell.source and "./" in cell.source) or 
                    ("read_csv(" in cell.source and not "http" in cell.source and not "/content/" in cell.source) or 
                    ("read_excel(" in cell.source and not "http" in cell.source and not "/content/" in cell.source)):
                    
                    if not has_file_reference_note:
                        note_cell = nbf.v4.new_markdown_cell(
                            """### หมายเหตุสำหรับการใช้งานบน Google Colab
ใน Google Colab การอ้างอิงไฟล์จะแตกต่างจากการรันบนเครื่องท้องถิ่น คุณต้อง:
1. อัพโหลดไฟล์ข้อมูลไปยัง Colab ก่อน (ใช้เมนูด้านซ้าย)
2. อ้างอิงไฟล์โดยใช้ชื่อไฟล์โดยตรง (ไม่ต้องมี path) หรือ
3. ใช้ Google Drive โดยอ้างอิง path เป็น '/content/drive/My Drive/...'"""
                        )
                        notebook.cells.insert(i, note_cell)
                        has_file_reference_note = True
                        break
        
        # บันทึกไฟล์ notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbf.write(notebook, f)
        
        return True
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการแก้ไขไฟล์ {notebook_path}: {e}")
        return False

def find_notebooks_and_modify():
    """ค้นหาไฟล์ notebook ทั้งหมดและแก้ไข"""
    notebook_count = 0
    success_count = 0
    
    for directory in notebook_dirs:
        if not directory.exists():
            print(f"ไม่พบโฟลเดอร์: {directory}")
            continue
            
        print(f"กำลังค้นหา notebooks ใน {directory}...")
        
        # ค้นหาไฟล์ .ipynb ในโฟลเดอร์และโฟลเดอร์ย่อย
        for path in directory.glob('**/*.ipynb'):
            # ข้ามโฟลเดอร์ .ipynb_checkpoints
            if '.ipynb_checkpoints' in str(path):
                continue
                
            notebook_count += 1
            if modify_notebook_for_colab(path):
                success_count += 1
    
    print(f"\nเสร็จสิ้น! แก้ไข {success_count}/{notebook_count} notebooks สำเร็จ")
    return success_count > 0

def create_colab_readme(directory, notebooks):
    """สร้างไฟล์ README.md ที่มีลิงก์ Open in Colab"""
    if not notebooks:
        return False
        
    dir_path = Path(directory)
    if not dir_path.exists():
        return False
        
    # สร้างชื่อที่อ่านง่ายจากชื่อโฟลเดอร์
    folder_name = dir_path.name
    folder_title = folder_name.replace('-', ' ').replace('_', ' ')
    
    readme_content = f"# {folder_title}\n\n## Notebooks (เปิดใน Google Colab)\n\n"
    
    for notebook in sorted(notebooks):
        notebook_path = f"{directory}/{notebook}".replace('\\', '/')
        github_path = f"https://colab.research.google.com/github/{GITHUB_USERNAME}/{REPO_NAME}/blob/{GITHUB_BRANCH}/{notebook_path}"
        
        # สร้างชื่อที่อ่านง่าย
        display_name = notebook.replace('_', ' ').replace('.ipynb', '')
        
        readme_content += f"- [{display_name}]({github_path}) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({github_path})\n"
    
    readme_content += """
## การใช้งานบน Google Colab

1. คลิกที่ปุ่ม "Open In Colab" ด้านบนของแต่ละ notebook
2. เมื่อเปิดใน Colab แล้ว ให้รันเซลล์แรกเพื่อติดตั้งแพ็คเกจที่จำเป็น
3. หากมีการใช้ไฟล์ข้อมูลเพิ่มเติม ให้อัพโหลดไฟล์ไปยัง Colab หรือใช้ Google Drive
"""
    
    readme_path = dir_path / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"สร้างไฟล์ README.md สำหรับ {directory} เรียบร้อยแล้ว")
    return True

def create_readme_for_all_directories():
    """สร้างไฟล์ README.md สำหรับทุกโฟลเดอร์ที่มี notebooks"""
    for directory in notebook_dirs:
        if not directory.exists():
            continue
            
        # รวบรวมรายชื่อ notebooks ในโฟลเดอร์
        notebooks = []
        for path in directory.glob('*.ipynb'):
            if '.ipynb_checkpoints' not in str(path):
                notebooks.append(path.name)
                
        # สร้าง README สำหรับโฟลเดอร์หลัก
        if notebooks:
            create_colab_readme(str(directory), notebooks)
            
        # ตรวจสอบโฟลเดอร์ย่อย
        for subdir in directory.glob('*/'):
            if subdir.is_dir() and '.ipynb_checkpoints' not in str(subdir):
                sub_notebooks = []
                for path in subdir.glob('*.ipynb'):
                    if '.ipynb_checkpoints' not in str(path):
                        sub_notebooks.append(path.name)
                        
                if sub_notebooks:
                    create_colab_readme(str(subdir), sub_notebooks)

def create_main_readme():
    """สร้าง/อัพเดทไฟล์ README.md หลักโดยเพิ่มส่วน Open in Colab"""
    readme_path = base_dir / "README.md"
    
    if not readme_path.exists():
        print(f"ไม่พบไฟล์ README.md หลัก")
        return False
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        colab_section = "## Lab Notebooks (เปิดใน Google Colab)\n\n"
        
        # รวบรวมทุก notebooks ที่พบ
        for directory in notebook_dirs:
            if not directory.exists():
                continue
                
            dir_name = directory.name
            dir_title = dir_name.replace('-', ' ').replace('_', ' ')
            
            notebooks_in_dir = []
            # ค้นหาใน directory หลัก
            for path in directory.glob('*.ipynb'):
                if '.ipynb_checkpoints' not in str(path):
                    notebooks_in_dir.append((path.name, str(directory / path.name)))
            
            # ค้นหาในโฟลเดอร์ย่อย
            for subdir in directory.glob('*/'):
                if subdir.is_dir() and '.ipynb_checkpoints' not in str(subdir):
                    for path in subdir.glob('*.ipynb'):
                        if '.ipynb_checkpoints' not in str(path):
                            notebooks_in_dir.append((path.name, str(subdir / path.name)))
            
            if notebooks_in_dir:
                colab_section += f"### {dir_title}\n"
                
                # เรียงตามชื่อไฟล์
                for notebook_name, notebook_path in sorted(notebooks_in_dir):
                    notebook_path = notebook_path.replace('\\', '/')
                    github_path = f"https://colab.research.google.com/github/{GITHUB_USERNAME}/{REPO_NAME}/blob/{GITHUB_BRANCH}/{notebook_path}"
                    
                    # สร้างชื่อที่อ่านง่าย
                    display_name = notebook_name.replace('_', ' ').replace('.ipynb', '')
                    
                    colab_section += f"- [{display_name}]({github_path}) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({github_path})\n"
                
                colab_section += "\n"
        
        # ตรวจสอบว่ามีส่วน Lab Notebooks อยู่แล้วหรือไม่
        if "## Lab Notebooks" in readme_content:
            # แทนที่ส่วน Lab Notebooks เดิม
            pattern = r'## Lab Notebooks.*?(?=##|$)'
            readme_content = re.sub(pattern, colab_section, readme_content, flags=re.DOTALL)
        else:
            # เพิ่มส่วน Lab Notebooks ต่อจากส่วนแรก
            first_section_end = readme_content.find('##', 2) if readme_content.find('##', 2) > 0 else len(readme_content)
            readme_content = readme_content[:first_section_end] + "\n\n" + colab_section + readme_content[first_section_end:]
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("อัพเดทไฟล์ README.md หลักเรียบร้อยแล้ว")
        return True
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการอัพเดทไฟล์ README.md: {e}")
        return False

def create_data_directory():
    """สร้างโฟลเดอร์ data หากยังไม่มี"""
    data_dir = base_dir / "data"
    if not data_dir.exists():
        data_dir.mkdir()
        print(f"สร้างโฟลเดอร์ {data_dir} สำเร็จ")
    
    # สร้างไฟล์ README.md ในโฟลเดอร์ data
    readme_path = data_dir / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("""# ไฟล์ข้อมูลสำหรับคอร์ส Data Science และ Data Analytics

โฟลเดอร์นี้ประกอบด้วยไฟล์ข้อมูลต่างๆ ที่ใช้ในคอร์ส

## วิธีใช้งานบน Google Colab

1. **วิธีที่ 1: อัพโหลดไฟล์โดยตรง**
   - คลิกที่ไอคอนโฟลเดอร์ด้านซ้ายมือ
   - คลิกที่ไอคอน "Upload"
   - เลือกไฟล์ข้อมูลที่ต้องการอัพโหลด

2. **วิธีที่ 2: ใช้ Google Drive**
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   # อ้างอิงไฟล์จาก Google Drive
   # ตัวอย่าง: pd.read_csv('/content/drive/My Drive/path/to/file.csv')
   ```

3. **วิธีที่ 3: ดาวน์โหลดจาก GitHub โดยตรง**
   ```python
   !wget https://raw.githubusercontent.com/amornpan/NT-Data-Science-and-Data-Analytics/master/data/filename.csv
   ```

## ตัวอย่างการใช้งาน

```python
import pandas as pd

# วิธีที่ 1: หลังจากอัพโหลดไฟล์แล้ว
df = pd.read_csv('filename.csv')

# วิธีที่ 2: จาก Google Drive
# df = pd.read_csv('/content/drive/My Drive/path/to/file.csv')

# วิธีที่ 3: ดาวน์โหลดจาก GitHub
# !wget https://raw.githubusercontent.com/amornpan/NT-Data-Science-and-Data-Analytics/master/data/filename.csv
# df = pd.read_csv('filename.csv')
```
""")
    
    # สร้างไฟล์สำหรับดาวน์โหลดข้อมูล
    download_script_path = data_dir / "download_data.py"
    with open(download_script_path, 'w', encoding='utf-8') as f:
        f.write("""
# สคริปต์ดาวน์โหลดไฟล์ข้อมูลสำหรับ Google Colab
# วิธีใช้: รันเซลล์นี้เพื่อดาวน์โหลดไฟล์ข้อมูลทั้งหมดที่ใช้ในคอร์ส

import os

# สร้างโฟลเดอร์ data หากยังไม่มี
if not os.path.exists('data'):
    os.makedirs('data')
    print("สร้างโฟลเดอร์ data สำเร็จ")

# ดาวน์โหลดไฟล์จาก GitHub
base_url = "https://raw.githubusercontent.com/amornpan/NT-Data-Science-and-Data-Analytics/master/data/"

files_to_download = [
    # รายชื่อไฟล์ที่ต้องดาวน์โหลด (จะเพิ่มเติมภายหลัง)
    "example.csv"
]

# ดาวน์โหลดไฟล์ทีละไฟล์
for filename in files_to_download:
    try:
        !wget -O "data/{filename}" "{base_url}{filename}"
        print(f"ดาวน์โหลดไฟล์ {filename} สำเร็จ")
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการดาวน์โหลดไฟล์ {filename}: {e}")

print("\\nดาวน์โหลดไฟล์ข้อมูลเสร็จสิ้น")
print("คุณสามารถอ้างอิงไฟล์เหล่านี้โดยใช้ path 'data/filename'")
""")
    
    print(f"เตรียมโฟลเดอร์ data เรียบร้อยแล้ว")
    return True

def create_colab_guide():
    """สร้างคู่มือการใช้งาน Google Colab"""
    guide_path = base_dir / "COLAB_GUIDE.md"
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write("""# วิธีใช้งาน Google Colab สำหรับคอร์ส Data Science และ Data Analytics

Google Colab (Colaboratory) เป็นสภาพแวดล้อมการเขียนโค้ด Python ที่ทำงานบนเว็บบราวเซอร์ ช่วยให้คุณสามารถเขียนและรันโค้ดได้โดยไม่ต้องติดตั้งอะไรเพิ่มเติม เหมาะสำหรับการเรียนรู้และทดลองเขียนโค้ด Python สำหรับ Data Science

## 1. วิธีเปิด Notebook ใน Google Colab

### วิธีที่ 1: เปิดจากลิงก์ "Open In Colab"
1. ในไฟล์ README.md ของแต่ละโฟลเดอร์ จะมีลิงก์ "Open In Colab" ให้คลิก
2. ระบบจะเปิด Google Colab ในแท็บใหม่
3. หากระบบถามให้ล็อกอินเข้า Google ให้ล็อกอินด้วยบัญชี Google ของคุณ

### วิธีที่ 2: เปิดผ่าน GitHub โดยตรง
1. เปิด [Google Colab](https://colab.research.google.com/)
2. คลิกที่ "File" > "Open notebook"
3. เลือกแท็บ "GitHub"
4. วางลิงก์ของ GitHub repository นี้: `https://github.com/amornpan/NT-Data-Science-and-Data-Analytics`
5. เลือก Notebook ที่ต้องการเปิด

## 2. การติดตั้งแพ็คเกจและเตรียมความพร้อม

ใน Notebook ทุกไฟล์ จะมีเซลล์แรกสำหรับการติดตั้งแพ็คเกจที่จำเป็น:

```python
# ติดตั้งแพ็คเกจที่จำเป็น (รันเฉพาะบน Google Colab)
import sys
if 'google.colab' in sys.modules:
    # ติดตั้งแพ็คเกจที่จำเป็น
    !pip install pandas numpy matplotlib seaborn
    
    # สำหรับไฟล์ข้อมูล - ให้ดาวน์โหลดจาก GitHub หรือ Google Drive
    # หากต้องการดาวน์โหลดไฟล์จาก GitHub Repository:
    # !git clone https://github.com/amornpan/NT-Data-Science-and-Data-Analytics.git
    # !cp -r NT-Data-Science-and-Data-Analytics/data ./
    
    print("เตรียมพร้อมใช้งานบน Google Colab แล้ว!")
```

**คำแนะนำ**: รันเซลล์นี้เป็นอันดับแรกเพื่อติดตั้งแพ็คเกจที่จำเป็น

## 3. การใช้งานไฟล์ข้อมูล (Data Files)

### วิธีที่ 1: อัพโหลดไฟล์ไปยัง Colab โดยตรง
1. คลิกที่ไอคอนโฟลเดอร์ด้านซ้ายมือ
2. คลิกที่ไอคอน "Upload"
3. เลือกไฟล์ข้อมูลจากเครื่องของคุณ
4. ในโค้ด การเรียกใช้ไฟล์จะเป็นแบบนี้:
   ```python
   import pandas as pd
   df = pd.read_csv('filename.csv')
   ```

### วิธีที่ 2: ใช้ Google Drive
1. เชื่อมต่อ Google Drive:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```
2. อ้างอิงไฟล์จาก Google Drive:
   ```python
   import pandas as pd
   df = pd.read_csv('/content/drive/My Drive/path/to/your/file.csv')
   ```

### วิธีที่ 3: ดาวน์โหลดไฟล์จาก GitHub
```python
!wget https://raw.githubusercontent.com/amornpan/NT-Data-Science-and-Data-Analytics/master/data/filename.csv
```

## 4. การบันทึกงานของคุณ

### บันทึกไปยัง Google Drive
1. คลิกที่ "File" > "Save a copy in Drive"
2. Notebook จะถูกบันทึกไปยัง Google Drive ของคุณ

### บันทึกเป็นไฟล์ .ipynb
1. คลิกที่ "File" > "Download" > "Download .ipynb"
2. ไฟล์จะถูกดาวน์โหลดมายังเครื่องของคุณ

## 5. การแชร์ Notebook

1. คลิกที่ปุ่ม "Share" ที่มุมขวาบน
2. กำหนดสิทธิ์การเข้าถึง (สามารถแก้ไขหรือดูอย่างเดียว)
3. คัดลอกลิงก์และส่งให้กับผู้ที่คุณต้องการแชร์

## 6. คำแนะนำเพิ่มเติม

1. **การรันโค้ด**: คลิกที่ปุ่ม "Play" ด้านซ้ายของเซลล์ หรือกด Shift+Enter
2. **การเพิ่มเซลล์**: คลิกที่ "+ Code" หรือ "+ Text" เพื่อเพิ่มเซลล์โค้ดหรือเซลล์ข้อความ
3. **การลบเซลล์**: เลือกเซลล์และกด Ctrl+M+D (หรือคลิกขวาและเลือก "Delete cell")
4. **การรันทุกเซลล์**: คลิกที่ "Runtime" > "Run all"

## 7. ข้อควรระวัง

1. Google Colab จะตัดการเชื่อมต่อหากไม่มีการใช้งานเป็นเวลานาน (ประมาณ 90 นาที)
2. หากใช้ GPU ฟรี อาจมีข้อจำกัดด้านทรัพยากรและเวลาใช้งาน
3. ข้อมูลจะหายไปเมื่อปิดเซสชัน ยกเว้นจะบันทึกไว้ใน Google Drive

## 8. การแก้ไขปัญหาเบื้องต้น

1. **ปัญหาการติดตั้งแพ็คเกจ**: ใช้คำสั่ง `!pip install package_name --upgrade`
2. **รันค้าง**: ลองรีสตาร์ท Runtime (Runtime > Restart runtime)
3. **หน่วยความจำไม่พอ**: ลองลบตัวแปรที่ไม่ใช้ หรือรีสตาร์ท Runtime
4. **ไฟล์หาย**: ตรวจสอบ path และชื่อไฟล์ให้ถูกต้อง
""")
    
    print(f"สร้างคู่มือการใช้งาน Google Colab เรียบร้อยแล้ว")
    return True

# ฟังก์ชันหลัก
if __name__ == "__main__":
    print("===== เริ่มการเตรียม Notebooks สำหรับ Google Colab =====\n")
    
    # สร้างโฟลเดอร์ data
    create_data_directory()
    
    # แก้ไขทุก notebooks
    find_notebooks_and_modify()
    
    # สร้าง README สำหรับแต่ละโฟลเดอร์
    create_readme_for_all_directories()
    
    # อัพเดท README.md หลัก
    create_main_readme()
    
    # สร้างคู่มือการใช้งาน Google Colab
    create_colab_guide()
    
    print("\n===== เสร็จสิ้นการเตรียม Notebooks สำหรับ Google Colab =====")
    print("\nสิ่งที่ต้องทำต่อไป:")
    print("1. อัพโหลดการเปลี่ยนแปลงทั้งหมดไปยัง GitHub repository")
    print("   git add .")
    print("   git commit -m \"เตรียม notebooks สำหรับ Google Colab\"")
    print("   git push")
    print("2. ทดสอบเปิด notebook ใน Colab โดยคลิกที่ปุ่ม \"Open in Colab\" ใน README.md")
