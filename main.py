import streamlit as st
from tasks import task_process_files, status_task, verify_task
from utils import concat_csv_files

st.title("Pipeline de Processos Jurídicos")


uploaded_files = st.file_uploader(
    "Selecione os pdf dos processos entre de 1 a 5 PDFs",
    type="pdf",
    accept_multiple_files=True,
)


if len(uploaded_files) >= 1 and len(uploaded_files) <= 5:
    if st.button("Enviar para processamento"):
        csv_files = []
        st.success(f"{len(uploaded_files)} arquivos enviados com sucesso!")

        for file in uploaded_files:
            task = task_process_files.delay(file.read())
            st.write(f"Tarefa criada: {task.id}")
            task_id = status_task(task.id)

            st.write("Aguarde enquanto processamos seus documentos...")
            csv_files.append(verify_task(task.id))

        st.success("Tarefa concluída!")

        csv_data = concat_csv_files(csv_files)
        st.download_button(
            "Baixar CSV",
            data=csv_data,
            file_name="data_processo.csv",
        )
