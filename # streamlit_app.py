import streamlit as st
import pytesseract
from pdf2image import convert_from_bytes
import re
from collections import defaultdict

st.set_page_config(page_title="GO OCR Viewer", layout="wide")
st.title("📘 Hindi GO Viewer (OCR-based for Scanned PDFs)")

uploaded_file = st.file_uploader("📄 Upload Scanned or Legacy Font GO PDF", type=["pdf"])

@st.cache_data(show_spinner=True)
def extract_text_with_ocr(file):
    images = convert_from_bytes(file.read(), dpi=300)
    text = ""
    for img in images:
        ocr_text = pytesseract.image_to_string(img, lang='hin')
        text += ocr_text + "\n"
    return text

def parse_structure(text):
    # Pattern for "अध्याय" and "नियम"
    chap_pattern = r"(अध्याय\s*\d+[^\n]*)"
    rule_pattern = r"(नियम\s*\d+[^\n]*)"

    chapters = list(re.finditer(chap_pattern, text))
    structure = defaultdict(dict)

    for i, chap in enumerate(chapters):
        chap_title = chap.group().strip()
        chap_start = chap.end()
        chap_end = chapters[i + 1].start() if i + 1 < len(chapters) else len(text)
        chap_text = text[chap_start:chap_end]

        rules = list(re.finditer(rule_pattern, chap_text))
        if not rules:
            structure[chap_title]["(No नियम found)"] = chap_text.strip()
        else:
            for j, rule in enumerate(rules):
                rule_title = rule.group().strip()
                r_start = rule.end()
                r_end = rules[j + 1].start() if j + 1 < len(rules) else len(chap_text)
                rule_text = chap_text[r_start:r_end].strip()
                structure[chap_title][rule_title] = rule_text

    return structure

if uploaded_file:
    st.info("🕵️‍♂️ Extracting Hindi text from scanned PDF using OCR...")
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
        st.warning("❌ No 'अध्याय' or 'नियम' found. Try uploading a clearer or properly scanned Hindi PDF.")
