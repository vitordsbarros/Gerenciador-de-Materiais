# funcionarios.py

from interfaces.utils import limpar_tela, pausar_tela, carregar_dados, salvar_dados, gerar_id_unico, CAMINHO_FUNCIONARIOS

def _solicitar_info_contato():
    """Função auxiliar para coletar informações de contato comuns."""
    info = {}
    info['telefone'] = input("Telefone (com DDD): ").strip()
    info['email'] = input("E-mail: ").strip()
    return info

def cadastrar_funcionario():
    """Função para cadastrar um novo funcionário."""
    limpar_tela()
    print("=" * 50)
    print("         CADASTRO DE NOVO FUNCIONÁRIO         ")
    print("=" * 50)

    funcionarios = carregar_dados(CAMINHO_FUNCIONARIOS)
    novo_funcionario = {}

    novo_funcionario['id_funcionario'] = gerar_id_unico()
    novo_funcionario['nome'] = input("Nome: ").strip()
    novo_funcionario['sobrenome'] = input("Sobrenome: ").strip()
    novo_funcionario['cpf'] = input("CPF: ").strip()
    # Validação simples de CPF (pode ser aprimorada)
    if not novo_funcionario['cpf'].isdigit() or len(novo_funcionario['cpf']) != 11:
        print("CPF inválido. Deve conter 11 dígitos numéricos.")
        pausar_tela()
        return

    novo_funcionario['contato'] = _solicitar_info_contato()

    cargos_validos = ["GERENTE DE OPERACOES", "CHEFE DE TRAFEGO", "CHEFE DE ROTA", "MOTORISTA"]
    while True:
        cargo = input("Cargo (Gerente de Operações, Chefe de Tráfego, Chefe de Rota, Motorista): ").upper().strip()
        if cargo in cargos_validos:
            novo_funcionario['cargo'] = cargo
            break
        else:
            print("Cargo inválido. Por favor, escolha entre as opções fornecidas.")

    # Pergunta sobre a região apenas para os cargos específicos
    if cargo in ["GERENTE DE OPERACOES", "CHEFE DE TRAFEGO", "CHEFE DE ROTA"]:
        while True:
            regiao = input("Responsável por (Capital/Interior): ").strip().title()
            if regiao in ['Capital', 'Interior']:
                novo_funcionario['regiao_responsavel'] = regiao
                break
            else:
                print("Região inválida. Por favor, digite 'Capital' ou 'Interior'.")
    else:
        novo_funcionario['regiao_responsavel'] = "N/A" # Motoristas e outros podem não ter região fixa

    funcionarios.append(novo_funcionario)
    salvar_dados(CAMINHO_FUNCIONARIOS, funcionarios)
    print(f"\nFuncionário '{novo_funcionario['nome']} {novo_funcionario['sobrenome']}' ({novo_funcionario['cargo']}) cadastrado com sucesso! ID: {novo_funcionario['id_funcionario']}")
    pausar_tela()

def listar_funcionarios():
    """Lista todos os funcionários cadastrados."""
    limpar_tela()
    print("=" * 50)
    print("         LISTAGEM DE FUNCIONÁRIOS          ")
    print("=" * 50)

    funcionarios = carregar_dados(CAMINHO_FUNCIONARIOS)

    if not funcionarios:
        print("Nenhum funcionário cadastrado ainda.")
    else:
        for i, func in enumerate(funcionarios, 1):
            print(f"\n--- Funcionário {i} ---")
            print(f"ID: {func.get('id_funcionario', 'N/A')}")
            print(f"Nome Completo: {func.get('nome', 'N/A')} {func.get('sobrenome', 'N/A')}")
            print(f"CPF: {func.get('cpf', 'N/A')}")
            print(f"Cargo: {func.get('cargo', 'N/A').replace('_', ' ').title()}")

            if func.get('regiao_responsavel') != "N/A":
                print(f"Região Responsável: {func.get('regiao_responsavel', 'N/A')}")

            contato_info = func.get('contato', {})
            print(f"  Telefone: {contato_info.get('telefone', 'N/A')}")
            print(f"  E-mail: {contato_info.get('email', 'N/A')}")
            print("-" * 30)
    pausar_tela()

def buscar_funcionario():
    """Busca um funcionário pelo nome ou CPF."""
    limpar_tela()
    print("=" * 50)
    print("           BUSCAR FUNCIONÁRIO            ")
    print("=" * 50)

    funcionarios = carregar_dados(CAMINHO_FUNCIONARIOS)
    termo_busca = input("Digite o nome ou CPF do funcionário para buscar: ").strip()

    encontrados = []
    for func in funcionarios:
        if termo_busca.lower() in func.get('nome', '').lower() or \
           (func.get('sobrenome') and termo_busca.lower() in func['sobrenome'].lower()) or \
           termo_busca == func.get('cpf', ''):
            encontrados.append(func)

    if not encontrados:
        print(f"Nenhum funcionário encontrado com o termo '{termo_busca}'.")
    else:
        print(f"\n--- Funcionários encontrados ({len(encontrados)}) ---")
        for i, func in enumerate(encontrados, 1):
            print(f"\n--- Funcionário {i} ---")
            print(f"ID: {func.get('id_funcionario', 'N/A')}")
            print(f"Nome Completo: {func.get('nome', 'N/A')} {func.get('sobrenome', 'N/A')}")
            print(f"Cargo: {func.get('cargo', 'N/A').replace('_', ' ').title()}")
            if func.get('regiao_responsavel') != "N/A":
                print(f"Região Responsável: {func.get('regiao_responsavel', 'N/A')}")
            print("-" * 30)
    pausar_tela()

def menu_funcionarios():
    """Menu para gerenciar as operações de funcionários."""
    while True:
        limpar_tela()
        print("=" * 50)
        print("        MENU DE GERENCIAMENTO DE FUNCIONÁRIOS        ")
        print("=" * 50)
        print("1. Cadastrar Novo Funcionário")
        print("2. Listar Funcionários")
        print("3. Buscar Funcionário")
        print("0. Voltar ao Menu Principal")
        print("-" * 50)

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_funcionario()
        elif opcao == '2':
            listar_funcionarios()
        elif opcao == '3':
            buscar_funcionario()
        elif opcao == '0':
            print("Voltando ao Menu Principal...")
            pausar_tela()
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            pausar_tela()

# Para testar o módulo funcionários diretamente (opcional)
if __name__ == "__main__":
    menu_funcionarios()