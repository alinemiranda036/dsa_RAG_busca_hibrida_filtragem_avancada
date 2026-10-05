# 🛍️ Consultor de Compras Inteligente - RAG com Filtragem Avançada

Um assistente de recomendação de produtos alimentado por **RAG (Retrieval-Augmented Generation)** que combina busca semântica vetorial, filtros de metadados avançados e geração de resposta com IA generativa para criar uma experiência de e-commerce inteligente.

## 📋 Descrição do Projeto

Este projeto implementa um sistema completo de recomendação de produtos que:

- **Busca Semântica Vetorial**: Encontra produtos semanticamente similares usando embeddings
- **Filtros Avançados de Metadados**: Refina resultados por categoria, marca e faixa de preço
- **Geração Inteligente**: Usa um LLM via Groq (`openai/gpt-oss-120b`) para gerar recomendações personalizadas
- **Banco Vetorial**: Utiliza Qdrant para armazenar e recuperar produtos através de embeddings
- **Interface Interativa**: Streamlit para experiência de usuário amigável
- **Processamento Local**: Funciona com banco vetorial em Docker

## 🎯 Caso de Uso

Ideal para:
- 🛒 **E-commerce**: Recomendação de produtos com contexto
- 💡 **Assistentes Virtuais**: Sugestões inteligentes baseadas em intenção
- 📱 **Aplicações de Catálogo**: Busca semântica em grandes volumes de produtos
- 🔬 **Prototipagem de IA**: Demonstrar RAG com filtros empresariais
- 🎓 **Educação**: Aprender sobre embeddings, bancos vetoriais e RAG

## 🏗️ Arquitetura

```
┌──────────────────────────────────────────────────────────────┐
│            Pergunta do Usuário                               │
│   "Quero um notebook leve para viajar"                       │
└────────────────┬─────────────────────────────────────────────┘
                 │
         ┌───────▼──────────┐
         │  Embedding Model │ (sentence-transformers)
         │  Gera vetor da   │ representação semântica
         │  pergunta        │
         └───────┬──────────┘
                 │
     ┌───────────┼──────────────┐
     │           │              │
     │     ┌─────▼─────┐        │
     │     │  Filtros  │◄───────┤ Categoria, Marca,
     │     │Metadados  │        │ Preço mín/máx
     │     └─────┬─────┘        │
     │           │              │
     ├───────────┴──────────────┤
     │
     └───────┬──────────────────┐
             │ Busca Vetorial no Qdrant
             │ (com filtros aplicados)
         ┌───▼──────────────┐
         │ Produtos         │
         │ Relevantes       │
         │ Recuperados      │
         └───┬──────────────┘
             │
     ┌───────▼──────────────────┐
     │  Prompt + Contexto       │
     │  (produtos recuperados)  │
     └───┬──────────────────────┘
         │
     ┌───▼──────────────────┐
     │  Groq (LLM)          │
     │  Gera Recomendação   │
     └───┬──────────────────┘
         │
     ┌───▼──────────────────┐
     │   Recomendação Final │
     │   (Contextualizada)  │
     │   + Lista de         │
     │     Produtos         │
     └──────────────────────┘
```

## 📁 Estrutura do Projeto

```
dsa_RAG_busca_hibrida_filtragem_avancada/
├── dsa_app.py                   # Interface Streamlit (UI)
├── dsa_ingestao.py              # Script de indexação de produtos
├── dsa_testa_qdrant.py          # Teste do cliente Qdrant
├── docker-compose.yml           # Sobe o Qdrant em container
├── requirements.txt             # Dependências Python
├── .gitignore                   # Arquivos que não devem ir para o Git (.env, venv, qdrant_data)
├── dados/
│   └── produtos.json            # Catálogo de produtos (6 itens)
├── img/                         # Imagens dos produtos exibidas na interface
├── src/
│   ├── embeddings.py            # Geração de embeddings
│   ├── vector_db.py             # Operações com Qdrant
│   └── llm_service.py           # Integração com o LLM via Groq
├── .env                         # Você cria (passo 3) - não vem no repositório
├── qdrant_data/                 # Criado automaticamente pelo Docker ao subir o Qdrant
└── README.md                    # Este arquivo
```

### Descrição dos Arquivos Principais

- `dsa_app.py`: Aplicação principal em Streamlit com interface interativa
- `dsa_ingestao.py`: Script responsável por carregar o catálogo e indexá-lo no Qdrant
- `dsa_testa_qdrant.py`: Verifica se a biblioteca do Qdrant está instalada e o cliente pode ser criado
- `docker-compose.yml`: Inicia o serviço Qdrant em container
- `requirements.txt`: Dependências do projeto
- `dados/produtos.json`: Dataset de produtos utilizado para indexação
- `img/`: Imagens dos produtos, referenciadas pelo campo `image` do catálogo
- `src/embeddings.py`: Módulo para geração de embeddings usando sentence-transformers
- `src/vector_db.py`: Operações com Qdrant (criação da coleção, inserção, busca com filtros)
- `src/llm_service.py`: Integração com Groq para geração de recomendações

## 🚀 Como Executar

### 1️⃣ Pré-requisitos

- Python 3.11 ou superior (testado em 3.11 e 3.12; em 3.10 a instalação falha)
- pip
- Docker Desktop (ou Docker Engine + Docker Compose) instalado **e em execução**, para o Qdrant
- Conta na Groq para gerar a chave de API (gratuita, passo 3)
- Alguns GB livres em disco para as dependências (o PyTorch é o maior pacote)
- Internet na primeira execução, para baixar a imagem do Qdrant e o modelo de embeddings do Hugging Face
- Portas `6333` (Qdrant) e `8501` (Streamlit) livres

### 2️⃣ Instalação

```bash
# Clone o repositório
git clone https://github.com/alinemiranda036/dsa_RAG_busca_hibrida_filtragem_avancada.git
cd dsa_RAG_busca_hibrida_filtragem_avancada

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/macOS
# ou
venv\Scripts\activate      # Windows

# Instale as dependências
pip install -r requirements.txt
```

### 3️⃣ Configurar Variáveis de Ambiente

O projeto lê **três** variáveis de um arquivo `.env`. Sem elas a ingestão e a aplicação não funcionam.

**Como criar a chave da Groq** (cada pessoa usa a sua; é gratuita, com limite de requisições):

1. Acesse https://console.groq.com e crie uma conta (ou entre com Google/GitHub)
2. No menu, abra **API Keys** (ou vá direto em https://console.groq.com/keys)
3. Clique em **Create API Key**, dê um nome (ex: `rag-busca-hibrida`) e confirme
4. Copie a chave gerada (começa com `gsk_`). Ela só é exibida uma vez; se perder, crie outra

**Como configurar no projeto:**

Crie um arquivo chamado `.env` na raiz do projeto (mesma pasta do `dsa_app.py`), usando um editor de texto, com o conteúdo:

```bash
GROQ_API_KEY=sua_chave_aqui
QDRANT_URL=http://localhost:6333
COLLECTION_NAME=produtos
```

- `GROQ_API_KEY`: substitua `sua_chave_aqui` pela chave copiada, sem aspas e sem espaços
- `QDRANT_URL`: endereço do Qdrant que o `docker-compose.yml` sobe (mantenha como está)
- `COLLECTION_NAME`: nome da coleção onde os produtos serão indexados (pode manter `produtos`)

> ⚠️ Nunca faça commit do `.env` nem compartilhe sua chave. O `.gitignore` do repositório já ignora o `.env`, a pasta `venv/` e a `qdrant_data/`.

> 💡 No Windows, crie o arquivo pelo editor (VS Code, Bloco de Notas) em vez de usar `echo ... > .env` no PowerShell, que pode salvar o arquivo em uma codificação que o projeto não lê.

### 4️⃣ Iniciar Qdrant (Banco Vetorial)

Com o Docker em execução, na pasta do projeto:

```bash
docker compose up -d
```

(em versões antigas do Docker o comando é `docker-compose up -d`)

Verifique se está rodando:

```bash
docker ps                             # deve listar o container qdrant_dsa
curl http://localhost:6333/healthz    # deve responder "healthz check passed"
```

Você também pode abrir `http://localhost:6333/dashboard` no navegador para ver o painel do Qdrant.

Isso sobe um container com Qdrant na porta `6333` e cria a pasta `qdrant_data/` com os dados persistidos.

### 5️⃣ Testar o Cliente Qdrant (opcional)

```bash
python dsa_testa_qdrant.py
```

Saída esperada: `✅ Cliente instanciado com sucesso.`

Esse script confirma que a biblioteca está instalada e mostra qual Python está em uso. Ele **não** garante que o Qdrant está no ar; para isso use as verificações do passo 4.

### 6️⃣ Indexar Produtos no Banco Vetorial

Antes de usar a aplicação, é necessário carregar o catálogo no banco vetorial:

```bash
python dsa_ingestao.py
```

Esse processo:

- Lê o arquivo `dados/produtos.json`
- Gera embeddings para cada produto (na primeira vez, baixa o modelo `all-MiniLM-L6-v2`)
- Cria a coleção e os índices de filtro no Qdrant
- Insere os registros com seus metadados

Saída esperada:

```
Iniciando ingestão de dados...
Coleção e Índices criados com sucesso.
6 produtos inseridos.
Ingestão concluída!
```

Avisos de depreciação (`DeprecationWarning`) podem aparecer e não são erros. O script pode ser executado novamente sem problemas: ele recria a coleção do zero a cada execução.

### 7️⃣ Executar a Aplicação Streamlit

```bash
streamlit run dsa_app.py
```

A interface será aberta no navegador em: `http://localhost:8501`

### 8️⃣ Conferir se Está Tudo Funcionando

Na interface, faça estes testes:

| Teste | Resultado esperado |
|-------|--------------------|
| Sem filtros, pergunte "Preciso de um notebook bom para trabalhar em viagens" | Recomendação de um notebook (MacBook Air M2 ou Dell XPS 13) e até 3 produtos listados à direita, com imagem |
| Categoria `Áudio`, pergunte por um notebook | Apenas Sony WH-1000XM5 e JBL Flip 6 aparecem como contexto, e a IA informa que nenhum atende |
| Marca `Sony` e preço máximo `3000` | Apenas o Sony WH-1000XM5 aparece |
| Categoria `Games` e marca `Apple` | Mensagem "Nenhum produto encontrado com esses filtros e termos." |

### 🧯 Problemas Comuns

| Sintoma | Causa provável | Como resolver |
|---------|----------------|---------------|
| `Connection refused` na ingestão ou ao abrir a app | Qdrant não está rodando | Abra o Docker e execute `docker compose up -d` |
| Erro na ingestão mesmo com o Qdrant no ar | `COLLECTION_NAME` ou `QDRANT_URL` ausentes no `.env` | Revise o passo 3 |
| "O catálogo ainda não foi indexado" na app | Ingestão não foi executada | Rode `python dsa_ingestao.py` |
| Erro da Groq sobre `api_key` ao abrir a app, ou erro 401 ao gerar a recomendação | `GROQ_API_KEY` ausente ou inválida | Confira a chave no `.env` e reinicie a app |
| `ModuleNotFoundError: No module named 'src'` | Comando executado fora da pasta do projeto | Entre na raiz do projeto antes de rodar os scripts |
| "Imagem indisponível" nos produtos | Pasta `img/` ausente | Confirme que o repositório foi clonado por completo |
| Erro ao instalar dependências | Python 3.10 ou anterior | Use Python 3.11+ |

Para encerrar o Qdrant: `docker compose down` (os dados continuam em `qdrant_data/`).

## 🔧 Componentes Principais

### 1. `dsa_ingestao.py` - Indexação de Produtos

Carrega o catálogo de produtos e os indexa no Qdrant:

```python
def dsa_executa_ingestao():
    # 1. Lê dados/produtos.json
    # 2. Inicializa modelo de embeddings
    # 3. Inicializa conexão com Qdrant
    # 4. Cria coleção e índices de filtro
    # 5. Insere dados com embeddings e metadados
```

**Fluxo de Ingestão:**
- Lê JSON com catálogo de produtos
- Inicializa modelo `all-MiniLM-L6-v2` para embeddings
- Recria a coleção no Qdrant (384 dimensões, distância cosseno) e cria índices para `category`, `brand` e `price`
- Gera o embedding a partir de `nome - descrição` de cada produto
- Cada produto armazena embedding + todos os campos do JSON como metadados (payload)

**Formato de cada produto em `dados/produtos.json`:**

```json
{
  "name": "JBL Flip 6",
  "description": "Caixa de som bluetooth portátil e resistente à água.",
  "category": "Áudio",
  "brand": "JBL",
  "price": 600,
  "link": "https://...",
  "image": "img/JBL_Flip_6.png"
}
```

### 2. `src/embeddings.py` - Geração de Embeddings

Utiliza `sentence-transformers` para converter texto em vetores numéricos:

```python
class EmbeddingModel:
    def __init__(self):
        # Carrega modelo pré-treinado leve (384 dimensões)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def get_embedding(self, text):
        # Retorna o embedding como lista Python (384 valores)
        return self.model.encode(text).tolist()
```

**Características:**
- Modelo leve e rápido (ideal para executar localmente, em CPU)
- Gera vetores de 384 dimensões
- Treinado principalmente em inglês; funciona para este catálogo em português, mas um modelo multilíngue tende a dar resultados melhores (veja Configuração Avançada)

### 3. `src/vector_db.py` - Operações com Qdrant

Gerencia todas as operações com o banco vetorial:

```python
class VectorDB:
    def create_collection(self):
        # Recria a coleção e os índices de category, brand e price

    def upsert_data(self, data, embedding_model):
        # Gera embeddings e insere os produtos com seus metadados

    def search(self, query_vector, category=None, brand=None,
               price_min=None, price_max=None, limit=5):
        # Busca vetorial com filtros de metadados aplicados
```

A URL do Qdrant e o nome da coleção vêm das variáveis `QDRANT_URL` e `COLLECTION_NAME` do `.env`.

**Filtros Suportados:**
- `category`: Games, Notebooks, Áudio
- `brand`: Sony, Microsoft, Apple, Dell, JBL
- `price_min` / `price_max`: faixa de preço do produto

O valor `"Todas"` em categoria ou marca desativa o respectivo filtro.

**Exemplo de Busca com Filtros:**
```python
resultados = db.search(
    query_vector=query_vector,
    category="Notebooks",
    brand="Todas",
    price_min=0,
    price_max=8000,
    limit=3
)
```

### 4. `src/llm_service.py` - Integração com IA Generativa

Conecta com Groq para gerar recomendações personalizadas:

```python
class LLMService:
    def __init__(self):
        # Lê a GROQ_API_KEY do .env
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate_recommendation(self, user_query, context_products):
        # Formata prompt com contexto dos produtos
        # Chama o modelo openai/gpt-oss-120b via Groq API
        # Retorna recomendação personalizada
```

**Fluxo:**
1. Recebe pergunta do usuário e produtos recuperados
2. Formata prompt com instruções e contexto (nome, marca, preço e descrição)
3. Envia para o modelo `openai/gpt-oss-120b` via Groq (temperatura 0.5)
4. Retorna recomendação em linguagem natural

### 5. `dsa_app.py` - Interface Streamlit

Interface interativa com:
- ✅ Chat com campo de busca semântica por intenção
- ✅ Filtros laterais (categoria, marca, faixa de preço)
- ✅ Recomendação gerada por IA
- ✅ Produtos recuperados com imagem, marca, categoria, descrição e link para a loja
- ✅ Histórico da conversa durante a sessão

## 📊 Exemplo de Fluxo Completo

### 1. Usuário consulta:
```
"Preciso de um notebook bom para trabalhar em viagens"
```

### 2. Sistema processa:
```python
# Gera embedding da pergunta
query_vector = embed_model.get_embedding(
    "Preciso de um notebook bom para trabalhar em viagens"
)

# Busca no Qdrant com os filtros escolhidos na barra lateral
search_results = db.search(
    query_vector=query_vector,
    category="Notebooks",
    brand="Todas",
    price_min=0,
    price_max=10000,
    limit=3
)

# Extrai os produtos (payloads) retornados
context_products = [hit.payload for hit in search_results]
# Ex.: MacBook Air M2 e Dell XPS 13
```

### 3. Gera recomendação:
```python
# O LLMService monta o prompt com a pergunta e os produtos recuperados
answer = llm_service.generate_recommendation(prompt, context_products)
```

### 4. Resposta:

A IA devolve um texto recomendando um dos produtos recuperados e explicando o motivo (por exemplo, o MacBook Air M2 por ser leve e ter bateria de longa duração). Ao lado, a interface lista os produtos usados como contexto.

## 📚 Exemplo de Uso Prático

Na interface, você pode testar perguntas como:

- "Preciso de um notebook bom para trabalhar em viagens"
- "Quero um console para jogar com meus amigos"
- "Qual fone é melhor para usar no avião?"
- "Procuro uma caixa de som para levar à praia"

Também é possível usar os filtros laterais para restringir por:

- **Categoria**: Games, Notebooks, Áudio
- **Marca**: Sony, Microsoft, Apple, Dell, JBL
- **Faixa de Preço**: de R$ 0 a R$ 10.000

## ⚙️ Configuração Avançada

### Mudar o modelo de embedding

```python
# Em src/embeddings.py
self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
# ou qualquer modelo da HuggingFace
```

Se o novo modelo gerar vetores com outra dimensão, ajuste também `size = 384` em `src/vector_db.py`. Depois de trocar o modelo, rode `python dsa_ingestao.py` novamente.

### Ajustar a quantidade de produtos recuperados

```python
# Em dsa_app.py
search_results = db.search(..., limit = 3)   # aumente para trazer mais produtos
```

### Adicionar produtos ou filtros

- Para novos produtos: edite `dados/produtos.json` (mesmos campos dos existentes), coloque a imagem em `img/` e rode a ingestão novamente
- Para novas categorias ou marcas: inclua também nas listas `categorias` e `marcas` do `dsa_app.py`
- Para um novo campo de filtro (cor, tamanho, etc.): crie o índice em `create_collection` e a condição em `search`, ambos em `src/vector_db.py`

### Trocar o modelo de LLM

```python
# Em src/llm_service.py
model = "openai/gpt-oss-120b",
# alternativa já comentada no código: "llama-3.3-70b-versatile"
```

A lista de modelos disponíveis está em https://console.groq.com/docs/models.

## 📊 Comparação com Alternativas

| Abordagem | Vantagens | Desvantagens |
|-----------|-----------|-------------|
| **Apenas Filtros SQL** | Simples, rápido, preciso | Sem compreensão semântica |
| **Apenas Busca Vetorial** | Entende contexto, sinônimos | Ignora filtros exatos, pode ser lento |
| **Híbrida (Este Projeto)** ✅ | Combina o melhor dos dois | Requer mais configuração |

## 🛡️ Segurança e Privacidade

- ✅ **Dados Locais**: Produtos armazenados no Qdrant local (não em nuvem)
- ✅ **Chave de API Segura**: Carregada apenas de variáveis de ambiente
- ✅ **Sem Histórico Persistente**: Consultas não são armazenadas permanentemente
- ✅ **Código Aberto**: Totalmente auditável
- ⚠️ **Nota**: Groq processa o prompt para gerar recomendação (API externa)

## 📈 Melhorias Futuras

- [ ] Suportar múltiplos formatos de entrada (CSV, API de catálogos)
- [ ] Análise de feedback de usuário para melhorar recomendações
- [ ] Personalização por perfil de comprador
- [ ] Integração com APIs de e-commerce reais (Shopify, WooCommerce)
- [ ] Dashboard de analytics e métricas
- [ ] Suporte a múltiplos idiomas
- [ ] Cache de embeddings para melhor performance
- [ ] API REST
- [ ] Testes automatizados
- [ ] Sistema de rating de recomendações

## 🤝 Contribuindo

Contribuições são bem-vindas! Você pode:
1. Abrir issues para bugs ou sugestões
2. Submeter pull requests com melhorias
3. Adicionar novos filtros ou funcionalidades
4. Melhorar a documentação

## ⚠️ Observações Importantes

- O serviço de IA (Groq) depende de uma chave de acesso válida
- O sistema deve ter o catálogo indexado antes de executar as consultas (`python dsa_ingestao.py`)
- A IA pode gerar respostas úteis, mas não substitui validação humana em decisões críticas
- Caso a busca retorne pouco ou nenhum resultado, revise os filtros e o dataset carregado
- Certifique-se de que o Docker está rodando antes de iniciar a aplicação

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais e de demonstração. Verifique a política do repositório e as licenças das bibliotecas utilizadas antes de uso em produção.

## 📞 Suporte

Para dúvidas ou problemas:
- Abra uma issue no GitHub
- Consulte a documentação do Qdrant: https://qdrant.tech/documentation/
- Consulte a documentação Groq: https://console.groq.com/docs
- Documentação Sentence Transformers: https://www.sbert.net/

## 🎓 Referências e Recursos

- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Sentence Transformers](https://www.sbert.net/)
- [Groq API Documentation](https://console.groq.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [RAG Patterns & Best Practices](https://docs.llamaindex.ai/en/stable/modules/retrieval_augmented_generation/)
- [Vector Search com Filtros](https://qdrant.tech/articles/vector-search-filtering/)
