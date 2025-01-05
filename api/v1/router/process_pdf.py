import re

import pdfplumber

data_params = {
    "Classe": "classe",
    "Assunto": "assunto",
    "Foro": "foro",
    "Vara": "vara",
    "Juiz": "juiz",
    "Área": "area",
    "Valor da ação": "valor_da_acao",
}

#  nome do autor do processo
#  documento do autor do processo
#  nome(s) do(s) réu(s) do processo
#  documento(s) do(s) réu(s) do processo


def process_pdf_entity(file):
    with pdfplumber.open(file) as pdf:
        cnj = r"\b\d{7}-\d{2}\.\d{4}\.\d{1,2}\.\d{2}\.\d{4}\b"
        list_data = []
        for page in pdf.pages:
            list_data.extend(page.extract_text().split("\n"))

        data_dict = {}
        cnj_captured = False
        for txt in list_data:
            if re.search(cnj, txt) and not cnj_captured:
                data_dict["cnj"] = re.findall(cnj, txt)[0]
                cnj_captured = True
            # data_dict["file"] = file_name
            if "Imptte" in txt:
                data_dict["autor"] = txt.split("Imptte")[1].strip()
            if "Imptdo" in txt:
                data_dict["reu"] = txt.split("Imptdo")[1].strip()

            if txt in data_params:
                data_dict[data_params[txt]] = list_data[list_data.index(txt) + 1]

    return data_dict
