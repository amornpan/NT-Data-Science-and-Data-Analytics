
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
