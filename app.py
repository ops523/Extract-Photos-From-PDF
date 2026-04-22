# ---------------- IMPORTS ----------------
import streamlit as st
import fitz  # PyMuPDF
import zipfile
from io import BytesIO
import base64
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Adwallz | PDF Photo Extractor",
    page_icon="assets/logo.png",
    layout="wide"
)

# ---------------- SESSION STATE INIT ----------------
if "zip_ready" not in st.session_state:
    st.session_state.zip_ready = False
    st.session_state.zip_bytes = None
    st.session_state.images = []

if "download_ready" not in st.session_state:
    st.session_state.download_ready = False

# ---------------- LOAD LOGO ----------------
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = get_base64("assets/logo.png")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
    <style>
    .main-title {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-text {
        color: #6c757d;
        margin-bottom: 20px;
    }
    .card {
        padding: 20px;
        border-radius: 12px;
        background-color: #f8f9fa;
        margin-bottom: 20px;
    }
    .success-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #e6f4ea;
        color: #1e7e34;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(f"""
    <div style="display:flex; align-items:center; gap:15px;">
        <img src="data:image/png;base64,{logo_base64}" width="60">
        <div>
            <div class="main-title">PDF Photo Extractor</div>
            <div class="sub-text">by Adwallz</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.image("assets/logo.png", width=120)
st.sidebar.markdown("### ⚙️ Settings")

min_size = st.sidebar.slider(
    "Minimum Image Size (px)",
    0, 1000, 200,
    help="Filter out small icons/logos"
)

st.sidebar.markdown("---")
st.sidebar.info("Increase size filter to remove unwanted elements")

# ---------------- MAIN LAYOUT ----------------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("📂 Upload PDF", type=["pdf"])
    extract_clicked = st.button("🚀 Extract Photos", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("### ℹ️ How it works")
    st.write("""
    1. Upload PDF  
    2. Click extract  
    3. Preview images  
    4. Download ZIP  
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PROCESSING ----------------
if uploaded_file and extract_clicked:

    # Reset download state
    st.session_state.download_ready = False

    with st.spinner("🔄 Processing PDF..."):

        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        extracted_images = []
        seen_xrefs = set()

        progress_bar = st.progress(0)
        total_pages = len(doc)

        for page_number in range(total_pages):
            page = doc[page_number]
            image_list = page.get_images(full=True)

            for img in image_list:
                xref = img[0]

                if xref in seen_xrefs:
                    continue
                seen_xrefs.add(xref)

                base_image = doc.extract_image(xref)

                if base_image["width"] < min_size or base_image["height"] < min_size:
                    continue

                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                filename = f"photo_{len(extracted_images)}.{image_ext}"
                extracted_images.append((filename, image_bytes))

            progress_bar.progress((page_number + 1) / total_pages)

        if len(extracted_images) == 0:
            st.warning("⚠️ No images found. This might be a scanned PDF.")
            st.session_state.zip_ready = False
            st.session_state.images = []

        else:
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for filename, image_bytes in extracted_images:
                    zip_file.writestr(filename, image_bytes)

            zip_buffer.seek(0)
            zip_bytes = zip_buffer.getvalue()

            st.session_state.zip_bytes = zip_bytes
            st.session_state.zip_ready = True
            st.session_state.images = extracted_images

# ---------------- RESULTS ----------------
if st.session_state.zip_ready:

    st.markdown('<div class="success-box">✅ Extraction Complete!</div>', unsafe_allow_html=True)

    total_images = len(st.session_state.images)
    zip_size_mb = len(st.session_state.zip_bytes) / (1024 * 1024)

    col1, col2, col3 = st.columns(3)
    col1.metric("Images Extracted", total_images)
    col2.metric("ZIP Size (MB)", f"{zip_size_mb:.2f}")
    col3.metric("Status", "Ready")

    st.markdown("---")

    # Preview
    st.subheader("🔍 Preview")
    preview_images = st.session_state.images[:12]
    cols = st.columns(6)

    for i, (filename, img_bytes) in enumerate(preview_images):
        with cols[i % 6]:
            st.image(img_bytes, caption=filename, use_container_width=True)

    st.markdown("---")

    # ---------------- DOWNLOAD UX ----------------
    col1, col2 = st.columns([3, 1])

    with col1:
        if not st.session_state.download_ready:

            if st.button("📦 Prepare Download", use_container_width=True):
                with st.spinner("⏳ Please wait, preparing your download..."):
                    time.sleep(1.5)

                st.session_state.download_ready = True
                st.rerun()

        else:
            st.success("✅ Your download is ready!")

            st.download_button(
                label="📥 Download All Photos (ZIP)",
                data=st.session_state.zip_bytes,
                file_name="extracted_photos.zip",
                mime="application/zip",
                use_container_width=True
            )

            st.caption("⬇️ Download will start instantly after clicking")

    with col2:
        st.info("Files are packaged securely before download.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("© 2026 Adwallz | Internal Tool")
