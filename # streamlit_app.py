import streamlit as st
import pdfplumber
import re

st.set_page_config(page_title="GO Section Viewer", layout="wide")
st.title("📘 General Order (GO) Section Viewer")

st.markdown("Upload a PDF (e.g., GO/Adhiniyam), and we'll extract its internal sections like 'धारा 1', 'धारा 2', etc.")

# --- Upload PDF ---
uploaded_file = st.file_uploader("📄 Upload GO PDF", type=["pdf"])

# --- Extract Sections ---
@st.cache_data(show_spinner=False)
def extract_sections_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    # Find section headers like "धारा 1", "धारा 2", ...
    pattern = r"(धारा\s+\d+[^\n]*)"
    matches = list(re.finditer(pattern, full_text))

    if not matches:
        return {}, full_text

    sections = {}
    for i in range(len(matches)):
        title = matches[i].group().strip()
        start = matches[i].end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        content = full_text[start:end].strip()
        sections[title] = content

    return sections, full_text

# --- Display Sections ---
if uploaded_file:
    with st.spinner("🔍 Extracting sections..."):
        sections_dict, full_text = extract_sections_from_pdf(uploaded_file)

    if not sections_dict:
        st.warning("No recognizable 'धारा' sections found. Showing full text instead.")
        st.text_area("📄 Full Text", full_text, height=600)
    else:
        selected_section = st.selectbox("📌 Select a Section (धारा)", list(sections_dict.keys()))
        st.markdown(f"### ✳️ {selected_section}")
        st.text_area("📝 Section Content", sections_dict[selected_section], height=500)

        # Optional: Save
        if st.button("💾 Save Section as Text"):
            file_name = selected_section.replace(" ", "_") + ".txt"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(sections_dict[selected_section])
            st.success(f"✅ Section saved as {file_name}")
