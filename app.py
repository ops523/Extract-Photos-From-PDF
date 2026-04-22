# ---------------- IMPORTS ----------------
import streamlit as st
import fitz
import zipfile
from io import BytesIO
import base64
import openai

# ---------------- OPENAI SETUP ----------------
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Adwallz | PDF Photo Extractor",
    page_icon="assets/logo.png",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "zip_ready" not in st.session_state:
    st.session_state.zip_ready = False
    st.session_state.zip_bytes = None
    st.session_state.images = []

# ---------------- LOGO ----------------
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = get_base64("assets/logo.png")

# ---------------- AI TAG FUNCTION ----------------
def classify_image(image_bytes):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Classify the image into one word: receipt, handwritten, wall, document, or other."},
                {"role": "user", "content": "Classify this image."}
            ],
            max_tokens=5
        )
        label = response.choices[0].message.content.strip().lower()
        return label
    except:
        return "other"

# ---------------- HEADER ----------------
st.markdown(f"""
<div style="display:flex; align-items:center; gap:15px;">
<img src="data:image/png;base64,{logo_base64}" width="60">
<div>
<div style="font-size:28px; font-weight:700;">PDF Photo Extractor</div>
<div style="color:gray;">by Adwallz (AI Powered)</div>
</div>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.image("assets/logo.png", width=120)
min_size = st.sidebar.slider("Min Image Size", 0, 1000, 200)

# ---------------- UPLOAD ----------------
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file and st.button("🚀 Extract & Tag Photos"):

    with st.spinner("Processing + AI tagging..."):

        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        extracted_images = []
        seen_xrefs = set()

        for page_number in range(len(doc)):
            page = doc[page_number]
            for img in page.get_images(full=True):
                xref = img[0]

                if xref in seen_xrefs:
                    continue
                seen_xrefs.add(xref)

                base_image = doc.extract_image(xref)

                if base_image["width"] < min_size or base_image["height"] < min_size:
                    continue

                image_bytes = base_image["image"]

                # AI TAGGING
                tag = classify_image(image_bytes)

                filename = f"{tag}_{len(extracted_images)}.jpg"

                extracted_images.append((filename, image_bytes, tag))

        # ZIP
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for filename, image_bytes, _ in extracted_images:
                zip_file.writestr(filename, image_bytes)

        zip_buffer.seek(0)

        st.session_state.zip_ready = True
        st.session_state.zip_bytes = zip_buffer.getvalue()
        st.session_state.images = extracted_images

# ---------------- RESULTS ----------------
if st.session_state.zip_ready:

    st.success("✅ Extraction + AI tagging complete")

    st.subheader("🔍 Preview")

    cols = st.columns(5)
    for i, (filename, img_bytes, tag) in enumerate(st.session_state.images[:10]):
        with cols[i % 5]:
            st.image(img_bytes)
            st.caption(f"{tag.upper()}")

    st.download_button(
        "📥 Download Tagged Photos",
        data=st.session_state.zip_bytes,
        file_name="tagged_photos.zip"
    )
