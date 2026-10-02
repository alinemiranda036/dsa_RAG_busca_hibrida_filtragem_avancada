# Projeto 3 – Sistema de Recomendação Semântica com Embeddings, Banco Vetorial, Filtros de Metadados e IA Generativa
# Módulo de ingestão no banco vetorial

# Importa o módulo json para leitura e manipulação de dados em formato JSON
import json

# Importa a classe EmbeddingModel responsável pela geração de embeddings
from src.embeddings import EmbeddingModel

# Importa a classe VectorDB responsável pela persistência vetorial dos dados
from src.vector_db import VectorDB

# Define a função principal de ingestão de dados
def dsa_executa_ingestao():
    
    # Exibe mensagem indicando o início do processo de ingestão
    print("Iniciando ingestão de dados...")
    
    # Abre o arquivo JSON contendo os dados brutos dos produtos
    with open('dados/produtos.json', 'r', encoding='utf-8') as f:
        
        # Carrega o conteúdo do arquivo JSON para uma estrutura Python
        data = json.load(f)
    
    # Inicializa o modelo de embeddings
    embed_model = EmbeddingModel()
    
    # Inicializa o banco de dados vetorial
    db = VectorDB()
    
    # Cria a coleção e os índices necessários no banco vetorial
    db.create_collection()
    
    # Insere os dados no banco vetorial gerando embeddings e armazenando payloads
    db.upsert_data(data, embed_model)
    
    # Exibe mensagem indicando o término do processo de ingestão
    print("Ingestão concluída!")

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    
    # Executa a função de ingestão de dados
    dsa_executa_ingestao()
