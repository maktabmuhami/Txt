import streamlit as st
from io import BytesIO
from zipfile import ZipFile
from docx import Document

# ----------------------------
# دالة استخراج النص من ملف Word
def extract_text_from_docx(file):
    doc = Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# ----------------------------
# واجهة المستخدم
st.title("📄 تحويل ملفات Word إلى TXT بترميز UTF-8")
st.markdown("👈 يمكنك رفع عدة ملفات Word (.docx) وسأقوم بتحويلها لك إلى ملفات TXT مع خيار تحميلها مضغوطة zip.")

uploaded_files = st.file_uploader("ارفع ملفات Word", type=["docx"], accept_multiple_files=True)

# ----------------------------
# إذا تم رفع ملفات
if uploaded_files:
    zip_buffer = BytesIO()
    with ZipFile(zip_buffer, "w") as zip_file:
        for uploaded_file in uploaded_files:
            # استخراج النص من ملف Word
            extracted_text = extract_text_from_docx(uploaded_file)
            
            # تجهيز اسم الملف الجديد بصيغة txt
            txt_filename = uploaded_file.name.replace(".docx", ".txt")
            
            # حفظ المحتوى كملف txt داخل zip
            zip_file.writestr(txt_filename, extracted_text.encode('utf-8'))

            # عرض زر لتحميل كل ملف بشكل منفصل
            txt_bytes = BytesIO()
            txt_bytes.write(extracted_text.encode('utf-8'))
            txt_bytes.seek(0)
            st.download_button(
                label=f"📥 تحميل {txt_filename}",
                data=txt_bytes,
                file_name=txt_filename,
                mime="text/plain"
            )
    
    # ----------------------------
    # زر لتحميل كل الملفات مضغوطة zip
    zip_buffer.seek(0)
    st.download_button(
        label="📦 تحميل جميع الملفات مضغوطة ZIP",
        data=zip_buffer,
        file_name="converted_files.zip",
        mime="application/zip"
    )
