# วันที่ 1 (ช่วงเช้า): พื้นฐาน Data Science และความสำคัญของข้อมูล

## ขั้นตอนการติดตั้งซอฟต์แวร์ที่จำเป็น

### การติดตั้ง Python 3.10 หรือใหม่กว่า

#### สำหรับ Windows

1. **ดาวน์โหลด Python**
   - เข้าไปที่เว็บไซต์ [Python.org](https://www.python.org/downloads/)
   - คลิกที่ปุ่ม "Download Python 3.10.x" (หรือเวอร์ชันล่าสุด)

2. **ติดตั้ง Python**
   - เปิดไฟล์ที่ดาวน์โหลดมา
   - เลือก "Add Python to PATH" ✓
   - คลิก "Install Now"
   - รอจนกระทั่งการติดตั้งเสร็จสมบูรณ์

3. **ตรวจสอบการติดตั้ง**
   - เปิด Command Prompt (หรือ PowerShell)
   - พิมพ์คำสั่ง `python --version` และกด Enter
   - ควรจะแสดงเวอร์ชันของ Python ที่ติดตั้ง เช่น "Python 3.10.x"

#### สำหรับ macOS

1. **ดาวน์โหลด Python**
   - เข้าไปที่เว็บไซต์ [Python.org](https://www.python.org/downloads/)
   - คลิกที่ปุ่ม "Download Python 3.10.x" (หรือเวอร์ชันล่าสุด)

2. **ติดตั้ง Python**
   - เปิดไฟล์ .pkg ที่ดาวน์โหลดมา
   - ทำตามขั้นตอนการติดตั้ง
   - รอจนกระทั่งการติดตั้งเสร็จสมบูรณ์

3. **ตรวจสอบการติดตั้ง**
   - เปิด Terminal
   - พิมพ์คำสั่ง `python3 --version` และกด Enter
   - ควรจะแสดงเวอร์ชันของ Python ที่ติดตั้ง เช่น "Python 3.10.x"

#### สำหรับ Linux

1. **ติดตั้ง Python**
   - เปิด Terminal
   - สำหรับ Ubuntu/Debian: `sudo apt update && sudo apt install python3.10`
   - สำหรับ Fedora: `sudo dnf install python3.10`
   - สำหรับ CentOS/RHEL: `sudo yum install python3.10`

2. **ตรวจสอบการติดตั้ง**
   - เปิด Terminal
   - พิมพ์คำสั่ง `python3 --version` และกด Enter
   - ควรจะแสดงเวอร์ชันของ Python ที่ติดตั้ง เช่น "Python 3.10.x"

### การติดตั้ง Anaconda หรือ Miniconda

#### การติดตั้ง Anaconda

Anaconda เป็นแพลตฟอร์มที่รวมเครื่องมือสำหรับ Data Science ไว้มากมาย รวมถึง Python, Jupyter Notebook และไลบรารีที่จำเป็นอื่นๆ

1. **ดาวน์โหลด Anaconda**
   - เข้าไปที่เว็บไซต์ [Anaconda.com](https://www.anaconda.com/products/individual)
   - เลือกดาวน์โหลดเวอร์ชันที่เหมาะกับระบบปฏิบัติการของคุณ (Windows, macOS, Linux)

2. **ติดตั้ง Anaconda**
   - **Windows**:
     - เปิดไฟล์ที่ดาวน์โหลดมา
     - เลือก "Install for All Users" (แนะนำ)
     - เลือก "Add Anaconda to my PATH environment variable" ✓
     - คลิก "Install"
     - รอจนกระทั่งการติดตั้งเสร็จสมบูรณ์

   - **macOS**:
     - เปิดไฟล์ .pkg ที่ดาวน์โหลดมา
     - ทำตามขั้นตอนการติดตั้ง
     - รอจนกระทั่งการติดตั้งเสร็จสมบูรณ์

   - **Linux**:
     - เปิด Terminal
     - ไปยังโฟลเดอร์ที่ดาวน์โหลดไฟล์มา
     - ทำให้สคริปต์ติดตั้งสามารถทำงานได้: `chmod +x Anaconda-latest-Linux-x86_64.sh`
     - รันสคริปต์ติดตั้ง: `./Anaconda-latest-Linux-x86_64.sh`
     - ทำตามคำแนะนำบนหน้าจอ

3. **ตรวจสอบการติดตั้ง**
   - เปิด Anaconda Navigator (จากเมนูเริ่มต้นหรือ Applications)
   - หรือตรวจสอบจาก Terminal/Command Prompt: `conda --version`

#### การติดตั้ง Miniconda

Miniconda เป็นเวอร์ชันที่เบากว่าของ Anaconda เหมาะสำหรับผู้ที่ต้องการติดตั้งเฉพาะเครื่องมือที่จำเป็น

1. **ดาวน์โหลด Miniconda**
   - เข้าไปที่เว็บไซต์ [docs.conda.io](https://docs.conda.io/en/latest/miniconda.html)
   - เลือกดาวน์โหลดเวอร์ชันที่เหมาะกับระบบปฏิบัติการของคุณ

2. **ติดตั้ง Miniconda**
   - **Windows**:
     - เปิดไฟล์ที่ดาวน์โหลดมา
     - เลือก "Add Miniconda to my PATH environment variable" ✓
     - คลิก "Install"
     - รอจนกระทั่งการติดตั้งเสร็จสมบูรณ์

   - **macOS/Linux**:
     - เปิด Terminal
     - ไปยังโฟลเดอร์ที่ดาวน์โหลดไฟล์มา
     - ทำให้สคริปต์ติดตั้งสามารถทำงานได้: `chmod +x Miniconda3-latest-*-x86_64.sh`
     - รันสคริปต์ติดตั้ง: `./Miniconda3-latest-*-x86_64.sh`
     - ทำตามคำแนะนำบนหน้าจอ

3. **ตรวจสอบการติดตั้ง**
   - เปิด Terminal หรือ Command Prompt
   - พิมพ์คำสั่ง `conda --version` และกด Enter
   - ควรจะแสดงเวอร์ชันของ conda ที่ติดตั้ง

### การติดตั้ง Jupyter Notebook

หากคุณติดตั้ง Anaconda แล้ว Jupyter Notebook จะถูกติดตั้งมาด้วย แต่หากคุณติดตั้ง Miniconda หรือ Python โดยตรง คุณสามารถติดตั้ง Jupyter Notebook เพิ่มเติมได้ดังนี้:

1. **ติดตั้งผ่าน conda** (สำหรับผู้ใช้ Anaconda/Miniconda):
   ```
   conda install -c conda-forge jupyter
   ```

2. **ติดตั้งผ่าน pip** (สำหรับผู้ใช้ Python โดยตรง):
   ```
   pip install notebook
   ```

3. **ตรวจสอบการติดตั้ง**:
   - เปิด Terminal หรือ Command Prompt
   - พิมพ์คำสั่ง `jupyter notebook` และกด Enter
   - เว็บเบราว์เซอร์ควรจะเปิดขึ้นมาพร้อมกับหน้า Jupyter Notebook

## การติดตั้ง Power BI Desktop

> **หมายเหตุ**: Power BI Desktop รองรับเฉพาะระบบปฏิบัติการ Windows เท่านั้น

1. **ดาวน์โหลด Power BI Desktop**
   - เข้าไปที่ [Microsoft Power BI Download](https://powerbi.microsoft.com/desktop/)
   - คลิกที่ปุ่ม "Download"

2. **ติดตั้ง Power BI Desktop**
   - เปิดไฟล์ที่ดาวน์โหลดมา
   - ทำตามขั้นตอนการติดตั้ง
   - รอจนกระทั่งการติดตั้งเสร็จสมบูรณ์

3. **ตรวจสอบการติดตั้ง**
   - เปิด Power BI Desktop จากเมนูเริ่มต้น
   - หน้าต่างแรกของ Power BI Desktop ควรจะปรากฏขึ้น

## ไลบรารีที่จำเป็นสำหรับการวิเคราะห์ข้อมูล

หลังจากติดตั้ง Python และ Anaconda/Miniconda แล้ว ให้ติดตั้งไลบรารีต่อไปนี้:

1. **NumPy**: สำหรับการคำนวณเชิงตัวเลข
   ```
   conda install numpy
   # หรือ
   pip install numpy
   ```

2. **Pandas**: สำหรับการจัดการและวิเคราะห์ข้อมูล
   ```
   conda install pandas
   # หรือ
   pip install pandas
   ```

3. **Matplotlib**: สำหรับการสร้างกราฟและการแสดงผลข้อมูล
   ```
   conda install matplotlib
   # หรือ
   pip install matplotlib
   ```

4. **Seaborn**: สำหรับการสร้างกราฟขั้นสูง
   ```
   conda install seaborn
   # หรือ
   pip install seaborn
   ```

5. **Scikit-learn**: สำหรับการเรียนรู้ของเครื่อง (Machine Learning)
   ```
   conda install scikit-learn
   # หรือ
   pip install scikit-learn
   ```

## เริ่มต้นใช้งาน Jupyter Notebook

1. เปิด Terminal หรือ Command Prompt
2. พิมพ์คำสั่ง `jupyter notebook` และกด Enter
3. เว็บเบราว์เซอร์จะเปิดขึ้นมาพร้อมกับหน้า Jupyter Notebook
4. คลิกที่ "New" > "Python 3" เพื่อสร้าง Notebook ใหม่
5. ทดลองเขียนโค้ด Python ง่ายๆ เช่น:
   ```python
   print("Hello, Data Science!")
   ```
6. กด Shift + Enter เพื่อรันโค้ด

## การทดสอบไลบรารีพื้นฐาน

```python
# ทดสอบ NumPy
import numpy as np
print("NumPy version:", np.__version__)
arr = np.array([1, 2, 3, 4, 5])
print("NumPy array:", arr)

# ทดสอบ Pandas
import pandas as pd
print("Pandas version:", pd.__version__)
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
print("Pandas DataFrame:\n", df)

# ทดสอบ Matplotlib
import matplotlib.pyplot as plt
print("Matplotlib version:", plt.__version__)
plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
plt.title('Simple Plot')
plt.show()
```

---

หากคุณมีปัญหาในการติดตั้งหรือใช้งานซอฟต์แวร์ใดๆ โปรดติดต่อวิทยากรเพื่อขอความช่วยเหลือ