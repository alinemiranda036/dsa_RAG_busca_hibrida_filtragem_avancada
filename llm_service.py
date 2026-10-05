# Projeto 3 – Sistema de Recomendação Semântica com Embeddings, Banco Vetorial, Filtros de Metadados e IA Generativa
# Módulo para o LLM

# Importa o módulo os para acesso a variáveis de ambiente
import os

# Importa o cliente Groq para interação com o modelo de linguagem
from groq import Groq

# Importa a função para carregar variáveis de ambiente a partir do arquivo .env
from dotenv import load_dotenv

# Carrega as variáveis de ambiente definidas no arquivo .env
load_dotenv()

# Define a classe LLMService, responsável por encapsular o acesso ao modelo de linguagem
class LLMService:
    
    # Método construtor da classe
    def __init__(self):
        
        # Inicializa o cliente Groq utilizando a chave de API armazenada nas variáveis de ambiente
        self.client = Groq(api_key = os.getenv("GROQ_API_KEY"))

    # Método responsável por gerar recomendações com base na consulta do usuário e no contexto recuperado
    def generate_recommendation(self, user_query, context_products):
        
        # Constrói o texto de contexto a partir dos produtos retornados pelo banco vetorial
        context_text = "\n".join([
            
            # Formata cada produto com nome, marca, preço e descrição
            f"- {prod['name']} (Marca: {prod['brand']}, Preço: R${prod['price']}): {prod['description']}"
            
            # Itera sobre a lista de produtos de contexto
            for prod in context_products
        ])

        # Define o prompt que será enviado ao modelo de linguagem
        prompt = f"""
        Você é um assistente de vendas especialista em tecnologia.
        
        PERGUNTA DO CLIENTE: "{user_query}"
        
        PRODUTOS DISPONÍVEIS (Recuperados do estoque):
        {context_text}
        
        INSTRUÇÃO: Com base APENAS nos produtos acima, recomende a melhor opção para o cliente. 
        Explique por que o produto atende à necessidade dele. Seja persuasivo, mas honesto.
        Se nenhum produto parecer adequado, diga isso educadamente.
        """

        # Realiza a chamada ao modelo de linguagem para gerar a resposta
        chat_completion = self.client.chat.completions.create(
            
            # Define a mensagem de entrada com o prompt construído
            messages = [{"role": "user", "content": prompt}],
            
            # Especifica o modelo de linguagem a ser utilizado
            # model = "llama-3.3-70b-versatile",
            model = "openai/gpt-oss-120b",
            
            # Define o grau de criatividade da resposta (de 0 a 2)
            temperature = 0.5,
        )

        # Retorna apenas o conteúdo textual da resposta gerada pelo modelo
        return chat_completion.choices[0].message.content




