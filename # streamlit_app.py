import streamlit as st
import fitz  # PyMuPDF
import re
from collections import defaultdict

st.set_page_config(page_title="GO Explorer (Hindi PDF)", layout="wide")
st.title("📘 General Order Explorer (अध्याय और नियम)")

uploaded_file = st.file_uploader("📄 Upload a Hindi PDF (Unicode only)", type=["pdf"])

@st.cache_data(show_spinner=True)
def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

def parse_structure(text):
    structure = defaultdict(dict)
    chapters = list(re.finditer(r"(अध्याय\s*\d+[^\n]*)", text))

    for i, chap in enumerate(chapters):
        chap_title = chap.group().strip()
        start = chap.end()
        end = chapters[i+1].start() if i+1 < len(chapters) else len(text)
        chap_text = text[start:end]

        rules = list(re.finditer(r"(नियम\s*\d+[^\n]*)", chap_text))
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
        selected_chap = st.selectbox("📚 अध्याय चुनें", chapters)
        if selected_chap:
            rules = list(structure[selected_chap].keys())
            selected_rule = st.selectbox("📌 नियम चुनें", rules)
            if selected_rule:
                st.markdown(f"### 📄 {selected_rule}")
                st.text_area("📝 नियम का विवरण", structure[selected_chap][selected_rule], height=500)
    else:
        st.warning("❌ अध्याय या नियम नहीं मिला। कृपया यूनिकोड हिंदी पीडीएफ अपलोड करें।")
