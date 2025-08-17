import streamlit as st
import fitz  # PyMuPDF for PDF
import re
from collections import defaultdict
from docx import Document  # for DOCX

st.set_page_config(page_title="GO Explorer (Hindi Docs)", layout="wide")
st.title("📘 General Order Explorer (अध्याय और नियम)")

# Allow both PDF and DOCX uploads
uploaded_file = st.file_uploader("📄 Upload a Hindi PDF/DOCX (Unicode only)", type=["pdf", "docx"])

@st.cache_data(show_spinner=True)
def extract_text(file, file_type):
    """Extract text from PDF or DOCX"""
    if file_type == "pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    elif file_type == "docx":
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    else:
        return ""

def parse_structure(text):
    """Parse chapters and rules from Hindi text"""
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
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type in ["pdf", "docx"]:
        text = extract_text(uploaded_file, file_type)
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
            st.warning("❌ अध्याय या नियम नहीं मिला। कृपया यूनिकोड हिंदी फ़ाइल अपलोड करें।")
    else:
        st.error("⚠️ केवल PDF और DOCX फ़ाइलें ही समर्थित हैं।")
