import streamlit as st
from core.core import send_file

uploaded_files = st.file_uploader(
    "Selecione o(s) pdf do(s) processo(s)", accept_multiple_files=True, type="pdf"
)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    send_file(bytes_data)
    # st.write("filename:", uploaded_file.name)
    # st.write(bytes_data)
