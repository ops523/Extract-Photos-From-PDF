import streamlit as st
import fitz  # PyMuPDF
import os
import zipfile
from io import BytesIO

st.set_page_config(page_title="PDF Photo Extractor", layout="centered")

st.title("📸 PDF Photo Extractor")
st.write("Upload a PDF and extract all photos as separate files.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

# Optional filter
min_size = st.slider("Minimum image size (px) to keep", 0, 1000, 200)

if uploaded_file:
    if st.button("Extract Photos"):
        with st.spinner("Processing..."):

            # Load PDF
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")

            extracted_images = []
            seen_xrefs = set()

            for page_number in range(len(doc)):
                page = doc[page_number]
                image_list = page.get_images(full=True)

                for img in image_list:
                    xref = img[0]

                    if xref in seen_xrefs:
                        continue
                    seen_xrefs.add(xref)

                    base_image = doc.extract_image(xref)

                    # Size filter
                    if base_image["width"] < min_size or base_image["height"] < min_size:
                        continue

                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]

                    filename = f"photo_{len(extracted_images)}.{image_ext}"
                    extracted_images.append((filename, image_bytes))

            if len(extracted_images) == 0:
                st.warning("No images found. This might be a scanned PDF.")
            else:
                # Create ZIP in memory
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                    for filename, image_bytes in extracted_images:
                        zip_file.writestr(filename, image_bytes)

                zip_buffer.seek(0)

                st.success(f"✅ Extracted {len(extracted_images)} photos")

                st.download_button(
                    label="📥 Download All Photos (ZIP)",
                    data=zip_buffer,
                    file_name="extracted_photos.zip",
                    mime="application/zip"
                )
