
import os
from pathlib import Path

# ตั้งค่าตัวแปร
GITHUB_USERNAME = "amornpan"
GITHUB_BRANCH = "master"
REPO_NAME = "NT-Data-Science-and-Data-Analytics"
OUTPUT_FILE = "ALL_COLAB_LINKS.md"

# โฟลเดอร์ที่ต้องการสแกน
dirs_to_scan = [
    "labs",
    "Day1-Morning",
    "Day1-Afternoon",
    "Day2-Morning",
    "Day2-Afternoon",
    "Day3-Morning",
    "Day3-Afternoon"
]

def find_notebooks_and_create_links():
    """ค้นหา notebooks ทั้งหมดและสร้างลิงก์เปิดใน Colab"""
    base_dir = Path.cwd()
    
    # เตรียมเนื้อหาสำหรับไฟล์ Markdown
    content = "# ลิงก์เปิด Google Colab สำหรับทุก Notebook\n\n"
    content += "เอกสารนี้รวบรวมลิงก์สำหรับเปิด notebook ทั้งหมดใน Google Colab\n\n"
    
    # วนสแกนโฟลเดอร์ที่กำหนด
    for dir_name in dirs_to_scan:
        dir_path = base_dir / dir_name
        if not dir_path.exists():
            continue
        
        # เพิ่มหัวข้อสำหรับโฟลเดอร์
        content += f"## {dir_name.replace('-', ' ')}\n\n"
        
        # ค้นหา notebooks ในโฟลเดอร์หลัก
        notebooks_in_dir = []
        for file_path in dir_path.glob('*.ipynb'):
            if '.ipynb_checkpoints' not in str(file_path):
                rel_path = file_path.relative_to(base_dir)
                notebooks_in_dir.append((file_path.name, rel_path))
        
        # ค้นหา notebooks ในโฟลเดอร์ย่อย
        for subdir in dir_path.glob('*/'):
            if subdir.is_dir() and '.ipynb_checkpoints' not in str(subdir):
                # เพิ่มหัวข้อย่อยสำหรับโฟลเดอร์ย่อย
                sub_notebooks = []
                for file_path in subdir.glob('*.ipynb'):
                    if '.ipynb_checkpoints' not in str(file_path):
                        rel_path = file_path.relative_to(base_dir)
                        sub_notebooks.append((file_path.name, rel_path))
                
                if sub_notebooks:
                    content += f"### {subdir.name}\n\n"
                    for notebook_name, rel_path in sorted(sub_notebooks):
                        # สร้างลิงก์ Colab
                        colab_url = f"https://colab.research.google.com/github/{GITHUB_USERNAME}/{REPO_NAME}/blob/{GITHUB_BRANCH}/{rel_path}".replace("\\", "/")
                        # สร้างชื่อที่อ่านได้
                        display_name = notebook_name.replace("_", " ").replace(".ipynb", "")
                        
                        # เพิ่มลิงก์ลงในเนื้อหา
                        content += f"- [{display_name}]({colab_url}) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_url})\n"
                    
                    content += "\n"
        
        # เพิ่มลิงก์สำหรับ notebooks ในโฟลเดอร์หลัก
        if notebooks_in_dir:
            for notebook_name, rel_path in sorted(notebooks_in_dir):
                # สร้างลิงก์ Colab
                colab_url = f"https://colab.research.google.com/github/{GITHUB_USERNAME}/{REPO_NAME}/blob/{GITHUB_BRANCH}/{rel_path}".replace("\\", "/")
                # สร้างชื่อที่อ่านได้
                display_name = notebook_name.replace("_", " ").replace(".ipynb", "")
                
                # เพิ่มลิงก์ลงในเนื้อหา
                content += f"- [{display_name}]({colab_url}) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_url})\n"
            
            content += "\n"
    
    # เพิ่มคำแนะนำการใช้งาน
    content += """## คำแนะนำในการใช้งาน Google Colab

1. **คลิกที่ปุ่ม "Open In Colab"** ด้านขวาของแต่ละ notebook เพื่อเปิดใน Google Colab
2. **รันเซลล์แรก** เพื่อติดตั้งแพ็คเกจที่จำเป็น
3. **การใช้ไฟล์ข้อมูล**:
   - **อัพโหลดไฟล์**: คลิกที่ไอคอนโฟลเดอร์ด้านซ้าย > Upload
   - **ใช้ Google Drive**:
     ```python
     from google.colab import drive
     drive.mount('/content/drive')
     ```
   - **ดาวน์โหลดจาก GitHub**:
     ```python
     !wget https://raw.githubusercontent.com/amornpan/NT-Data-Science-and-Data-Analytics/master/data/filename.csv
     ```

4. **การบันทึกงาน**:
   - บันทึกไปยัง Google Drive: `File > Save a copy in Drive`
   - ดาวน์โหลดเป็นไฟล์: `File > Download > Download .ipynb`

**หมายเหตุ**: Google Colab จะตัดการเชื่อมต่อหากไม่มีการใช้งานเป็นเวลานาน (ประมาณ 90 นาที)
"""
    
    # บันทึกไฟล์
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"สร้างไฟล์ {OUTPUT_FILE} เรียบร้อยแล้ว")
    return content

if __name__ == "__main__":
    find_notebooks_and_create_links()
    print("เสร็จสิ้น! ตรวจสอบไฟล์ ALL_COLAB_LINKS.md")
