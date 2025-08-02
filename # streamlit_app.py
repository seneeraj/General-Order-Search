import streamlit as st
import pdfplumber
import re
from collections import defaultdict

st.set_page_config(page_title="GO Explorer Debug", layout="wide")
st.title("📘 GO Section Extractor – Debug Mode")

uploaded_file = st.file_uploader("📄 Upload GO PDF (e.g. Niyamavali)", type=["pdf"])

@st.cache_data(show_spinner=False)
def extract_raw_text(file):
    try:
        with pdfplumber.open(file) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception:
        return ""

if uploaded_file:
    raw_text = extract_raw_text(uploaded_file)

    st.markdown("### 🔎 Raw Extracted Text (First 5000 characters)")
    st.text_area("🧾 Extracted Text", raw_text[:5000], height=400)

    # Now test regex manually
    chapters = re.findall(r"(अध्याय\s+\d+[^:\n]*)", raw_text)
    st.markdown(f"### 🧩 Detected अध्याय ({len(chapters)} found)")
    st.write(chapters if chapters else "❌ No headings found. Try using PyMuPDF for better results.")
