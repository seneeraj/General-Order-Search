import streamlit as st
import fitz  # PyMuPDF
import re
from collections import defaultdict
from docx import Document  # for DOCX

st.set_page_config(page_title="GO Explorer (Hindi Files)", layout="wide")
st.title("📘 General Order Explorer (अध्याय / भाग / खंड / सेक्शन)")

uploaded_file = st.file_uploader("📄 Upload a Hindi PDF or DOCX (Unicode only)", type=["pdf", "docx"])

@st.cache_data(show_spinner=True)
def extract_text(file, filetype):
    if filetype == "pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    elif filetype == "docx":
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    return ""

def parse_structure(text, division_type):
    structure = defaultdict(dict)

    # Regex pattern based on selected division type
    if division_type == "अध्याय":
        pattern = r"(अध्याय\s*\d+[^\n]*)"
    elif division_type == "भाग":
        pattern = r"(भाग\s*\d+[^\n]*)"
    elif division_type == "खंड":
        pattern = r"(खंड\s*\d+[^\n]*)"
    elif division_type == "सेक्शन":
        pattern = r"(सेक्शन\s*\d+[^\n]*)"
    else:
        pattern = r"(अध्याय\s*\d+[^\n]*)"  # fallback

    chapters = list(re.finditer(pattern, text))

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
    filetype = "pdf" if uploaded_file.type == "application/pdf" else "docx"
    text = extract_text(uploaded_file, filetype)

    # Step 1: Select division type
    division_type = st.selectbox(
        "📖 दस्तावेज़ विभाजन चुनें",
        ["अध्याय", "भाग", "खंड", "सेक्शन"],
        index=0
    )

    # Step 2: Parse text
    structure = parse_structure(text, division_type)

    chapters = list(structure.keys())
    if chapters:
        selected_chap = st.selectbox(f"📚 {division_type} चुनें", chapters, index=None, placeholder=f"📚 {division_type} चुनें")
        if selected_chap:
            rules = list(structure[selected_chap].keys())
            selected_rule = st.selectbox("📌 नियम चुनें", rules)
            if selected_rule:
                st.markdown(f"### 📄 {selected_rule}")
                st.text_area("📝 नियम का विवरण", structure[selected_chap][selected_rule], height=500)
    else:
        st.warning("❌ कोई अध्याय/भाग/खंड/सेक्शन नहीं मिला। कृपया यूनिकोड हिंदी फ़ाइल अपलोड करें।")
