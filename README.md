# talk-with-your-code-v1

O **talk-with-your-code-v1** é uma ferramenta que permite interagir com seu codebase utilizando inteligência artificial. Por meio de técnicas de NLP, embeddings e busca de similaridade, o sistema permite que você faça perguntas técnicas sobre seu código e receba respostas concisas, referenciando os arquivos e trechos mais relevantes.

---

## Conceito

Este projeto tem como objetivo facilitar a consulta e compreensão de grandes codebases. Ele realiza os seguintes passos:

- **Ingestão do Codebase**:  
  Os arquivos presentes na pasta `./codebase` são carregados e divididos em fragmentos (chunks) usando o `RecursiveCharacterTextSplitter`.

- **Geração de Embeddings**:  
  Cada fragmento é convertido em um vetor (embedding) utilizando o modelo `microsoft/graphcodebert-base` via HuggingFace. Esses embeddings são armazenados em uma coleção no **ChromaDB**.

- **Consulta e Resposta**:  
  Quando uma consulta é feita, o sistema realiza uma busca de similaridade para recuperar os trechos de código mais relevantes e, em seguida, utiliza o modelo **ChatDeepSeek** para gerar uma resposta técnica e informativa, referenciando os arquivos e trechos pertinentes.

---

## Funcionalidades

- **Ingestão do Codebase**: Processa os arquivos do diretório `./codebase` e armazena os embeddings em uma coleção no ChromaDB.
- **Consulta Inteligente**: Permite fazer perguntas sobre o código e obtém respostas baseadas no contexto do codebase.
- **Integração com Docker**: O serviço do ChromaDB pode ser iniciado facilmente via `docker-compose`.

---

## Pré-requisitos

- **Python 3.8+**
- **Docker** (para rodar o ChromaDB via docker-compose)
- Dependências listadas em `requeriments.txt`

---

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/RomanJoseph/talk-with-your-code-v1.git
   cd talk-with-your-code-v1
   ```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requeriments.txt
   ```

---

## Configuração

1. **Configure as variáveis de ambiente:**  
   Crie um arquivo `.env` (baseado no `.env.example`) e preencha as seguintes variáveis:

   - `DEEPSEEK_API_KEY`: Sua chave de API para o ChatDeepSeek.
   - `HF_CACHE_DIR`: Diretório para cache do HuggingFace (por exemplo, `./cache/huggingface`).
   - `HF_TOKEN`: Seu token do HuggingFace.

2. **Atenção:**  
   Certifique-se de que o arquivo `.env` está listado no `.gitignore` para não versionar informações sensíveis.

---

## Execução

### 1. Inicializando o ChromaDB

Utilize o docker-compose para subir o serviço do ChromaDB:

```bash
docker-compose up -d
```

O serviço ficará disponível em [http://localhost:8000](http://localhost:8000).

### 2. Ingestão do Codebase

Certifique-se de que os arquivos do seu codebase estejam na pasta `./codebase`. Em seguida, execute:

```bash
python runner.py ingest
```

Esse comando:

- Carrega os arquivos do diretório.
- Divide o conteúdo em chunks.
- Gera os embeddings e os armazena na coleção `codebase_v3` do ChromaDB.

### 3. Consultando o Codebase

Após a ingestão, você pode fazer consultas sobre o código. Utilize o seguinte comando:

```bash
python runner.py start "Sua pergunta sobre o código"
```

**Exemplo:**

```bash
python runner.py start "Como a função de ingestão divide os arquivos?"
```

O sistema realizará uma busca de similaridade e, com base nos documentos encontrados, retornará uma resposta técnica e concisa.

---

## Estrutura do Projeto

- **main.py**: Script principal que recebe a pergunta e exibe a resposta.
- **runner.py**: Gerencia os comandos disponíveis (ex.: `start` para consulta e `ingest` para ingestão).
- **utils/ingest.py**: Responsável pela ingestão e processamento dos arquivos do codebase.
- **utils/query.py**: Realiza a consulta no vector store e interage com o LLM para gerar a resposta.
- **utils/embeddings.py**: Configura e gera os embeddings locais utilizando HuggingFace.
- **docker-compose.yml**: Define o serviço do ChromaDB necessário para o armazenamento dos embeddings.

---

## Considerações Finais

O **talk-with-your-code-v1** é uma ferramenta poderosa para ajudar desenvolvedores a entender e navegar em grandes codebases de forma inteligente. Se você encontrar algum problema ou tiver sugestões, sinta-se à vontade para contribuir com o projeto através de issues ou pull requests.

Boa codificação!
