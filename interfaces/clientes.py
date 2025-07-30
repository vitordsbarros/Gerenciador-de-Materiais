# clientes.py

import os
from interfaces.utils import limpar_tela, pausar_tela, carregar_dados, salvar_dados, gerar_id_unico, CAMINHO_CLIENTES

def _solicitar_info_pessoal():
    """Função auxiliar para coletar informações pessoais comuns."""
    info = {}
    info['endereco'] = input("Endereço (Rua, Número, Bairro, Cidade, Estado, CEP): ").strip()
    info['telefone'] = input("Telefone (com DDD): ").strip()
    info['email'] = input("E-mail: ").strip()
    return info

def _confirmar_dados(dados):
    """Exibe os dados coletados e pede confirmação ao usuário."""
    limpar_tela()
    print("=" * 50)
    print("        REVISE OS DADOS ANTES DE CADASTRAR         ")
    print("=" * 50)
    for chave, valor in dados.items():
        if isinstance(valor, dict):
            print(f"\n  {chave.replace('_', ' ').title()}:")
            for sub_chave, sub_valor in valor.items():
                print(f"    - {sub_chave.replace('_', ' ').title()}: {sub_valor}")
        else:
            print(f"  {chave.replace('_', ' ').title()}: {valor}")
    print("-" * 50)
    confirmacao = input("Os dados estão corretos? (s/n): ").lower().strip()
    return confirmacao == 's'

def cadastrar_cliente():
    """Função para cadastrar um novo cliente (Pessoa Física ou Jurídica)."""
    limpar_tela()
    print("=" * 50)
    print("         CADASTRO DE NOVO CLIENTE          ")
    print("=" * 50)

    clientes = carregar_dados(CAMINHO_CLIENTES)
    novo_cliente = {}

    # Geração de ID único para o cliente
    novo_cliente['id_cliente'] = gerar_id_unico()

    tipo_cliente = input("Tipo de Cliente (PF para Pessoa Física / PJ para Pessoa Jurídica): ").upper().strip()

    if tipo_cliente not in ['PF', 'PJ']:
        print("Tipo de cliente inválido. Por favor, digite 'PF' ou 'PJ'.")
        pausar_tela()
        return

    novo_cliente['tipo'] = tipo_cliente
    novo_cliente['nome'] = input("Nome/Razão Social: ").strip()

    if tipo_cliente == 'PF':
        novo_cliente['sobrenome'] = input("Sobrenome: ").strip()
        novo_cliente['cpf'] = input("CPF: ").strip()
        # Validação simples de CPF (pode ser aprimorada)
        if not novo_cliente['cpf'].isdigit() or len(novo_cliente['cpf']) != 11:
            print("CPF inválido. Deve conter 11 dígitos numéricos.")
            pausar_tela()
            return
        novo_cliente['informacoes_pessoais'] = _solicitar_info_pessoal()
        novo_cliente['ativo'] = True # PF geralmente começa como ativo
    elif tipo_cliente == 'PJ':
        novo_cliente['cnpj'] = input("CNPJ: ").strip()
        # Validação simples de CNPJ (pode ser aprimorada)
        if not novo_cliente['cnpj'].isdigit() or len(novo_cliente['cnpj']) != 14:
            print("CNPJ inválido. Deve conter 14 dígitos numéricos.")
            pausar_tela()
            return
        novo_cliente['nome_fantasia'] = input("Nome Fantasia: ").strip()
        novo_cliente['informacoes_pessoais'] = _solicitar_info_pessoal() # Usando o mesmo para endereço, tel, email

        novo_cliente['regiao'] = input("Região (Capital/Interior): ").strip().title()
        novo_cliente['rede'] = input("Possui rede? (s/n): ").lower().strip() == 's'
        novo_cliente['inadimplente'] = 'Não'
        if not novo_cliente['rede']:
            novo_cliente['inadimplente'] = 'Sim' # Marcar como inadimplente se não tiver rede
            print("Atenção: Cliente PJ sem rede marcado como 'Inadimplente'.")

        novo_cliente['ativo'] = input("O CNPJ está ativo? (s/n): ").lower().strip() == 's'

    # Confirmação antes de salvar
    if _confirmar_dados(novo_cliente):
        clientes.append(novo_cliente)
        salvar_dados(CAMINHO_CLIENTES, clientes)
        print(f"\nCliente {novo_cliente.get('nome')} cadastrado com sucesso! ID: {novo_cliente['id_cliente']}")
    else:
        print("\nCadastro cancelado. Dados não foram salvos.")

    pausar_tela()

def listar_clientes():
    """Lista todos os clientes cadastrados."""
    limpar_tela()
    print("=" * 50)
    print("         LISTAGEM DE CLIENTES          ")
    print("=" * 50)

    clientes = carregar_dados(CAMINHO_CLIENTES)

    if not clientes:
        print("Nenhum cliente cadastrado ainda.")
    else:
        for i, cliente in enumerate(clientes, 1):
            print(f"\n--- Cliente {i} ---")
            print(f"ID: {cliente.get('id_cliente', 'N/A')}")
            print(f"Tipo: {cliente.get('tipo', 'N/A')}")
            print(f"Nome/Razão Social: {cliente.get('nome', 'N/A')} {cliente.get('sobrenome', '')}")

            if cliente['tipo'] == 'PF':
                print(f"CPF: {cliente.get('cpf', 'N/A')}")
            elif cliente['tipo'] == 'PJ':
                print(f"CNPJ: {cliente.get('cnpj', 'N/A')}")
                print(f"Nome Fantasia: {cliente.get('nome_fantasia', 'N/A')}")
                print(f"Região: {cliente.get('regiao', 'N/A')}")
                print(f"Possui Rede: {'Sim' if cliente.get('rede') else 'Não'}")
                if not cliente.get('rede'):
                    print(f"Status: {cliente.get('inadimplente', 'N/A')}")

            print(f"Ativo: {'Sim' if cliente.get('ativo') else 'Não'}")

            info_p = cliente.get('informacoes_pessoais', {})
            print(f"  Endereço: {info_p.get('endereco', 'N/A')}")
            print(f"  Telefone: {info_p.get('telefone', 'N/A')}")
            print(f"  E-mail: {info_p.get('email', 'N/A')}")
            print("-" * 30)
    pausar_tela()

def buscar_cliente():
    """Busca um cliente pelo nome, CPF ou CNPJ."""
    limpar_tela()
    print("=" * 50)
    print("           BUSCAR CLIENTE            ")
    print("=" * 50)

    clientes = carregar_dados(CAMINHO_CLIENTES)
    termo_busca = input("Digite o nome, CPF ou CNPJ do cliente para buscar: ").strip()

    encontrados = []
    for cli in clientes:
        if termo_busca.lower() in cli.get('nome', '').lower() or \
           (cli.get('sobrenome') and termo_busca.lower() in cli['sobrenome'].lower()) or \
           termo_busca == cli.get('cpf', '') or \
           termo_busca == cli.get('cnpj', ''):
            encontrados.append(cli)

    if not encontrados:
        print(f"Nenhum cliente encontrado com o termo '{termo_busca}'.")
    else:
        print(f"\n--- Clientes encontrados ({len(encontrados)}) ---")
        for i, cliente in enumerate(encontrados, 1):
            print(f"\n--- Cliente {i} ---")
            print(f"ID: {cliente.get('id_cliente', 'N/A')}")
            print(f"Tipo: {cliente.get('tipo', 'N/A')}")
            print(f"Nome/Razão Social: {cliente.get('nome', 'N/A')} {cliente.get('sobrenome', '')}")
            if cliente['tipo'] == 'PF':
                print(f"CPF: {cliente.get('cpf', 'N/A')}")
            elif cliente['tipo'] == 'PJ':
                print(f"CNPJ: {cliente.get('cnpj', 'N/A')}")
                print(f"Nome Fantasia: {cliente.get('nome_fantasia', 'N/A')}")
            print(f"Ativo: {'Sim' if cliente.get('ativo') else 'Não'}")
            print("-" * 30)
    pausar_tela()

def menu_clientes():
    """Menu para gerenciar as operações de clientes."""
    while True:
        limpar_tela()
        print("=" * 50)
        print("        MENU DE GERENCIAMENTO DE CLIENTES        ")
        print("=" * 50)
        print("1. Cadastrar Cliente")
        print("2. Listar Clientes")
        print("3. Buscar Cliente")
        # print("4. Editar Cliente (em desenvolvimento)")
        # print("5. Remover Cliente (em desenvolvimento)")
        print("0. Voltar ao Menu Principal")
        print("-" * 50)

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_cliente()
        elif opcao == '2':
            listar_clientes()
        elif opcao == '3':
            buscar_cliente()
        elif opcao == '0':
            print("Voltando ao Menu Principal...")
            pausar_tela()
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            pausar_tela()

# Para testar o módulo clientes diretamente (opcional)
if __name__ == "__main__":
    menu_clientes()