import streamlit as st
import fitz  # PyMuPDF
import re
from collections import defaultdict

st.set_page_config(page_title="GO Explorer (Unicode or Visual Text)", layout="wide")
st.title("📘 GO Viewer: अध्याय और नियम (PyMuPDF Version)")

uploaded_file = st.file_uploader("📄 Upload a Hindi PDF", type=["pdf"])

@st.cache_data(show_spinner=True)
def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    full_text = "\n".join(page.get_text() for page in doc)
    return full_text

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
    text = extract_text(uploaded_file)
    structure = parse_structure(text)
    chapters = list(structure.keys())

    if chapters:
        selected_chapter = st.selectbox("📚 Select अध्याय", chapters)

        if selected_chapter:
            rules = list(structure[selected_chapter].keys())
            selected_rule = st.selectbox("📌 Select नियम", rules)

            if selected_rule:
                st.markdown(f"### 📝 {selected_rule}")
                st.text_area("📄 Rule Content", structure[selected_chapter][selected_rule], height=500)
    else:
        st.warning("❌ No 'अध्याय' or 'नियम' found. Try another PDF or check Hindi encoding.")
