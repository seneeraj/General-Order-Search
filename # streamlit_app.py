import streamlit as st
import os
import requests
import pdfplumber
import difflib
from bs4 import BeautifulSoup

st.set_page_config(page_title="GO Comparator", layout="wide")
st.title("📜 General Order (GO) Comparator")

# ---- Utility functions ----

@st.cache_data
def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def compare_texts(text1, text2):
    d = difflib.HtmlDiff()
    return d.make_table(text1.splitlines(), text2.splitlines(), context=True, numlines=2)

def get_go_pdfs_from_website(department_name):
    # Dummy implementation: Replace with real URL scraping
    if department_name.lower() == "panchayati raj":
        return {
            "GO-2022": "https://example.com/old_go.pdf",
            "GO-2023": "https://example.com/new_go.pdf"
        }
    return {}

# ---- UI Layout ----

option = st.radio("🔍 What do you want to do?", ["Search from Website", "Upload Your PDFs"])

if option == "Search from Website":
    dept = st.selectbox("Select Department", ["Panchayati Raj", "Education", "Health"])
    go_links = get_go_pdfs_from_website(dept)

    if not go_links:
        st.warning("No GOs found for this department.")
    else:
        go1_name, go1_url = list(go_links.items())[0]
        go2_name, go2_url = list(go_links.items())[1]

        go1_file = f"/tmp/{go1_name}.pdf"
        go2_file = f"/tmp/{go2_name}.pdf"

        with open(go1_file, 'wb') as f: f.write(requests.get(go1_url).content)
        with open(go2_file, 'wb') as f: f.write(requests.get(go2_url).content)

        text1 = extract_text_from_pdf(go1_file)
        text2 = extract_text_from_pdf(go2_file)

        st.subheader(f"📑 Comparing {go1_name} vs {go2_name}")
        html_diff = compare_texts(text1, text2)
        st.components.v1.html(html_diff, height=600, scrolling=True)

elif option == "Upload Your PDFs":
    col1, col2 = st.columns(2)
    with col1:
        file1 = st.file_uploader("Upload Old GO PDF", type="pdf", key="1")
    with col2:
        file2 = st.file_uploader("Upload Latest GO PDF", type="pdf", key="2")

    if file1 and file2:
        text1 = extract_text_from_pdf(file1)
        text2 = extract_text_from_pdf(file2)

        st.subheader("📑 Comparison Result")
        html_diff = compare_texts(text1, text2)
        st.components.v1.html(html_diff, height=600, scrolling=True)
