# pipeline_process_processo

Teste técnico – Analista Desenvolvedor Back End - Phython

1-> Construa uma interface simples utilizando a tecnologia de sua preferência, onde um usuário possa
inserir de uma a cinco cópias integrais de processos jurídicos em formato pdf.

2-> Esses documentos devem ser direcionados à uma fila, em um serviço de mensageria, para que
possam ser analisados, um a um, por uma API, que deverá extrair as seguintes informações:

- nome do autor do processo
- documento do autor do processo
- nome(s) do(s) réu(s) do processo
- documento(s) do(s) réu(s) do processo

Essas informações deverão ser estruturadas em uma `planilha`, deixando claro quais informações dizem
respeito a qual processo e `disponibilizada quando completa`,
de alguma forma, `alertando o usuário de sua disponibilidade.`

O segundo item deve obrigatoriamente ser feito utilizando Python.

`Suba código da solução completa no Git e envie o link.`

Caso precise, insira observações no corpo do e-mail quando enviar o link.


## Funcionalidades Principais

1. **Upload de PDF**: O usuário pode fazer upload de arquivos PDF diretamente pelo frontend de 1 a 5 pdf.
2. **Fila de Processamento**: Os arquivos enviados são colocados em uma fila que vai acionar uma api para fazer o processamento do pdf, extraindo as informações.
3. **Extração de Informações**: O sistema utiliza uma API para extrair informações relevantes dos PDFs, para retorna um arquivo csv para o usuario.
4. **Gerenciamento de Tarefas**: Utiliza `Rabbitmq` e `Celery` para orquestrar o processamento e o `Redis` como backend de resultado.

## Tecnologias Utilizadas

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Fila de Mensagens**:  [RabbitMQ ](https://www.rabbitmq.com/)
- **Backend de Resultado**: [Redis](https://redis.io/)
- **Orquestração de Tarefas**: [Celery](https://docs.celeryproject.org/)
- **Containerização**: [Docker](https://www.docker.com/)

## Como Executar o Projeto

### 1. Requisitos

- `Docker` e `Docker Compose` instalados na máquina.
- Python 3.12 (caso queira rodar localmente sem Docker).

### 2. Clonando o Repositório

```bash
https://github.com/MieleSantos/pipeline_process_processo.git
```
### 3. Crie um arquivo .env na raiz do diretório, com as seguintes variaveis

```bash
URL_BASE=http://api:8000/process/
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/0
RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest
```
**Nota** Estou usando as credencias padrões do rabbitmq, para produção altera essa configuração
### 4. Executando com Docker Compose

```bash
docker-compose up --build -d
```

Isso iniciará os seguintes containers:

- **Frontend(front-1)**: Aplicativo Streamlit na porta `8501` 
- **Backend(api-1)**: API FastAPI na porta `8000`
- **Worker(worker_task_process_files-1)**: Worker Celery para processar as tarefas na fila.
- **Backend Resultado (redis-1)**: Redis para guarda o resultado para consultas dos status das tasks
- **Fila(rabbitmq)**: Rabbitmq como broker para gerenciar as tasks do celery



### 5. Testando o Sistema

1. Acesse o frontend em: [http://localhost:8501](http://localhost:8501)
2. Envie um arquivo PDF pelo upload.
3. O sistema processará o(s) arquivo(s) e exibirá as informações extraídas, permitindo fazer o download em arquivo csv

## Estrutura do Projeto

```
.
├── api/                  # Código da API FastAPI
├── main.py               # Aplicativo Streamlit
├── config_celery.py      # Configuração do Celery
├── docker-compose.yml    # Configuração do Docker Compose
├── Dockerfile            # Dockerfile do Backend
├── tasks.py              # Tasks do Worker Celery
├── pyproject.toml        # Dependências Python
└── README.md             # Documentação do projeto
└── utils.py              # Para funções extras
```
