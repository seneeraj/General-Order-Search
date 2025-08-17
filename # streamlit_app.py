import streamlit as st
import fitz  # PyMuPDF
import re
from collections import defaultdict
from docx import Document  # for DOCX
import io

st.set_page_config(page_title="GO Explorer (Hindi Files)", layout="wide")
st.title("📘 General Order Explorer (हिंदी अध्याय / नियम खोजक)")

uploaded_file = st.file_uploader("📄 Upload a Hindi PDF/DOCX", type=["pdf", "docx"])

# --- Sidebar Settings ---
st.sidebar.header("⚙️ Settings")

default_chapters = ["अध्याय", "भाग", "खंड", "सेक्शन"]
default_rules = ["नियम", "धारा", "प्रावधान"]

user_chapters = st.sidebar.text_input(
    "📝 Extra Chapter Keywords (comma separated)",
    ""
)
user_rules = st.sidebar.text_input(
    "📝 Extra Rule Keywords (comma separated)",
    ""
)

CHAPTER_KEYWORDS = default_chapters + [k.strip() for k in user_chapters.split(",") if k.strip()]
RULE_KEYWORDS = default_rules + [k.strip() for k in user_rules.split(",") if k.strip()]

st.sidebar.markdown("✅ Current Chapter Keywords:")
st.sidebar.write(CHAPTER_KEYWORDS)
st.sidebar.markdown("✅ Current Rule Keywords:")
st.sidebar.write(RULE_KEYWORDS)

# --- Text Extraction ---
@st.cache_data(show_spinner=True)
def extract_text(file, filetype):
    if filetype == "pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    elif filetype == "docx":
        doc = Document(io.BytesIO(file.read()))
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return ""

def build_chapter_pattern():
    patterns = []
    for k in CHAPTER_KEYWORDS:
        patterns.append(rf"{k}\s*[\dIVX०-९]+")  # numbers
        patterns.append(rf"{k}\s*[प्रथमद्वितीयतृतीयचतुर्थपञ्चम]+")  # ordinals
    return "(" + "|".join(patterns) + ")"

def build_rule_pattern():
    patterns = []
    for k in RULE_KEYWORDS:
        patterns.append(rf"{k}\s*[\dIVX०-९]+")  # numbers
        patterns.append(rf"{k}\s*संख्या\s*\d+")  # संख्या format
    return "(" + "|".join(patterns) + ")"

def parse_structure(text):
    structure = defaultdict(dict)

    chapter_pattern = re.compile(build_chapter_pattern())
    rule_pattern = re.compile(build_rule_pattern())

    chapters = list(chapter_pattern.finditer(text))

    for i, chap in enumerate(chapters):
        chap_title = chap.group().strip()
        start = chap.end()
        end = chapters[i+1].start() if i+1 < len(chapters) else len(text)
        chap_text = text[start:end]

        rules = list(rule_pattern.finditer(chap_text))
        if not rules:
            structure[chap_title]["(कोई नियम/धारा नहीं मिला)"] = chap_text.strip()
        else:
            for j, rule in enumerate(rules):
                rule_title = rule.group().strip()
                r_start = rule.end()
                r_end = rules[j+1].start() if j+1 < len(rules) else len(chap_text)
                rule_text = chap_text[r_start:r_end].strip()
                structure[chap_title][rule_title] = rule_text
    return structure

# --- UI ---
if uploaded_file:
    ext = uploaded_file.name.split(".")[-1].lower()
    text = extract_text(uploaded_file, ext)
    structure = parse_structure(text)

    chapters = list(structure.keys())
    if chapters:
        selected_chap = st.selectbox("📚 अध्याय / भाग / खंड चुनें", chapters)
        if selected_chap:
            rules = list(structure[selected_chap].keys())
            selected_rule = st.selectbox("📌 नियम / धारा / प्रावधान चुनें", rules)
            if selected_rule:
                st.markdown(f"### 📄 {selected_rule}")
                st.text_area("📝 विवरण", structure[selected_chap][selected_rule], height=500)
    else:
        st.warning("❌ अध्याय/भाग/खंड या नियम/धारा/प्रावधान नहीं मिला। कृपया सही यूनिकोड हिंदी फ़ाइल अपलोड करें।")
