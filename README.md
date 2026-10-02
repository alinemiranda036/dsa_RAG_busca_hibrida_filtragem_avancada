# 🛍️ Consultor de Compras Inteligente - RAG com Filtragem Avançada

Um assistente de recomendação de produtos alimentado por **RAG (Retrieval-Augmented Generation)** que combina busca semântica vetorial, filtros de metadados avançados e geração de resposta com IA generativa para criar uma experiência de e-commerce inteligente.

## 📋 Descrição do Projeto

Este projeto implementa um sistema completo de recomendação de produtos que:

- **Busca Semântica Vetorial**: Encontra produtos semanticamente similares usando embeddings
- **Filtros Avançados de Metadados**: Refina resultados por categoria, marca e faixa de preço
- **Geração Inteligente**: Usa Groq (LLaMA) para gerar recomendações personalizadas
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
     │  Groq (LLaMA)        │
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
├── dsa_testa_qdrant.py          # Teste de conexão com Qdrant
├── docker-compose.yml           # Orchestração do Qdrant
├── requirements.txt             # Dependências Python
├── dados/
│   └── produtos.json            # Catálogo de produtos
├── src/
│   ├── embeddings.py            # Geração de embeddings
│   ├── vector_db.py             # Operações com Qdrant
│   └── llm_service.py           # Integração com Groq/LLaMA
└── README.md                    # Este arquivo
```

### Descrição dos Arquivos Principais

- `dsa_app.py`: Aplicação principal em Streamlit com interface interativa
- `dsa_ingestao.py`: Script responsável por carregar o catálogo e indexá-lo no Qdrant
- `dsa_testa_qdrant.py`: Arquivo para testar a conexão e a operação do banco vetorial
- `docker-compose.yml`: Inicia o serviço Qdrant em container
- `requirements.txt`: Dependências do projeto
- `dados/produtos.json`: Dataset de produtos utilizado para indexação
- `src/embeddings.py`: Módulo para geração de embeddings usando sentence-transformers
- `src/vector_db.py`: Operações com Qdrant (busca, inserção, filtros)
- `src/llm_service.py`: Integração com Groq para geração de recomendações

## 🚀 Como Executar

### 1️⃣ Pré-requisitos

- Python 3.10+
- Docker e Docker Compose (para Qdrant)
- Chave de API da Groq (https://console.groq.com)
- pip

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

```bash
# Crie um arquivo .env na raiz do projeto
echo "GROQ_API_KEY=sua_chave_aqui" > .env
```

Obtenha sua chave de API em: https://console.groq.com

### 4️⃣ Iniciar Qdrant (Banco Vetorial)

```bash
# Na pasta do projeto
docker-compose up -d

# Verifique se está rodando
curl http://localhost:6333/health
```

Isso subirá um container com Qdrant na porta `6333`.

### 5️⃣ Indexar Produtos no Banco Vetorial

Antes de usar a aplicação, é necessário carregar o catálogo no banco vetorial:

```bash
python dsa_ingestao.py
```

Esse processo:

- Lê o arquivo `dados/produtos.json`
- Gera embeddings para cada produto
- Cria a coleção no Qdrant
- Insere os registros com seus metadados

### 6️⃣ Testar Conexão com Qdrant

```bash
python dsa_testa_qdrant.py
```

### 7️⃣ Executar a Aplicação Streamlit

```bash
streamlit run dsa_app.py
```

A interface será aberta no navegador em: `http://localhost:8501`

## 🔧 Componentes Principais

### 1. `dsa_ingestao.py` - Indexação de Produtos

Carrega o catálogo de produtos e os indexa no Qdrant:

```python
def dsa_executa_ingestao():
    # 1. Lê dados/produtos.json
    # 2. Inicializa modelo de embeddings
    # 3. Inicializa conexão com Qdrant
    # 4. Cria coleção com schema de produtos
    # 5. Insere dados com embeddings e metadados
```

**Fluxo de Ingestão:**
- Lê JSON com catálogo de produtos
- Inicializa modelo `all-MiniLM-L6-v2` para embeddings
- Cria schema no Qdrant com propriedades (título, conteúdo, categoria, marca, preço)
- Insere produtos em batch para melhor performance
- Cada produto armazena embedding + metadados para filtros

### 2. `src/embeddings.py` - Geração de Embeddings

Utiliza `sentence-transformers` para converter texto em vetores numéricos:

```python
class EmbeddingModel:
    def __init__(self):
        # Carrega modelo pré-treinado leve (384-dimensional)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def encode(self, text):
        # Retorna embedding (vetor 384-dimensional)
        return self.model.encode(text)
```

**Características:**
- Modelo leve e rápido (ideal para executar localmente)
- Gera vetores de 384 dimensões
- Treinado em 215M pares de sentenças
- Suporta múltiplos idiomas

### 3. `src/vector_db.py` - Operações com Qdrant

Gerencia todas as operações com o banco vetorial:

```python
class VectorDB:
    def create_collection(self):
        # Cria coleção com schema de produtos
    
    def upsert_data(self, products, embeddings):
        # Insere/atualiza produtos com embeddings e metadados
    
    def search_with_filters(self, query_vector, filters):
        # Busca com filtros de metadados aplicados
```

**Filtros Suportados:**
- `categoria`: Eletrônicos, Acessórios, Periféricos, etc.
- `marca`: Samsung, Apple, Sony, LG, etc.
- `preco_min`: Preço mínimo do produto
- `preco_max`: Preço máximo do produto

**Exemplo de Busca com Filtros:**
```python
filters = {
    "categoria": "Eletrônicos",
    "marca": "Samsung",
    "preco_min": 1000,
    "preco_max": 3000
}

resultados = db.search_with_filters(query_vector, filters, top_k=5)
```

### 4. `src/llm_service.py` - Integração com IA Generativa

Conecta com Groq para gerar recomendações personalizadas:

```python
class LLMService:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
    
    def generate_recommendation(self, query, products):
        # Formata prompt com contexto dos produtos
        # Chama LLaMA via Groq API
        # Retorna recomendação personalizada
```

**Fluxo:**
1. Recebe pergunta do usuário e produtos recuperados
2. Formata prompt com instruções e contexto
3. Envia para LLaMA 3 via Groq
4. Retorna recomendação em linguagem natural

### 5. `dsa_app.py` - Interface Streamlit

Interface interativa com:
- ✅ Campo de busca semântica por intenção
- ✅ Filtros laterais (categoria, marca, faixa de preço)
- ✅ Visualização de resultados em cards
- ✅ Recomendações geradas por IA
- ✅ Scores de relevância e similitude
- ✅ Detalhes completos do produto

## 📊 Exemplo de Fluxo Completo

### 1. Usuário consulta:
```
"Quero um notebook bom para viajar"
```

### 2. Sistema processa:
```python
# Gera embedding da pergunta
embedding_pergunta = embed_model.encode(
    "Quero um notebook bom para viajar"
)

# Define filtros aplicados (se houver)
filters = {
    "categoria": "Eletrônicos",
    "tipo": "Notebook",
    "preco_max": 5000
}

# Busca no Qdrant com filtros
resultados = db.search_with_filters(
    query_vector=embedding_pergunta,
    filters=filters,
    top_k=5
)

# Retorna:
# [Notebook Ultraleve X1 (score: 0.95),
#  Notebook Profissional Y2 (score: 0.89),
#  Notebook Gamer Z3 (score: 0.78)]
```

### 3. Gera recomendação:
```python
# Cria prompt contextualizado
prompt = f"""
Baseado nestes notebooks disponíveis:
{formata_produtos(resultados)}

Para a necessidade: "Quero um notebook bom para viajar"

Recomende o melhor produto e explique por quê.
Seja conciso e técnico.
"""

# Envia para LLaMA via Groq
resposta = llm_service.generate_recommendation(prompt)
```

### 4. Resposta:
```
🎯 Recomendação: Notebook Ultraleve X1

Por que este é o melhor para você:
✅ Peso: 1.2kg (extremamente portátil)
✅ Bateria: 12h (suficiente para dias inteiros)
✅ Processador: Intel i7 (roda tudo que precisa)
✅ Tela: 14" Full HD (compacta e nítida)
✅ Preço: R$ 3.999 (justo para a configuração)

Ideal para viagens por ser leve e robusto.
```

## 📚 Exemplo de Uso Prático

Na interface, você pode testar perguntas como:

- "Quero um notebook leve para viagens"
- "Qual console é melhor para jogar com amigos?"
- "Preciso de um fone de ouvido para usar no avião"
- "Quero uma caixa de som portátil para praia"
- "Qual monitor é melhor para programar?"

Também é possível usar os filtros laterais para restringir por:

- **Categoria**: Eletrônicos, Acessórios, Periféricos
- **Marca**: Samsung, Apple, Sony, LG, Positivo, etc.
- **Faixa de Preço**: Defina mín e máx customizados

## ⚙️ Configuração Avançada

### Mudar o modelo de embedding

```python
# Em src/embeddings.py
self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
# ou qualquer modelo da HuggingFace
# Opções: multi-qa-mpnet-base-dot-v1, distiluse-base-multilingual-cased-v2, etc.
```

### Ajustar sensibilidade da busca vetorial

```python
# Em src/vector_db.py
resultados = self.client.search(
    collection_name="produtos",
    query_vector=vector,
    score_threshold=0.7,  # Aumentar para mais similares
    limit=5
)
```

### Personalizar filtros de metadados

Edite `dados/produtos.json` e `src/vector_db.py` para:
- Adicionar novos campos de filtro (cor, tamanho, etc.)
- Criar facetas personalizadas
- Implementar lógica de filtros complexos (AND, OR, NOT)

### Configurar Groq API

```python
# Em src/llm_service.py
self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# Você pode mudar o modelo LLaMA se necessário
```

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
- O sistema deve ter o catálogo indexado antes de executar as consultas
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

---

**Desenvolvido com ❤️ para a comunidade de IA e E-commerce**
