
import os
import json
import nbformat as nbf

# ตรวจสอบโครงสร้างโฟลเดอร์
labs_dir = 'labs'
days = [f'วันที่{i}-{period}' for i in range(1, 4) for period in ['เช้า', 'บ่าย']]

# ฟังก์ชันสำหรับแก้ไข Notebook
def prepare_notebook_for_colab(notebook_path):
    try:
        # อ่านไฟล์ notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbf.read(f, as_version=4)
        
        # เพิ่ม cell แรกสำหรับการติดตั้งแพคเกจ
        setup_cell = nbf.v4.new_code_cell(
            """# ติดตั้งแพ็คเกจที่จำเป็น (รันเฉพาะบน Google Colab)
import sys
if 'google.colab' in sys.modules:
    # ติดตั้งแพ็คเกจที่จำเป็น
    !pip install pandas numpy matplotlib seaborn
    
    # สำหรับไฟล์ข้อมูล - ให้ดาวน์โหลดจาก GitHub หรือ Google Drive
    # หากต้องการดาวน์โหลดไฟล์จาก GitHub Repository:
    # !git clone https://github.com/amornpan/NT-Data-Science-and-Data-Analytics.git
    # !cp -r NT-Data-Science-and-Data-Analytics/data ./
    
    print("เตรียมพร้อมใช้งานบน Google Colab แล้ว!")"""
        )
        
        # เพิ่ม cell แรกสุด
        notebook.cells.insert(0, setup_cell)
        
        # บันทึกไฟล์ notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbf.write(notebook, f)
        
        print(f"แก้ไขไฟล์ {notebook_path} สำเร็จ")
        return True
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการแก้ไขไฟล์ {notebook_path}: {e}")
        return False

# ฟังก์ชันสำหรับสร้างลิงก์ Colab ใน README
def generate_colab_links():
    colab_links = "## Lab Notebooks (เปิดใน Google Colab)\n\n"
    
    for day in days:
        day_dir = os.path.join(labs_dir, day)
        if not os.path.exists(day_dir):
            continue
            
        colab_links += f"### {day}\n"
        
        for filename in os.listdir(day_dir):
            if filename.endswith('.ipynb') and not filename.startswith('.'):
                notebook_path = f"{labs_dir}/{day}/{filename}"
                notebook_path = notebook_path.replace('\\', '/')
                github_path = f"https://colab.research.google.com/github/YOUR_USERNAME/NT-Data-Science-and-Data-Analytics/blob/master/{notebook_path}"
                
                # สร้างชื่อที่อ่านง่ายขึ้น
                display_name = filename.replace('_', ' ').replace('.ipynb', '')
                
                colab_links += f"- [{display_name}]({github_path}) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({github_path})\n"
        
        colab_links += "\n"
    
    return colab_links

# แก้ไข README.md
def update_readme():
    try:
        # อ่าน README.md
        with open('README.md', 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        # สร้างลิงก์ Colab
        colab_links = generate_colab_links()
        
        # ตรวจสอบว่ามีส่วน Lab Notebooks แล้วหรือไม่
        if "## Lab Notebooks" in readme_content:
            # แทนที่ส่วน Lab Notebooks เดิม
            import re
            readme_content = re.sub(r'## Lab Notebooks.*?(?=##|$)', colab_links, readme_content, flags=re.DOTALL)
        else:
            # เพิ่มส่วน Lab Notebooks ท้าย README
            readme_content += "\n\n" + colab_links
        
        # บันทึก README.md
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("แก้ไข README.md สำเร็จ")
        return True
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการแก้ไข README.md: {e}")
        return False

# ดำเนินการแก้ไข notebooks
notebook_count = 0
for day in days:
    day_dir = os.path.join(labs_dir, day)
    if not os.path.exists(day_dir):
        continue
    
    for filename in os.listdir(day_dir):
        if filename.endswith('.ipynb') and not filename.startswith('.'):
            notebook_path = os.path.join(day_dir, filename)
            if prepare_notebook_for_colab(notebook_path):
                notebook_count += 1

print(f"แก้ไข {notebook_count} notebooks สำเร็จ")

# แก้ไข README.md
update_readme()

print("\nคำแนะนำเพิ่มเติม:")
print("1. อย่าลืมแก้ไข 'YOUR_USERNAME' ในไฟล์ setup_colab.py เป็นชื่อผู้ใช้ GitHub ของคุณ")
print("2. อัพโหลดการเปลี่ยนแปลงทั้งหมดไปยัง GitHub repository ของคุณ")
print("3. ตรวจสอบว่าปุ่ม 'Open in Colab' ทำงานได้อย่างถูกต้อง")
