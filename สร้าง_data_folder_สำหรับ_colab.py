
import os
import json
import re
import nbformat as nbf
from collections import defaultdict

# ตรวจสอบโครงสร้างโฟลเดอร์
labs_dir = 'labs'
days = [f'วันที่{i}-{period}' for i in range(1, 4) for period in ['เช้า', 'บ่าย']]

# ตัวแปรเก็บข้อมูลการใช้ไฟล์
file_usage = defaultdict(set)

# รูปแบบการค้นหาการอ้างอิงไฟล์
file_patterns = [
    r'open\([\'"]([^\'"]+)[\'"]\)',
    r'read_csv\([\'"]([^\'"]+)[\'"]\)',
    r'read_excel\([\'"]([^\'"]+)[\'"]\)',
    r'pd\.read_(\w+)\([\'"]([^\'"]+)[\'"]\)',
    r'imread\([\'"]([^\'"]+)[\'"]\)',
    r'load\([\'"]([^\'"]+)[\'"]\)'
]

def extract_file_references(notebook_path):
    """สกัดการอ้างอิงไฟล์จาก notebook"""
    try:
        # อ่านไฟล์ notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbf.read(f, as_version=4)
        
        references = set()
        
        # ค้นหาการอ้างอิงไฟล์ในเซลล์โค้ด
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                source = cell.source
                
                for pattern in file_patterns:
                    matches = re.findall(pattern, source)
                    if matches:
                        for match in matches:
                            if isinstance(match, tuple):
                                # กรณีที่ pattern จับได้ทั้ง function และ path
                                # เช่น pd.read_csv('file.csv') จะได้ ('csv', 'file.csv')
                                file_path = match[-1]  # path จะอยู่ในตำแหน่งสุดท้าย
                            else:
                                file_path = match
                            
                            # กรองเฉพาะไฟล์ท้องถิ่น (ไม่รวม URL)
                            if not file_path.startswith(('http://', 'https://', '/')):
                                references.add(file_path)
        
        return references
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการอ่านไฟล์ {notebook_path}: {e}")
        return set()

def create_data_directory():
    """สร้างโฟลเดอร์ data หากยังไม่มี"""
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"สร้างโฟลเดอร์ {data_dir} สำเร็จ")
    return data_dir

def scan_all_notebooks():
    """สแกนทุก notebook เพื่อหาการอ้างอิงไฟล์"""
    for day in days:
        day_dir = os.path.join(labs_dir, day)
        if not os.path.exists(day_dir):
            continue
        
        for filename in os.listdir(day_dir):
            if filename.endswith('.ipynb') and not filename.startswith('.'):
                notebook_path = os.path.join(day_dir, filename)
                
                # สกัดการอ้างอิงไฟล์
                references = extract_file_references(notebook_path)
                
                # บันทึกข้อมูล
                if references:
                    for ref in references:
                        file_usage[ref].add(os.path.join(day, filename))
                    print(f"พบการอ้างอิงไฟล์ {len(references)} รายการในไฟล์ {notebook_path}")

def create_data_file_report(data_dir):
    """สร้างไฟล์รายงานการใช้ไฟล์ข้อมูล"""
    report_path = os.path.join(data_dir, 'file_usage_report.md')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# รายงานการใช้ไฟล์ข้อมูลใน Notebooks\n\n")
        
        if not file_usage:
            f.write("ไม่พบการอ้างอิงไฟล์ในทุก notebook\n")
            return
        
        f.write("| ไฟล์ข้อมูล | ใช้ใน Notebooks |\n")
        f.write("|------------|----------------|\n")
        
        for file_path, notebooks in sorted(file_usage.items()):
            notebooks_str = ", ".join(sorted(notebooks))
            f.write(f"| `{file_path}` | {notebooks_str} |\n")
    
    print(f"สร้างไฟล์รายงาน {report_path} สำเร็จ")

def create_data_setup_script(data_dir):
    """สร้างสคริปต์สำหรับติดตั้งไฟล์ข้อมูลใน Google Colab"""
    script_path = os.path.join(data_dir, 'download_data_files.py')
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write("""
# สคริปต์ดาวน์โหลดไฟล์ข้อมูลสำหรับ Google Colab
# วิธีใช้: รันเซลล์นี้เพื่อดาวน์โหลดไฟล์ข้อมูลทั้งหมดที่ใช้ในคอร์ส

import os

# สร้างโฟลเดอร์ data หากยังไม่มี
if not os.path.exists('data'):
    os.makedirs('data')
    print("สร้างโฟลเดอร์ data สำเร็จ")

# ดาวน์โหลดไฟล์จาก GitHub
base_url = "https://raw.githubusercontent.com/amornpan/NT-Data-Science-and-Data-Analytics/main/data/"

files_to_download = [
""")

        # เพิ่มรายการไฟล์ที่ต้องดาวน์โหลด
        for file_path in sorted(file_usage.keys()):
            # ใช้เฉพาะชื่อไฟล์ (ไม่รวม path)
            filename = os.path.basename(file_path)
            f.write(f'    "{filename}",\n')

        f.write("""]

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
    
    print(f"สร้างไฟล์สคริปต์ติดตั้ง {script_path} สำเร็จ")

def create_readme_for_data_dir(data_dir):
    """สร้างไฟล์ README สำหรับโฟลเดอร์ data"""
    readme_path = os.path.join(data_dir, 'README.md')
    
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
   - ใช้สคริปต์ `download_data_files.py` ในโฟลเดอร์นี้
   - หรือดาวน์โหลดทีละไฟล์:
   ```python
   !wget https://raw.githubusercontent.com/YOUR_USERNAME/NT-Data-Science-and-Data-Analytics/main/data/filename.csv
   ```

## รายการไฟล์ข้อมูล

สามารถดูรายละเอียดการใช้งานแต่ละไฟล์ได้ในไฟล์ `file_usage_report.md`
""")
    
    print(f"สร้างไฟล์ README {readme_path} สำเร็จ")

# ขั้นตอนหลัก
if __name__ == "__main__":
    # สร้างโฟลเดอร์ data
    data_dir = create_data_directory()
    
    # สแกนทุก notebook
    scan_all_notebooks()
    
    # สร้างรายงานและไฟล์ที่เกี่ยวข้อง
    create_data_file_report(data_dir)
    create_data_setup_script(data_dir)
    create_readme_for_data_dir(data_dir)
    
    print("\nเสร็จสิ้น!")
    print(f"พบการอ้างอิงไฟล์ทั้งหมด {len(file_usage)} รายการ")
    print("โปรดดำเนินการต่อไปนี้:")
    print("1. ค้นหาและรวบรวมไฟล์ข้อมูลทั้งหมดที่พบในรายงาน")
    print("2. คัดลอกไฟล์เหล่านั้นไปยังโฟลเดอร์ 'data'")
    print("3. อัพโหลดโฟลเดอร์ 'data' ไปยัง GitHub repository ของคุณ")
    print("4. แก้ไข 'YOUR_USERNAME' ในไฟล์ต่างๆ เป็นชื่อผู้ใช้ GitHub ของคุณ")
