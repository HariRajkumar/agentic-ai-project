# import streamlit as st
# import requests

# BACKEND_URL = "http://127.0.0.1:5000/api/upload/"


# def render_uploader():
#     st.header("Upload a Document")

#     uploaded_file = st.file_uploader(
#         "Upload PDF, TXT, or Image",
#         type=["pdf", "txt", "png", "jpg", "jpeg"]
#     )

#     if uploaded_file:
#         if st.button("Upload & Summarize"):
#             with st.spinner("Processing document..."):
#                 files = {"file": uploaded_file}
#                 response = requests.post(BACKEND_URL, files=files)

#             if response.status_code == 200:
#                 data = response.json()

#                 st.success("Document processed successfully")

#                 st.subheader("Summary")
#                 st.write(data["summary_preview"])
#             else:
#                 st.error("Upload failed")

import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:5000/api/upload/"


def render_uploader():
    st.header("Upload a Document")

    # Initialize session state (safe to call multiple times)
    if "summary" not in st.session_state:
        st.session_state.summary = None

    uploaded_file = st.file_uploader(
        "Upload PDF, TXT, or Image",
        type=["pdf", "txt", "png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        if st.button("Upload & Summarize"):
            with st.spinner("Processing document..."):
                files = {"file": uploaded_file}
                response = requests.post(BACKEND_URL, files=files)

            if response.status_code == 200:
                data = response.json()

                # ✅ Persist summary across reruns
                st.session_state.summary = data["summary_preview"]

                st.success("Document processed successfully")
            else:
                st.error("Upload failed")

    # ✅ Always render summary from session state
    if st.session_state.summary:
        st.subheader("Summary")
        st.write(st.session_state.summary)
