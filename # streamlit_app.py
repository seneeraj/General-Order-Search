import streamlit as st
import os
import requests
import pdfplumber
from bs4 import BeautifulSoup
from difflib import HtmlDiff

# --- Title ---
st.title("📄 Government Order (GO) Comparator")

# --- Step 1: Select Department ---
@st.cache_data
def get_departments():
    url = "https://mpedistrict.gov.in/Public/GO_List.aspx"
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        dropdown = soup.find("select", {"id": "ddlDept"})
        return {option.text.strip(): option['value'] for option in dropdown.find_all("option") if option['value']}
    except Exception:
        return {}

departments = get_departments()
department = st.selectbox("Select Department", ["--Select--"] + list(departments.keys()))

# --- Step 2: Select Category/Section ---
@st.cache_data
def get_categories(dept_code):
    try:
        url = f"https://mpedistrict.gov.in/Public/GO_List.aspx?dept={dept_code}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.find("table", {"id": "ctl00_ContentPlaceHolder1_gvGO"})
        sections = set()
        if table:
            for row in table.find_all("tr")[1:]:
                cols = row.find_all("td")
                if len(cols) > 3:
                    sections.add(cols[3].text.strip())
        return sorted(sections)
    except Exception:
        return []

section = None
if department != "--Select--":
    dept_code = departments[department]
    sections = get_categories(dept_code)
    if sections:
        section = st.selectbox("Select GO Category (Adhyadesh etc.)", ["--Select--"] + sections)
    else:
        st.warning("No sections found. Please try uploading a PDF directly.")

# --- Step 3: Get GO Documents (Dummy/Future Work) ---
st.markdown("#### Upload a GO PDF document (Latest or Base)")
uploaded_file = st.file_uploader("📄 Upload GO PDF", type=["pdf"])

# --- Step 4: Extract text ---
def extract_text(file):
    try:
        with pdfplumber.open(file) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])
        return text.strip()
    except Exception:
        return ""

text_latest = ""
if uploaded_file:
    text_latest = extract_text(uploaded_file)
    if not text_latest:
        st.error("❌ Failed to extract text from this PDF. It may be image-based or corrupted.")

# --- Step 5: Upload another GO to compare with ---
st.markdown("#### Upload another GO PDF to compare with (Previous Version)")
compare_file = st.file_uploader("📄 Upload GO for Comparison", type=["pdf"], key="compare")

text_compare = ""
if compare_file:
    text_compare = extract_text(compare_file)
    if not text_compare:
        st.error("❌ Failed to extract text from comparison PDF.")

# --- Step 6: Show Comparison ---
if text_latest and text_compare:
    st.markdown("### 🧐 Comparison Result")
    diff = HtmlDiff().make_table(
        text_compare.splitlines(), text_latest.splitlines(),
        fromdesc="Previous GO", todesc="Latest GO", context=True
    )
    st.components.v1.html(diff, scrolling=True, height=600)

# --- Footer ---
st.info("This app compares Government Orders. If no GO is available for scraping, you can upload your own PDF.")
