import streamlit as st
from tasks import task_process_files, data_task_status, verify_task
from utils import concat_csv_files

st.title("Pipeline de Processos Jurídicos")


uploaded_files = st.file_uploader(
    "Selecione os pdf dos processos entre de 1 a 5 PDFs",
    type="pdf",
    accept_multiple_files=True,
)


if len(uploaded_files) >= 1 and len(uploaded_files) <= 5:
    is_ok = True  # controla a exibição do botão de download
    if st.button("Enviar para processamento"):
        csv_files = []
        st.success(f"{len(uploaded_files)} arquivos enviados com sucesso!")

        for file in uploaded_files:
            try:
                task = task_process_files.delay(file.read())
                st.write(f"Tarefa criada: {task.id}")
                task_id = data_task_status(task.id)

                st.write("Aguarde enquanto processamos seus documentos...")

                csv_files.append(verify_task(task.id))
            except Exception as e:
                st.error(f"Erro ao processar arquivo: {e}")
                is_ok = False
                break

        if is_ok:
            st.success("Tarefa concluída!")
            csv_data = concat_csv_files(csv_files)
            st.download_button(
                "Baixar CSV",
                data=csv_data,
                file_name="data_processo.csv",
            )
