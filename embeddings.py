# Projeto 3 – Sistema de Recomendação Semântica com Embeddings, Banco Vetorial, Filtros de Metadados e IA Generativa
# Módulo responsável por carregar e encapsular o modelo de embeddings

# Importa a classe SentenceTransformer da biblioteca sentence-transformers
from sentence_transformers import SentenceTransformer

# Define a classe EmbeddingModel, responsável por gerenciar o modelo de embeddings
class EmbeddingModel:
    
    # Método construtor da classe
    def __init__(self):
        
        # Inicializa o modelo pré-treinado all-MiniLM-L6-v2 para geração de embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    # Define o método responsável por gerar embeddings a partir de um texto de entrada
    def get_embedding(self, text):
        
        # Codifica o texto em um vetor numérico e converte o resultado para uma lista Python
        return self.model.encode(text).tolist()
