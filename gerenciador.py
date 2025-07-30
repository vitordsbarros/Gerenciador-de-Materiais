# gerenciador.py

from interfaces.utils import limpar_tela, pausar_tela, inicializar_arquivos_json
from interfaces.clientes import menu_clientes
from interfaces.estoque import menu_estoque
from interfaces.funcionarios import menu_funcionarios
from interfaces.entregas import menu_entregas

def exibir_cabecalho():
    """Exibe o cabeçalho do programa."""
    limpar_tela()
    print("=" * 50)
    print("     SISTEMA DE GERENCIAMENTO DE FORNECEDORA")
    print("      (Materiais de Construção - Natal/RN)")
    print("=" * 50)
    print("\nBem-vindo(a) ao seu sistema de gestão!\n")

def menu_principal():
    """Exibe o menu principal e gerencia as opções."""
    while True:
        exibir_cabecalho()
        print("1. Gerenciar Clientes")
        print("2. Gerenciar Estoque de Peças")
        print("3. Gerenciar Funcionários")
        print("4. Gerenciar Pedidos e Entregas")
        print("0. Sair do Programa")
        print("-" * 50)

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\nRedirecionando para Gerenciar Clientes...")
            menu_clientes()
        elif opcao == '2':
            print("\nRedirecionando para Gerenciar Estoque de Peças...")
            menu_estoque()
        elif opcao == '3':
            print("\nRedirecionando para Gerenciar Funcionários...")
            menu_funcionarios()
        elif opcao == '4':
            print("\nRedirecionando para Gerenciar Pedidos e Entregas...")
            menu_entregas()
        elif opcao == '0':
            print("\nSaindo do programa. Obrigado por usar nosso sistema!")
            pausar_tela() # Pequena pausa antes de sair
            limpar_tela()
            break
        else:
            print("\nOpção inválida. Por favor, escolha uma opção válida do menu.")
            pausar_tela()

# Ponto de entrada do programa
if __name__ == "__main__":
    inicializar_arquivos_json() # Garante que os arquivos JSON existam antes de tudo
    menu_principal()