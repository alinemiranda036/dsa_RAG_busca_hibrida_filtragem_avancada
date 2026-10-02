# Projeto 3 – Sistema de Recomendação Semântica com Embeddings, Banco Vetorial, Filtros de Metadados e IA Generativa
# Módulo para testar o banco vetorial

# Imports
import sys
from qdrant_client import QdrantClient

print(f"\nPython Executável: {sys.executable}")

try:
    
    # Tenta instanciar o cliente
    client = QdrantClient(url="http://localhost:6333")
    print("\n✅ Cliente instanciado com sucesso.\n")
    
except Exception as e:
    print(f"\n❌ Erro ao instanciar: {e}")