import re

import pdfplumber

#  nome do autor do processo
#  documento do autor do processo
#  nome(s) do(s) réu(s) do processo
#  documento(s) do(s) réu(s) do processo

# parametros que serão buscados no arquivo pdf
data_params = {
    'Classe': 'classe',
    'Assunto': 'assunto',
    'Foro': 'foro',
    'Vara': 'vara',
    'Juiz': 'juiz',
    'Área': 'area',
    'Nome': 'nome',
    'Autor': 'autor',
    'Réu': 'reu',
    # "Nome Observação Advogados": "Nome Observação Advogados",
    'Valor da ação': 'valor_da_acao',
}


def process_pdf_entity(file):
    """
    Processa o arquivo pdf e retorna os dados do processo encontrados no arquivo
    Args:
        file (bytes): pdf file

    Returns:
        dict: Dados do processo
    """
    with pdfplumber.open(file) as pdf:
        list_data = []

        for page in pdf.pages:
            list_data.extend(page.extract_text().split('\n'))

    return extract_entity(list_data)


def extract_entity(list_data):
    """
        Extrair a informações encontradas nos pdf
    Args:
        list_data (list): lista com o texto extraido do pdf

    Returns:
        dict: Infomações encontradas
    """
    data_dict = {}
    cnj = r'\b\d{7}-\d{2}\.\d{4}\.\d{1,2}\.\d{2}\.\d{4}\b'

    cnj_captured = False
    for txt in list_data:
        if re.search(cnj, txt) and not cnj_captured:
            data_dict['cnj'] = re.findall(cnj, txt)[0]
            cnj_captured = True

        if 'Imptte' in txt:
            data_dict['autor'] = txt.split('Imptte')[1].strip()
        if 'Imptdo' in txt:
            data_dict['reu'] = txt.split('Imptdo')[1].strip()

        if 'Reqte' in txt and 'Imptte' not in txt:
            data_dict['autor'] = txt.split('Reqte')[1].strip()
        if 'Reqdo' in txt and 'Imptdo' not in txt:
            reu = txt.split('Reqdo')[1].strip()
            if data_dict.get('reu'):
                data_dict['reu'] = data_dict['reu'] + ',' + reu
            else:
                data_dict['reu'] = reu
        # if "OAB" in txt:
        #     try:
        #         data_dict["autor"] = list_data[list_data.index(txt) + 1]
        #         data_dict["reu"] = list_data[list_data.index(txt) + 6]
        #     except Exception as e:
        #         print(e)
        if txt in data_params:
            data_dict[data_params[txt]] = list_data[list_data.index(txt) + 1]

    return data_dict
