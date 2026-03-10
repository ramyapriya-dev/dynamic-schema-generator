from country_detector import detect_country
from schema_adapter import adapt_schema
import streamlit as st
import pdfplumber
import json
import os
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from classifier import detect_document_type
from schema_loader import load_schema


# ---------- TEXT EXTRACTION FUNCTION ----------
def extract_text(file):

    text = ""

    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except:
        pass

    # If no text found → OCR
    if text.strip() == "":
        file.seek(0)

        images = convert_from_bytes(
            file.read(),
            poppler_path=r"C:\poppler\Library\bin"
        )

        for img in images:
            text += pytesseract.image_to_string(img)

    return text


# ---------- UI ----------
st.title("Dynamic Document Schema Generator")

uploaded_file = st.file_uploader("Upload Document", type=["pdf"])


if uploaded_file:

    # ---------- CREATE UPLOAD FOLDER ----------
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    # ---------- SAVE UPLOADED FILE ----------
    file_path = os.path.join("uploads", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File saved to {file_path}")

    # ---------- EXTRACT TEXT ----------
    text = extract_text(uploaded_file)

    # ---------- DETECT DOCUMENT TYPE ----------
    doc_type = detect_document_type(text)

    # ---------- DETECT COUNTRY ----------
    country = detect_country(text)

    st.subheader("Detected Document Type")
    st.write(doc_type)

    st.subheader("Detected Country")
    st.write(country)

    # ---------- LOAD GLOBAL SCHEMA ----------
    global_schema = load_schema(doc_type)

    # ---------- GENERATE COUNTRY SCHEMA ----------
    schema = adapt_schema(global_schema, country)

    # Remove unnecessary keys if present
    schema.pop("document_type", None)
    schema.pop("country", None)

    # ---------- SCHEMA VIEWER ----------
    st.subheader("Schema Fields")

    for field in schema["fields"]:

        field_title = f"{field['id']}  ({field['type']})"

        with st.expander(field_title):

            st.write("Description")
            st.write(field.get("description", ""))

            st.write("Guideline")
            st.write(field.get("guideline", ""))

            st.write("Multiple")
            st.write(field.get("multiple", False))

            # ---------- SUBFIELDS ----------
            if "subFields" in field:

                st.markdown("### Sub Fields")

                for sub in field["subFields"]:

                    sub_title = f"{sub['id']} ({sub['type']})"

                    with st.expander(sub_title):

                        st.write("Description")
                        st.write(sub.get("description", ""))

                        st.write("Guideline")
                        st.write(sub.get("guideline", ""))

                        st.write("Multiple")
                        st.write(sub.get("multiple", False))

    # ---------- SAVE OUTPUT SCHEMA ----------
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    safe_country = country.replace(" ", "_")

    output_file = f"outputs/{doc_type}_{safe_country}_schema.json"

    with open(output_file, "w") as f:
        json.dump(schema, f, indent=4)

    st.success(f"Schema saved to {output_file}")
