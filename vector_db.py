# Projeto 3 – Sistema de Recomendação Semântica com Embeddings, Banco Vetorial, Filtros de Metadados e IA Generativa
# Módulo responsável por carregar e encapsular o banco vetorial e suas operações

# Importa o módulo os para acesso a variáveis de ambiente
import os

# Importa o cliente principal do Qdrant
from qdrant_client import QdrantClient

# Importa as estruturas e modelos necessários para vetores, filtros e condições
from qdrant_client.models import PointStruct, VectorParams, Distance, Filter, FieldCondition, MatchValue, Range

# Importa a função para carregar variáveis de ambiente a partir do arquivo .env
from dotenv import load_dotenv

# Carrega as variáveis de ambiente definidas no arquivo .env
load_dotenv()

# Define a classe VectorDB, responsável por gerenciar o banco de dados vetorial
class VectorDB:
    
    # Método construtor da classe
    def __init__(self):
        
        # Inicializa o cliente do Qdrant utilizando a URL definida nas variáveis de ambiente
        self.client = QdrantClient(url = os.getenv("QDRANT_URL"))
        
        # Define o nome da coleção a partir das variáveis de ambiente
        self.collection_name = os.getenv("COLLECTION_NAME")

    # Método responsável por criar ou recriar a coleção no Qdrant
    def create_collection(self):
        
        # Recria a coleção garantindo um estado limpo, indicado apenas para fins de demonstração
        self.client.recreate_collection(
            collection_name = self.collection_name,
            
            # Define a configuração dos vetores, incluindo dimensão e métrica de similaridade
            vectors_config = VectorParams(size = 384, distance = Distance.COSINE),
        )
        
        # Cria índice de payload para o campo category visando otimizar filtros
        self.client.create_payload_index(self.collection_name, field_name = "category", field_schema = "keyword")
        
        # Cria índice de payload para o campo brand visando otimizar filtros
        self.client.create_payload_index(self.collection_name, field_name = "brand", field_schema = "keyword")
        
        # Cria índice de payload para o campo price visando otimizar filtros numéricos
        self.client.create_payload_index(self.collection_name, field_name = "price", field_schema = "integer")
        
        # Exibe mensagem indicando sucesso na criação da coleção e índices
        print("Coleção e Índices criados com sucesso.")

    # Método responsável por inserir ou atualizar dados vetoriais na coleção
    def upsert_data(self, data, embedding_model):
        
        # Inicializa a lista que armazenará os pontos vetoriais
        points = []
        
        # Itera sobre os dados recebidos, gerando IDs sequenciais
        for idx, item in enumerate(data):
            
            # Concatena nome e descrição para gerar o texto de entrada do modelo de embeddings
            text_to_embed = f"{item['name']} - {item['description']}"
            
            # Gera o vetor de embedding a partir do texto
            vector = embedding_model.get_embedding(text_to_embed)
            
            # Cria a estrutura do ponto vetorial com ID, vetor e payload
            points.append(PointStruct(
                id = idx,
                vector = vector,
                payload = item
            ))
        
        # Realiza a operação de upsert no Qdrant
        self.client.upsert(collection_name = self.collection_name, points = points)
        
        # Exibe mensagem indicando quantos produtos foram inseridos
        print(f"{len(points)} produtos inseridos.")

    # Método responsável por realizar buscas vetoriais com filtros dinâmicos
    def search(self, query_vector, category = None, brand = None, price_min = None, price_max = None, limit = 5):
        
        # Inicializa a lista de condições de filtro
        filter_conditions = []

        # Adiciona filtro por categoria, caso seja informada e diferente de "Todas"
        if category and category != "Todas":
            filter_conditions.append(FieldCondition(key = "category", match = MatchValue(value = category)))
        
        # Adiciona filtro por marca, caso seja informada e diferente de "Todas"
        if brand and brand != "Todas":
            filter_conditions.append(FieldCondition(key = "brand", match = MatchValue(value = brand)))
            
        # Adiciona filtro por faixa de preço, caso algum dos limites seja informado
        if price_min is not None or price_max is not None:
            filter_conditions.append(
                FieldCondition(
                    key = "price",
                    range = Range(gte = price_min, lte = price_max)
                )
            )

        # Cria o filtro do Qdrant apenas se houver condições definidas
        qdrant_filter = Filter(must = filter_conditions) if filter_conditions else None

        # Executa a consulta vetorial no Qdrant com filtro opcional
        results = self.client.query_points(
            collection_name = self.collection_name,
            
            # Vetor de consulta utilizado para similaridade semântica
            query = query_vector,
            
            # Filtro dinâmico baseado nos parâmetros fornecidos
            query_filter = qdrant_filter,
            
            # Número máximo de resultados retornados
            limit = limit
        )
        
        # Retorna apenas os pontos encontrados na busca
        return results.points



