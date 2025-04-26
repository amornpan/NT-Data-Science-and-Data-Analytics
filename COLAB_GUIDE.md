# วิธีใช้งาน Google Colab สำหรับ Lab ทั้งหมด

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
    # !git clone https://github.com/YOUR_USERNAME/NT-Data-Science-and-Data-Analytics.git
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
!wget https://raw.githubusercontent.com/YOUR_USERNAME/NT-Data-Science-and-Data-Analytics/main/data/filename.csv
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
