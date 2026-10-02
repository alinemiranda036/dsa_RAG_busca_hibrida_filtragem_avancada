# Consultor de Compras Inteligente

Sistema de recomendação de produtos baseado em busca semântica híbrida, filtros de metadados e geração de resposta com IA. O projeto combina embeddings, banco vetorial (Qdrant), filtros por categoria, marca e faixa de preço, e um modelo de linguagem para produzir recomendações contextualizadas em linguagem natural.

## Visão geral

Este projeto foi desenvolvido para demonstrar como construir uma solução de RAG (Retrieval-Augmented Generation) aplicada ao contexto de e-commerce. Em vez de responder apenas com conhecimento genérico, o sistema:

- converte a pergunta do usuário em embedding;
- busca produtos semanticamente similares em um banco vetorial;
- aplica filtros de metadados como categoria, marca e faixa de preço;
- recupera os produtos mais relevantes;
- envia esse contexto para um modelo de linguagem;
- retorna uma recomendação final em linguagem natural, explicando por que aquele produto faz sentido para a necessidade do cliente.

A interface web é construída com Streamlit, permitindo interação simples e rápida em um ambiente de demonstração ou prova de conceito.

## Objetivo do projeto

O objetivo principal é facilitar a descoberta de produtos eletrônicos com base na intenção do usuário, por exemplo:

- "Preciso de um notebook bom para viajar"
- "Quero um console para jogar com os amigos"
- "Qual fone é melhor para usar no avião?"
- "Procuro uma caixa de som para levar à praia"

Além da busca semântica, o sistema também permite refinar a busca com filtros, simulando cenários reais de e-commerce e recomendação.

## Principais tecnologias

- Python
- Streamlit
- Qdrant
- sentence-transformers
- Hugging Face transformers
- Groq
- Docker Compose

## Arquitetura do sistema

O fluxo principal do projeto é o seguinte:

1. O usuário envia uma consulta no front-end em Streamlit.
2. A aplicação transforma a mensagem em embedding usando um modelo de embeddings.
3. A busca é executada no Qdrant com filtros de metadados.
4. Os produtos recuperados são enviados ao modelo de linguagem.
5. A IA gera uma resposta contextualizada com base no catálogo pesquisado.
6. A interface exibe a recomendação e os produtos relevantes.

## Funcionalidades

- Busca semântica por intenção do usuário
- Filtros por categoria, marca e faixa de preço
- Recuperação híbrida de produtos relevantes
- Resposta gerada por IA com contexto do catálogo
- Interface amigável em Streamlit
- Persistência em banco vetorial com Qdrant
- Estrutura pronta para extensão com novos produtos, filtros ou modelos

## Estrutura do repositório

```text
.
├── README.md
├── docker-compose.yml
├── dsa_app.py
├── dsa_ingestao.py
├── dsa_testa_qdrant.py
├── requirements.txt
├── dados/
│   └── produtos.json
├── src/
│   ├── embeddings.py
│   ├── llm_service.py
│   └── vector_db.py
└── qdrant_data/
```

### Descrição dos arquivos principais

- `dsa_app.py`: aplicação principal em Streamlit.
- `dsa_ingestao.py`: script responsável por carregar os dados e indexá-los no Qdrant.
- `dsa_testa_qdrant.py`: arquivo para testar a conexão e a operação do banco vetorial.
- `docker-compose.yml`: inicia o serviço Qdrant em container.
- `requirements.txt`: dependências do projeto.
- `dados/produtos.json`: dataset de produtos utilizado para indexação.
- `src/`: módulos responsáveis por embeddings, busca vetorial e integração com o modelo de linguagem.

## Pré-requisitos

Antes de iniciar, confirme que você possui:

- Python 3.10+
- pip
- Docker e Docker Compose
- Acesso a uma API de modelo de linguagem da Groq (ou ajuste o serviço de LLM para outro provedor)

## Configuração do ambiente

### 1) Clonar o repositório

```bash
git clone https://github.com/alinemiranda036/dsa_RAG_busca_hibrida_filtragem_avancada.git
cd dsa_RAG_busca_hibrida_filtragem_avancada
```

### 2) Criar ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# ou
.venv\Scripts\activate      # Windows
```

### 3) Instalar dependências

```bash
pip install -r requirements.txt
```

### 4) Iniciar o Qdrant

```bash
docker compose up -d
```

Isso subirá um container com Qdrant na porta `6333`.

## Execução do projeto

### Indexar os dados

Antes de usar a aplicação, é necessário carregar o catálogo no banco vetorial:

```bash
python dsa_ingestao.py
```

Esse processo:

- lê o arquivo `dados/produtos.json`;
- gera embeddings dos produtos;
- cria a coleção no Qdrant;
- insere os registros com seus metadados.

### Rodar a aplicação Streamlit

```bash
streamlit run dsa_app.py
```

A interface será aberta no navegador, permitindo a interação com o sistema.

## Exemplo de uso

Na interface, você pode testar perguntas como:

- "Quero um notebook leve para viagens"
- "Qual console é melhor para jogar com amigos?"
- "Preciso de um fone de ouvido para usar no avião"
- "Quero uma caixa de som portátil para praia"

Também é possível usar os filtros laterais para restringir por:

- categoria;
- marca;
- faixa de preço.

## Observações importantes

- O serviço de IA depende de uma chave de acesso válida da Groq.
- O sistema deve ter o catálogo indexado antes de executar as consultas.
- A IA pode gerar respostas úteis, mas não substitui validação humana em decisões críticas.
- Caso a busca retorne pouco ou nenhum resultado, revise os filtros e o dataset carregado.

## Caso de uso real

Este projeto funciona como exemplo de aplicação prática de IA em ambientes de recomendação, com foco em:

- recuperação eficiente de produtos;
- contexto enriquecido para modelos generativos;
- combinação de busca semântica com filtros empresariais;
- experiência interativa em UX de e-commerce.

## Conclusão

O repositório demonstra, de forma prática e didática, como combinar busca vetorial, filtros de metadados e modelos de linguagem para construir um sistema de recomendação inteligente. Ele é uma base excelente para estudos, provas de conceito e extensões para cenários reais de recomendação e busca em catálogo.

## Licença

Este projeto foi desenvolvido para fins educacionais e de demonstração. Verifique a política do repositório e as licenças das bibliotecas utilizadas antes de uso em produção.

---

Se quiser, também posso ajustar o README para um estilo mais institucional, mais técnico ou mais visual, com badges, screenshots e uma seção de arquitetura em diagrama.
