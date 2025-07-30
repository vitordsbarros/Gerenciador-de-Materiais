# estoque.py

from interfaces.utils import limpar_tela, pausar_tela, carregar_dados, salvar_dados, gerar_id_unico, CAMINHO_ESTOQUE

def cadastrar_peca():
    """Função para cadastrar uma nova peça no estoque."""
    limpar_tela()
    print("=" * 50)
    print("         CADASTRO DE NOVA PEÇA         ")
    print("=" * 50)

    estoque = carregar_dados(CAMINHO_ESTOQUE)
    nova_peca = {}

    nova_peca['id_peca'] = gerar_id_unico()
    nova_peca['nome'] = input("Nome da Peça (ex: Parafuso Philips, Bloco Cerâmico): ").strip()
    nova_peca['material'] = input("Material da Peça (ex: Aço, Cimento, PVC): ").strip()

    while True:
        try:
            quantidade = int(input("Quantidade inicial em estoque: "))
            if quantidade < 0:
                print("A quantidade não pode ser negativa. Digite um valor válido.")
            else:
                nova_peca['quantidade'] = quantidade
                break
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro para a quantidade.")

    estoque.append(nova_peca)
    salvar_dados(CAMINHO_ESTOQUE, estoque)
    print(f"\nPeça '{nova_peca['nome']}' (ID: {nova_peca['id_peca']}) cadastrada com sucesso!")
    pausar_tela()

def listar_pecas():
    """Lista todas as peças cadastradas no estoque."""
    limpar_tela()
    print("=" * 50)
    print("         LISTAGEM DE PEÇAS NO ESTOQUE        ")
    print("=" * 50)

    estoque = carregar_dados(CAMINHO_ESTOQUE)

    if not estoque:
        print("Nenhuma peça cadastrada no estoque ainda.")
    else:
        for i, peca in enumerate(estoque, 1):
            status = "Em Estoque"
            if peca['quantidade'] == 0:
                status = "FORA DE ESTOQUE!"
            elif peca['quantidade'] < 10: # Exemplo de alerta para baixo estoque
                status = f"Baixo Estoque ({peca['quantidade']})"

            print(f"\n--- Peça {i} ---")
            print(f"ID: {peca.get('id_peca', 'N/A')}")
            print(f"Nome: {peca.get('nome', 'N/A')}")
            print(f"Material: {peca.get('material', 'N/A')}")
            print(f"Quantidade: {peca.get('quantidade', 'N/A')}")
            print(f"Status: {status}")
            print("-" * 30)
    pausar_tela()

def atualizar_quantidade_peca():
    """Atualiza a quantidade de uma peça existente no estoque."""
    limpar_tela()
    print("=" * 50)
    print("         ATUALIZAR QUANTIDADE DE PEÇA         ")
    print("=" * 50)

    estoque = carregar_dados(CAMINHO_ESTOQUE)
    if not estoque:
        print("Nenhuma peça cadastrada para atualizar.")
        pausar_tela()
        return

    id_busca = input("Digite o ID da peça que deseja atualizar a quantidade: ").strip()

    peca_encontrada = None
    for peca in estoque:
        if peca.get('id_peca') == id_busca:
            peca_encontrada = peca
            break

    if not peca_encontrada:
        print(f"Peça com ID '{id_busca}' não encontrada no estoque.")
    else:
        print(f"\nPeça encontrada: {peca_encontrada['nome']} (Material: {peca_encontrada['material']})")
        print(f"Quantidade atual: {peca_encontrada['quantidade']}")

        while True:
            try:
                nova_quantidade = int(input("Digite a nova quantidade total em estoque: "))
                if nova_quantidade < 0:
                    print("A quantidade não pode ser negativa. Digite um valor válido.")
                else:
                    peca_encontrada['quantidade'] = nova_quantidade
                    break
            except ValueError:
                print("Entrada inválida. Por favor, digite um número inteiro.")

        salvar_dados(CAMINHO_ESTOQUE, estoque)
        print(f"\nQuantidade da peça '{peca_encontrada['nome']}' atualizada para {peca_encontrada['quantidade']}.")

    pausar_tela()

def buscar_peca():
    """Busca uma peça pelo nome ou ID."""
    limpar_tela()
    print("=" * 50)
    print("             BUSCAR PEÇA             ")
    print("=" * 50)

    estoque = carregar_dados(CAMINHO_ESTOQUE)
    termo_busca = input("Digite o nome ou ID da peça para buscar: ").strip()

    encontradas = []
    for peca in estoque:
        if termo_busca.lower() in peca.get('nome', '').lower() or \
           termo_busca.lower() == peca.get('id_peca', '').lower():
            encontradas.append(peca)

    if not encontradas:
        print(f"Nenhuma peça encontrada com o termo '{termo_busca}'.")
    else:
        print(f"\n--- Peças encontradas ({len(encontradas)}) ---")
        for i, peca in enumerate(encontradas, 1):
            status = "Em Estoque"
            if peca['quantidade'] == 0:
                status = "FORA DE ESTOQUE!"
            print(f"\n--- Peça {i} ---")
            print(f"ID: {peca.get('id_peca', 'N/A')}")
            print(f"Nome: {peca.get('nome', 'N/A')}")
            print(f"Material: {peca.get('material', 'N/A')}")
            print(f"Quantidade: {peca.get('quantidade', 'N/A')}")
            print(f"Status: {status}")
            print("-" * 30)
    pausar_tela()

def menu_estoque():
    """Menu para gerenciar as operações de estoque."""
    while True:
        limpar_tela()
        print("=" * 50)
        print("        MENU DE GERENCIAMENTO DE ESTOQUE        ")
        print("=" * 50)
        print("1. Cadastrar Nova Peça")
        print("2. Listar Peças no Estoque")
        print("3. Atualizar Quantidade de Peça")
        print("4. Buscar Peça")
        print("0. Voltar ao Menu Principal")
        print("-" * 50)

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_peca()
        elif opcao == '2':
            listar_pecas()
        elif opcao == '3':
            atualizar_quantidade_peca()
        elif opcao == '4':
            buscar_peca()
        elif opcao == '0':
            print("Voltando ao Menu Principal...")
            pausar_tela()
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            pausar_tela()

# Para testar o módulo estoque diretamente (opcional)
if __name__ == "__main__":
    menu_estoque()