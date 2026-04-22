import streamlit as st
import time

# ---------------- DOWNLOAD UX ----------------
if st.session_state.zip_ready:

    if "download_ready" not in st.session_state:
        st.session_state.download_ready = False

    col1, col2 = st.columns([3, 1])

    with col1:
        if not st.session_state.download_ready:
            if st.button("📦 Prepare Download", use_container_width=True):

                with st.spinner("⏳ Please wait, preparing your download..."):
                    time.sleep(1.5)  # UX delay (feels responsive)

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

    with col2:
        st.info("Files are packaged securely before download.")
