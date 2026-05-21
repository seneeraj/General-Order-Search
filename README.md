# 📘 General Order Explorer (Hindi GO Parser)

A Streamlit-based application for exploring and navigating Hindi Government Orders (GO), circulars, rules, and official documents.

The application can:
- Upload and read Hindi PDF/DOCX files
- Detect structured sections like:
  - अध्याय (Chapter)
  - भाग (Part)
  - खंड (Section)
  - सेक्शन (Section)
- Detect नियम (Rules)
- Display content interactively
- Fallback to automatic bullet-point summaries if no structure is found

---

# 🚀 Features

## ✅ File Support
- PDF (`.pdf`)
- Microsoft Word (`.docx`)

---

## ✅ Smart Structure Detection

Automatically identifies:
- अध्याय
- भाग
- खंड
- सेक्शन

inside uploaded Government Orders.

---

## ✅ Rule Detection

Extracts:
- नियम 1
- नियम 2
- etc.

from each section.

---

## ✅ Interactive Navigation

Users can:
1. Upload GO document
2. Select structure type
3. Select chapter/section
4. Select rule
5. Read detailed content

---

## ✅ Fallback Auto-Bullet Mode

If no structured headings are found:
- Entire document is split into bullet points
- Short summaries are shown
- Full content available inside expandable sections

---

# 🧠 How It Works

## Step 1 — Upload Document
User uploads:
- Unicode Hindi PDF
- Unicode Hindi DOCX

---

## Step 2 — Text Extraction

### PDF
Uses:
- PyMuPDF (`fitz`)

### DOCX
Uses:
- python-docx

---

## Step 3 — Structure Parsing

The app searches for:
- अध्याय
- भाग
- खंड
- सेक्शन

using Regex patterns.

---

## Step 4 — Rule Parsing

Inside each section, the app searches for:
- नियम

and organizes them hierarchically.

---

## Step 5 — Display

Structured navigation is shown using Streamlit dropdowns.

---

# ⚡ Fallback Mode

If no structure exists:
- Bullet points are auto-detected
- Summaries are generated
- Full content shown inside expanders

---

# 📂 Project Structure

```plaintext
project-folder/
│
├── streamlit_app.py
├── requirements.txt
└── README.md
````

---

# 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 📄 requirements.txt

```txt
streamlit
pymupdf
python-docx
```

---

# ▶️ Run Application

```bash
streamlit run streamlit_app.py
```

---

# 🌐 Streamlit Cloud Deployment

## 1. Upload files to GitHub

Upload:

* streamlit_app.py
* requirements.txt
* README.md

---

## 2. Deploy on Streamlit Cloud

Open:
[https://streamlit.io/cloud](https://streamlit.io/cloud)

Create a new app and select:

* GitHub repository
* Main file:
  `streamlit_app.py`

---

# 📌 Supported Document Types

| Type                  | Supported |
| --------------------- | --------- |
| Unicode Hindi PDF     | ✅         |
| Unicode Hindi DOCX    | ✅         |
| Scanned PDFs          | ❌         |
| KrutiDev/Legacy Fonts | ❌         |

---

# ⚠️ Current Limitations

The application currently works only with:

* Unicode Hindi text

It does NOT fully support:

* KrutiDev fonts
* Scanned image PDFs
* OCR-based extraction

---

# 🔮 Planned Features

* OCR Support
* GO Comparison Engine
* AI-based Summaries
* Change Tracking
* Department-wise Database
* Keyword Search
* Export to DOC/PDF
* Alerts & Notifications

---

# 🧠 Use Cases

* Government Order exploration
* Rule navigation
* Circular management
* Legal document analysis
* Department document indexing
* Administrative record systems

---

# 👨‍💻 Built With

* Python
* Streamlit
* PyMuPDF
* python-docx
* Regular Expressions (Regex)

---

# 📜 License

This project is intended for educational, research, and administrative assistance purposes.

---

# ✨ Future Vision

This application is the foundation for a:

## "Human-Alike AI Reasoning Search System"

for Government Orders, Rules, Circulars, and Administrative Documents.

```
```
