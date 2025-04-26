
# โค้ดสำหรับแสดงแผนภาพ Mermaid ใน Google Colab

def display_mermaid(mermaid_code):
    """
    แสดงแผนภาพ Mermaid ใน Google Colab ผ่าน mermaid.ink
    
    Parameters:
    mermaid_code (str): โค้ด Mermaid ที่ต้องการแสดงผล
    
    Returns:
    IPython.display.Image: แสดงรูปภาพแผนภาพ Mermaid
    """
    import base64
    import zlib
    from IPython.display import Image, display, HTML
    
    # ตรวจสอบว่ารันอยู่บน Google Colab หรือไม่
    try:
        import google.colab
        is_colab = True
    except:
        is_colab = False
    
    # ถ้ารันบน Colab ให้ใช้ mermaid.ink
    if is_colab:
        # ลบช่องว่างหน้าและหลังข้อความ
        mermaid_code = mermaid_code.strip()
        
        # แปลงเป็น URL
        encoded_data = base64.urlsafe_b64encode(
            zlib.compress(mermaid_code.encode('utf-8'), 9)
        ).decode('ascii')
        
        mermaid_url = f"https://mermaid.ink/img/pako:{encoded_data}"
        
        # แสดงรูปภาพ
        print("กำลังแสดงแผนภาพ Mermaid ผ่าน mermaid.ink...")
        return Image(mermaid_url)
    
    # ถ้าไม่ได้รันบน Colab ให้ใช้ JavaScript โดยตรง
    else:
        display(HTML("""
        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
        <script>
            mermaid.initialize({startOnLoad:true});
        </script>
        """))
        
        display(HTML(f"""
        <div class="mermaid">
        {mermaid_code}
        </div>
        """))
        return None

# ตัวอย่างการใช้งาน
"""
# ตัวอย่างการใช้งาน:
from mermaid_helper import display_mermaid

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
    
    PRODUCTS {
        int product_id PK
        string product_name
        string category
        float price
        int stock
    }
'''

# แสดงแผนภาพ
display_mermaid(mermaid_code)
"""
