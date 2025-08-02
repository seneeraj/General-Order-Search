import streamlit as st
import pytesseract
from pdf2image import convert_from_bytes
import re
from collections import defaultdict
import os

# Set this path if Tesseract is not in PATH
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.set_page_config(page_title="GO Hindi OCR Viewer", layout="wide")
st.title("📘 Hindi GO Viewer (OCR based for scanned PDFs)")

uploaded_file = st.file_uploader("📄 Upload Hindi GO PDF (Scanned or Legacy Font)", type=["pdf"])

@st.cache_data(show_spinner=True)
def extract_text_with_ocr(file):
    images = convert_from_bytes(file.read(), dpi=300, poppler_path=r"C:\path\to\poppler\bin")
    text = ""
    for img in images:
        ocr_text = pytesseract.image_to_string(img, lang='hin')
        text += ocr_text + "\n"
    return text

def parse_structure(text):
    structure = defaultdict(dict)

    chapter_pattern = r"(अध्याय\s*\d+[^\n]*)"
    rule_pattern = r"(नियम\s*\d+[^\n]*)"

    chapters = list(re.finditer(chapter_pattern, text))

    for i, chap in enumerate(chapters):
        chap_title = chap.group().strip()
        start = chap.end()
        end = chapters[i+1].start() if i+1 < len(chapters) else len(text)
        chap_text = text[start:end]

        rules = list(re.finditer(rule_pattern, chap_text))
        if not rules:
            structure[chap_title]["(कोई नियम नहीं मिला)"] = chap_text.strip()
        else:
            for j, rule in enumerate(rules):
                rule_title = rule.group().strip()
                r_start = rule.end()
                r_end = rules[j+1].start() if j+1 < len(rules) else len(chap_text)
                rule_text = chap_text[r_start:r_end].strip()
                structure[chap_title][rule_title] = rule_text

    return structure

if uploaded_file:
    st.info("🔍 Running OCR on uploaded PDF...")
    text = extract_text_with_ocr(uploaded_file)
    structure = parse_structure(text)
    chapters = list(structure.keys())

    if chapters:
        selected_chapter = st.selectbox("📚 Select अध्याय", chapters)
        if selected_chapter:
            rules = list(structure[selected_chapter].keys())
            selected_rule = st.selectbox("📌 Select नियम", rules)
            if selected_rule:
                st.markdown(f"### ✳️ {selected_rule}")
                st.text_area("📄 Rule Content", structure[selected_chapter][selected_rule], height=500)
    else:
        st.warning("❌ Couldn’t find 'अध्याय' or 'नियम'. Check OCR quality or use a clearer PDF.")
