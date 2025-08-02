import streamlit as st
import pdfplumber
import re
from collections import defaultdict

st.set_page_config(page_title="GO Explorer", layout="wide")
st.title("📘 Uttar Pradesh GO Explorer – अध्याय और नियम Viewer")

st.markdown("Upload a GO PDF to explore chapters (`अध्याय`) and their respective rules (`नियम`).")

# --- Upload PDF ---
uploaded_file = st.file_uploader("📄 Upload GO PDF", type=["pdf"])

# --- Text Extraction and Parsing ---
@st.cache_data(show_spinner=False)
def extract_structure(file):
    with pdfplumber.open(file) as pdf:
        full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    # Step 1: Find all अध्याय (chapters)
    chapter_pattern = r"(अध्याय\s+\d+\s*[-–]?\s*[^\n]*)"
    chapter_matches = list(re.finditer(chapter_pattern, full_text))

    # Step 2: Split text into chapters
    chapters = {}
    for i, match in enumerate(chapter_matches):
        chap_title = match.group().strip()
        start = match.end()
        end = chapter_matches[i + 1].start() if i + 1 < len(chapter_matches) else len(full_text)
        chapters[chap_title] = full_text[start:end]

    # Step 3: Within each chapter, extract नियमs
    full_structure = defaultdict(dict)
    rule_pattern = r"(नियम\s+\d+[^\n]*)"

    for chap, chap_text in chapters.items():
        rule_matches = list(re.finditer(rule_pattern, chap_text))
        if not rule_matches:
            full_structure[chap]["(No नियम found)"] = chap_text.strip()
            continue

        for i, rule in enumerate(rule_matches):
            rule_title = rule.group().strip()
            r_start = rule.end()
            r_end = rule_matches[i + 1].start() if i + 1 < len(rule_matches) else len(chap_text)
            content = chap_text[r_start:r_end].strip()
            full_structure[chap][rule_title] = content

    return full_structure

# --- UI Logic ---
if uploaded_file:
    structure = extract_structure(uploaded_file)
    chapters = list(structure.keys())

    selected_chapter = st.selectbox("📚 Select अध्याय (Chapter)", chapters)

    if selected_chapter:
        rules = list(structure[selected_chapter].keys())
        selected_rule = st.selectbox("📌 Select नियम (Rule)", rules)

        if selected_rule:
            st.markdown(f"### 📝 {selected_rule}")
            st.text_area("📄 Rule Content", structure[selected_chapter][selected_rule], height=500)
