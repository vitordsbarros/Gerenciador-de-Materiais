# utils.py

import os
import json
import uuid # Módulo para gerar IDs únicos universalmente (UUIDs)

def limpar_tela():
    """
    Limpa o console para uma melhor visualização do programa.
    Detecta o sistema operacional para usar o comando correto ('cls' para Windows, 'clear' para Linux/macOS).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar_tela():
    """
    Pausa a execução do programa e aguarda o usuário pressionar Enter para continuar.
    Útil para permitir que o usuário leia mensagens antes que a tela seja limpa ou um novo menu apareça.
    """
    input("\nPressione Enter para continuar...")

def carregar_dados(caminho_arquivo):
    """
    Carrega dados de um arquivo JSON.

    Args:
        caminho_arquivo (str): O caminho completo para o arquivo JSON.

    Returns:
        list or dict: Os dados carregados do arquivo. Retorna uma lista vazia ou um dicionário vazio
                      se o arquivo não existir ou estiver vazio, garantindo que o programa não quebre.
    """
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            # Tenta carregar o JSON. Se o arquivo estiver vazio, retorna um JSON vazio []
            dados = json.load(f)
            # Retorna lista vazia se o JSON está vazio e a expectativa é uma lista
            if not dados and caminho_arquivo.endswith(('.json')):
                return []
            return dados
    except FileNotFoundError:
        # Se o arquivo não existe, retorna uma lista vazia, o que é útil para iniciar um novo banco de dados
        print(f"Arquivo '{caminho_arquivo}' não encontrado. Criando um novo.")
        return []
    except json.JSONDecodeError:
        # Se o arquivo não é um JSON válido (ex: vazio, corrompido), retorna uma lista vazia
        print(f"Erro ao decodificar JSON do arquivo '{caminho_arquivo}'. O arquivo pode estar corrompido ou vazio.")
        return []

def salvar_dados(caminho_arquivo, dados):
    """
    Salva dados em um arquivo JSON.

    Args:
        caminho_arquivo (str): O caminho completo para o arquivo JSON onde os dados serão salvos.
        dados (list or dict): Os dados (lista ou dicionário) a serem salvos no arquivo.
    """
    try:
        # 'w' abre o arquivo para escrita, criando-o se não existir ou sobrescrevendo se existir.
        # indent=4 formata o JSON com 4 espaços para melhor legibilidade.
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Erro de I/O ao salvar dados no arquivo '{caminho_arquivo}': {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao salvar dados: {e}")

def gerar_id_unico():
    """
    Gera um ID único universalmente (UUID) como string.
    Útil para identificar de forma exclusiva clientes, peças, pedidos, etc.
    """
    return str(uuid.uuid4())

# --- Configurações de Caminhos dos Arquivos JSON ---
# É uma boa prática centralizar os caminhos dos arquivos de dados
# para facilitar a manutenção e importação em outros módulos.

# Garante que o diretório 'data' exista
DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
    print(f"Diretório '{DATA_DIR}' criado.")


CAMINHO_CLIENTES = os.path.join(DATA_DIR, 'clientes.json')
CAMINHO_ESTOQUE = os.path.join(DATA_DIR, 'estoque.json')
CAMINHO_FUNCIONARIOS = os.path.join(DATA_DIR, 'funcionarios.json')
CAMINHO_PEDIDOS = os.path.join(DATA_DIR, 'pedidos.json')


# Inicializa os arquivos JSON se não existirem
def inicializar_arquivos_json():
    """
    Verifica se os arquivos JSON existem e os cria com uma lista vazia se não existirem.
    Isso evita erros de FileNotFoundError na primeira execução.
    """
    arquivos = {
        CAMINHO_CLIENTES: [],
        CAMINHO_ESTOQUE: [],
        CAMINHO_FUNCIONARIOS: [],
        CAMINHO_PEDIDOS: []
    }
    for caminho, dados_iniciais in arquivos.items():
        if not os.path.exists(caminho) or os.stat(caminho).st_size == 0:
            print(f"Inicializando arquivo {os.path.basename(caminho)}...")
            salvar_dados(caminho, dados_iniciais)

# Chamada para inicializar os arquivos JSON na primeira execução ou importação
if __name__ == "__main__":
    # Este bloco só será executado se você rodar 'python utils.py' diretamente
    # Para testes ou para garantir a criação inicial dos arquivos
    limpar_tela()
    print("--- Teste de Funções Utilitárias ---")
    inicializar_arquivos_json()
    print(f"Um ID único gerado: {gerar_id_unico()}")
    print("\nFunções utilitárias prontas.")
    pausar_tela()