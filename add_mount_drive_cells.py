
import os
import json
import nbformat as nbf
from nbformat.v4 import new_markdown_cell, new_code_cell

# ตรวจสอบโครงสร้างโฟลเดอร์
labs_dir = 'labs'
days = [f'วันที่{i}-{period}' for i in range(1, 4) for period in ['เช้า', 'บ่าย']]

def add_data_loading_cell(notebook_path):
    try:
        # อ่านไฟล์ notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbf.read(f, as_version=4)
        
        # ตรวจสอบว่ามีเซลล์สำหรับ Google Drive แล้วหรือไม่
        has_drive_cell = any('drive.mount' in cell.get('source', '') for cell in notebook.cells 
                           if cell.cell_type == 'code')
        
        if not has_drive_cell:
            # สร้างเซลล์ markdown อธิบาย
            md_cell = new_markdown_cell(
                """## การเข้าถึงไฟล์ข้อมูล

หากมีการใช้ไฟล์ข้อมูลใน notebook นี้ คุณสามารถเลือกวิธีการเข้าถึงไฟล์ได้ดังนี้:

1. **อัพโหลดไฟล์โดยตรง**: ใช้เมนูด้านซ้าย (ไอคอนรูปโฟลเดอร์) ในการอัพโหลดไฟล์จากเครื่องของคุณ
2. **ใช้ Google Drive**: เชื่อมต่อกับ Google Drive โดยการรันเซลล์ด้านล่าง
3. **ดาวน์โหลดจาก GitHub**: หากข้อมูลอยู่ใน Repository"""
            )
            
            # สร้างเซลล์โค้ดสำหรับเชื่อมต่อ Google Drive
            drive_cell = new_code_cell(
                """# เชื่อมต่อกับ Google Drive (รันเซลล์นี้หากต้องการเข้าถึงไฟล์จาก Drive)
from google.colab import drive
drive.mount('/content/drive')

# ตัวอย่างการอ่านไฟล์จาก Google Drive
# import pandas as pd
# df = pd.read_csv('/content/drive/My Drive/path/to/your/file.csv')"""
            )
            
            # สร้างเซลล์โค้ดสำหรับดาวน์โหลดจาก GitHub
            github_cell = new_code_cell(
                """# ดาวน์โหลดไฟล์จาก GitHub (รันเซลล์นี้หากต้องการดาวน์โหลดไฟล์จาก GitHub)
# แก้ไข USERNAME และ path ให้ถูกต้อง

# !wget https://raw.githubusercontent.com/amornpan/NT-Data-Science-and-Data-Analytics/main/data/example.csv
# !ls -la  # ตรวจสอบว่าไฟล์ถูกดาวน์โหลดมาแล้ว"""
            )
            
            # เพิ่มเซลล์ต่อจากเซลล์แรก (อาจมีเซลล์ setup แล้ว)
            notebook.cells.insert(1, md_cell)
            notebook.cells.insert(2, drive_cell)
            notebook.cells.insert(3, github_cell)
            
            # บันทึกไฟล์ notebook
            with open(notebook_path, 'w', encoding='utf-8') as f:
                nbf.write(notebook, f)
            
            print(f"เพิ่มเซลล์การเข้าถึงไฟล์ในไฟล์ {notebook_path} สำเร็จ")
            return True
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการแก้ไขไฟล์ {notebook_path}: {e}")
        return False

# ฟังก์ชันตรวจสอบและแก้ไขการอ้างอิงไฟล์ใน notebook
def check_file_references(notebook_path):
    try:
        # อ่านไฟล์ notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbf.read(f, as_version=4)
        
        modified = False
        
        # ตรวจสอบการอ้างอิงไฟล์ในเซลล์โค้ด
        for i, cell in enumerate(notebook.cells):
            if cell.cell_type == 'code':
                source = cell.source
                # ตรวจสอบการอ้างอิงไฟล์ท้องถิ่น (ตัวอย่างเช่น open('file.csv'), pd.read_csv('file.csv') เป็นต้น)
                if ("open(" in source and "./" in source) or \
                   ("read_csv(" in source and not "http" in source and not "/content/" in source) or \
                   ("read_excel(" in source and not "http" in source and not "/content/" in source):
                    
                    # เพิ่มคำอธิบายเกี่ยวกับการอ้างอิงไฟล์ใน Google Colab
                    comment_cell = new_markdown_cell(
                        """### หมายเหตุสำหรับการใช้งานบน Google Colab
ใน Google Colab การอ้างอิงไฟล์จะแตกต่างจากการรันบนเครื่องท้องถิ่น คุณต้อง:
1. อัพโหลดไฟล์ข้อมูลไปยัง Colab ก่อน (ใช้เมนูด้านซ้าย)
2. อ้างอิงไฟล์โดยใช้ชื่อไฟล์โดยตรง (ไม่ต้องมี path) หรือ
3. ใช้ Google Drive โดยอ้างอิง path เป็น '/content/drive/My Drive/...'"""
                    )
                    
                    notebook.cells.insert(i, comment_cell)
                    modified = True
                    break  # เพิ่มเพียงครั้งเดียวต่อไฟล์
        
        if modified:
            # บันทึกไฟล์ notebook
            with open(notebook_path, 'w', encoding='utf-8') as f:
                nbf.write(notebook, f)
            
            print(f"เพิ่มคำอธิบายการอ้างอิงไฟล์ในไฟล์ {notebook_path} สำเร็จ")
        return True
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการตรวจสอบไฟล์ {notebook_path}: {e}")
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
            
            # เพิ่มเซลล์การเข้าถึงไฟล์
            if add_data_loading_cell(notebook_path):
                notebook_count += 1
                
            # ตรวจสอบและแก้ไขการอ้างอิงไฟล์
            check_file_references(notebook_path)

print(f"แก้ไข {notebook_count} notebooks สำเร็จ")

print("\nคำแนะนำเพิ่มเติม:")
print("1. อย่าลืมแก้ไข 'YOUR_USERNAME' ในโค้ดทั้งหมดเป็นชื่อผู้ใช้ GitHub ของคุณ")
print("2. อัพโหลดการเปลี่ยนแปลงทั้งหมดไปยัง GitHub repository ของคุณ")
print("3. หากมีไฟล์ข้อมูลที่ใช้ในแต่ละ notebook ให้อัพโหลดไปยัง GitHub ด้วย")
