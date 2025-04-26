
# โค้ดสำหรับเซลล์แรกใน notebook สำหรับ Google Colab
setup_cell_code = """# ติดตั้งแพ็คเกจที่จำเป็น (รันเฉพาะบน Google Colab)
import sys
if 'google.colab' in sys.modules:
    # ติดตั้งแพ็คเกจที่จำเป็น
    !pip install pandas numpy matplotlib seaborn
    
    # สำหรับไฟล์ข้อมูล - ให้ดาวน์โหลดจาก GitHub หรือ Google Drive
    # หากต้องการดาวน์โหลดไฟล์จาก GitHub Repository:
    # !git clone https://github.com/amornpan/NT-Data-Science-and-Data-Analytics.git
    # !cp -r NT-Data-Science-and-Data-Analytics/data ./
    
    print("เตรียมพร้อมใช้งานบน Google Colab แล้ว!")
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

# !wget https://raw.githubusercontent.com/amornpan/NT-Data-Science-and-Data-Analytics/main/data/example.csv
# !ls -la  # ตรวจสอบว่าไฟล์ถูกดาวน์โหลดมาแล้ว
"""

print("รันสคริปต์ setup_colab.py เพื่อเพิ่มเซลล์นี้ในทุก notebook")
