# entregas.py

import random
from datetime import datetime, timedelta
from interfaces.utils import limpar_tela, pausar_tela, carregar_dados, salvar_dados, gerar_id_unico, \
                    CAMINHO_PEDIDOS, CAMINHO_CLIENTES, CAMINHO_ESTOQUE, CAMINHO_FUNCIONARIOS

def registrar_pedido():
    """
    Registra um novo pedido, associando-o a um cliente, selecionando peças do estoque
    e atribuindo a equipe de entrega.
    """
    limpar_tela()
    print("=" * 50)
    print("         REGISTRO DE NOVO PEDIDO         ")
    print("=" * 50)

    clientes = carregar_dados(CAMINHO_CLIENTES)
    estoque = carregar_dados(CAMINHO_ESTOQUE)
    funcionarios = carregar_dados(CAMINHO_FUNCIONARIOS)
    pedidos = carregar_dados(CAMINHO_PEDIDOS)

    if not clientes:
        print("É necessário cadastrar clientes antes de registrar pedidos.")
        pausar_tela()
        return
    if not estoque:
        print("É necessário cadastrar peças no estoque antes de registrar pedidos.")
        pausar_tela()
        return
    if not funcionarios:
        print("É necessário cadastrar funcionários (especialmente motoristas e gerentes) antes de registrar pedidos.")
        pausar_tela()
        return

    # --- 1. Selecionar Cliente ---
    print("\n--- Seleção de Cliente ---")
    cliente_encontrado = None
    while cliente_encontrado is None:
        termo_busca_cliente = input("Digite o ID, Nome, CPF ou CNPJ do cliente para o pedido (ou 'voltar'): ").strip()
        if termo_busca_cliente.lower() == 'voltar':
            return

        for cli in clientes:
            if termo_busca_cliente.lower() in cli.get('id_cliente', '').lower() or \
               termo_busca_cliente.lower() in cli.get('nome', '').lower() or \
               (cli.get('sobrenome') and termo_busca_cliente.lower() in cli['sobrenome'].lower()) or \
               termo_busca_cliente == cli.get('cpf', '') or \
               termo_busca_cliente == cli.get('cnpj', ''):
                cliente_encontrado = cli
                break

        if cliente_encontrado:
            print(f"Cliente selecionado: {cliente_encontrado.get('nome')} (ID: {cliente_encontrado.get('id_cliente')})")
        else:
            print("Cliente não encontrado. Tente novamente.")

    # --- 2. Selecionar Peças do Pedido ---
    print("\n--- Seleção de Peças ---")
    itens_pedido = []
    total_valor_pedido = 0 # Um campo para futuras melhorias de valor

    while True:
        id_peca_busca = input("Digite o ID ou Nome da peça a ser adicionada (ou 'f' para finalizar): ").strip()
        if id_peca_busca.lower() == 'f':
            break

        peca_encontrada = None
        for peca in estoque:
            if id_peca_busca.lower() in peca.get('id_peca', '').lower() or \
               id_peca_busca.lower() in peca.get('nome', '').lower():
                peca_encontrada = peca
                break

        if not peca_encontrada:
            print("Peça não encontrada no estoque.")
            continue

        print(f"Peça: {peca_encontrada['nome']} (Estoque: {peca_encontrada['quantidade']})")
        if peca_encontrada['quantidade'] == 0:
            print("Esta peça está FORA DE ESTOQUE e não pode ser adicionada ao pedido.")
            continue

        while True:
            try:
                qtd_desejada = int(input(f"Quantas unidades de '{peca_encontrada['nome']}' o cliente deseja? "))
                if qtd_desejada <= 0:
                    print("A quantidade deve ser maior que zero.")
                elif qtd_desejada > peca_encontrada['quantidade']:
                    print(f"Não há estoque suficiente. Apenas {peca_encontrada['quantidade']} unidades disponíveis.")
                else:
                    itens_pedido.append({
                        'id_peca': peca_encontrada['id_peca'],
                        'nome_peca': peca_encontrada['nome'],
                        'quantidade': qtd_desejada
                    })
                    # Diminui a quantidade no estoque
                    peca_encontrada['quantidade'] -= qtd_desejada
                    print(f"'{peca_encontrada['nome']}' ({qtd_desejada} unidades) adicionado ao pedido.")
                    break
            except ValueError:
                print("Entrada inválida. Por favor, digite um número inteiro.")

    if not itens_pedido:
        print("Nenhuma peça foi adicionada ao pedido. Pedido cancelado.")
        salvar_dados(CAMINHO_ESTOQUE, estoque) # Garante que o estoque seja salvo mesmo se o pedido for cancelado
        pausar_tela()
        return

    # Salva o estoque atualizado
    salvar_dados(CAMINHO_ESTOQUE, estoque)
    print("\nPeças do pedido registradas e estoque atualizado.")

    # --- 3. Atribuição de Equipe e Região ---
    print("\n--- Atribuição de Equipe de Entrega ---")
    regiao_entrega = None
    while regiao_entrega not in ['Capital', 'Interior']:
        regiao_entrega = input("A entrega será para qual região (Capital/Interior)? ").strip().title()
        if regiao_entrega not in ['Capital', 'Interior']:
            print("Região inválida. Por favor, digite 'Capital' ou 'Interior'.")

    gerentes_operacoes = [f for f in funcionarios if f.get('cargo') == 'GERENTE DE OPERACOES' and f.get('regiao_responsavel') == regiao_entrega]
    chefes_trafego = [f for f in funcionarios if f.get('cargo') == 'CHEFE DE TRAFEGO' and f.get('regiao_responsavel') == regiao_entrega]
    chefes_rota = [f for f in funcionarios if f.get('cargo') == 'CHEFE DE ROTA' and f.get('regiao_responsavel') == regiao_entrega]
    motoristas_disponiveis = [f for f in funcionarios if f.get('cargo') == 'MOTORISTA']

    gerente_selecionado = random.choice(gerentes_operacoes) if gerentes_operacoes else {'nome': 'N/A', 'sobrenome': '', 'id_funcionario': 'N/A'}
    chefe_trafego_selecionado = random.choice(chefes_trafego) if chefes_trafego else {'nome': 'N/A', 'sobrenome': '', 'id_funcionario': 'N/A'}
    chefe_rota_selecionado = random.choice(chefes_rota) if chefes_rota else {'nome': 'N/A', 'sobrenome': '', 'id_funcionario': 'N/A'}
    motorista_selecionado = random.choice(motoristas_disponiveis) if motoristas_disponiveis else {'nome': 'N/A', 'sobrenome': '', 'id_funcionario': 'N/A'}

    print(f"\n--- Equipe Designada para {regiao_entrega} ---")
    print(f"Gerente de Operações: {gerente_selecionado['nome']} {gerente_selecionado['sobrenome']} (ID: {gerente_selecionado['id_funcionario']})")
    print(f"Chefe de Tráfego: {chefe_trafego_selecionado['nome']} {chefe_trafego_selecionado['sobrenome']} (ID: {chefe_trafego_selecionado['id_funcionario']})")
    print(f"Chefe de Rota: {chefe_rota_selecionado['nome']} {chefe_rota_selecionado['sobrenome']} (ID: {chefe_rota_selecionado['id_funcionario']})")
    print(f"Motorista: {motorista_selecionado['nome']} {motorista_selecionado['sobrenome']} (ID: {motorista_selecionado['id_funcionario']})")

    if gerente_selecionado['nome'] == 'N/A' or chefe_trafego_selecionado['nome'] == 'N/A' or \
       chefe_rota_selecionado['nome'] == 'N/A' or motorista_selecionado['nome'] == 'N/A':
        print("\nAtenção: Falta de funcionários específicos para esta região ou função. O pedido será registrado, mas o sistema está incompleto.")
        pausar_tela()

    # --- 4. Gerar Informações do Pedido/Entrega ---
    agora = datetime.now()
    tempo_estimado_entrega = agora + timedelta(days=1, hours=random.randint(4, 12)) # Ex: 1 dia e 4 a 12h

    novo_pedido = {
        'id_pedido': gerar_id_unico(),
        'id_cliente': cliente_encontrado['id_cliente'],
        'nome_cliente': cliente_encontrado['nome'],
        'data_solicitacao': agora.strftime("%Y-%m-%d %H:%M:%S"),
        'itens_pedido': itens_pedido,
        'regiao_entrega': regiao_entrega,
        'equipe_entrega': {
            'gerente_operacoes': gerente_selecionado['id_funcionario'],
            'chefe_trafego': chefe_trafego_selecionado['id_funcionario'],
            'chefe_rota': chefe_rota_selecionado['id_funcionario'],
            'motorista': motorista_selecionado['id_funcionario']
        },
        'tempo_estimado_entrega': tempo_estimado_entrega.strftime("%Y-%m-%d %H:%M:%S"),
        'numero_protocolo': f"PROT-{random.randint(10000, 99999)}",
        'codigo_rastreio': f"RAST-{gerar_id_unico()[:8].upper()}",
        'status_entrega': 'Em Processamento'
    }

    pedidos.append(novo_pedido)
    salvar_dados(CAMINHO_PEDIDOS, pedidos)

    limpar_tela()
    print("=" * 50)
    print("         PAINEL DE PEDIDO E ENTREGA         ")
    print("=" * 50)
    print(f"Data e Hora do Pedido: {novo_pedido['data_solicitacao']}")
    print(f"Cliente: {novo_pedido['nome_cliente']}")
    print(f"Região de Entrega: {novo_pedido['regiao_entrega']}")
    print("\nItens do Pedido:")
    for item in novo_pedido['itens_pedido']:
        print(f"  - {item['nome_peca']} (x{item['quantidade']})")

    print("\nEquipe Designada:")
    print(f"  Gerente de Operações ID: {novo_pedido['equipe_entrega']['gerente_operacoes']}")
    print(f"  Chefe de Tráfego ID: {novo_pedido['equipe_entrega']['chefe_trafego']}")
    print(f"  Chefe de Rota ID: {novo_pedido['equipe_entrega']['chefe_rota']}")
    print(f"  Motorista ID: {novo_pedido['equipe_entrega']['motorista']}")

    print(f"\nTempo Estimado de Entrega: {novo_pedido['tempo_estimado_entrega']}")
    print(f"Número de Protocolo: {novo_pedido['numero_protocolo']}")
    print(f"Código de Rastreio: {novo_pedido['codigo_rastreio']}")
    print(f"Status da Entrega: {novo_pedido['status_entrega']}")

    # Verifica atraso
    if datetime.now() > tempo_estimado_entrega:
        print("\n!!! ATENÇÃO: ESTA ENTREGA ESTÁ ATRASADA !!!")

    pausar_tela()

def listar_pedidos():
    """Lista todos os pedidos registrados."""
    limpar_tela()
    print("=" * 50)
    print("         LISTAGEM DE PEDIDOS         ")
    print("=" * 50)

    pedidos = carregar_dados(CAMINHO_PEDIDOS)

    if not pedidos:
        print("Nenhum pedido registrado ainda.")
    else:
        for i, pedido in enumerate(pedidos, 1):
            status_atraso = ""
            if datetime.now() > datetime.strptime(pedido['tempo_estimado_entrega'], "%Y-%m-%d %H:%M:%S"):
                status_atraso = " (ATRASADO)"

            print(f"\n--- Pedido {i} ---")
            print(f"ID do Pedido: {pedido.get('id_pedido', 'N/A')}")
            print(f"Cliente: {pedido.get('nome_cliente', 'N/A')} (ID: {pedido.get('id_cliente', 'N/A')})")
            print(f"Data Solicitação: {pedido.get('data_solicitacao', 'N/A')}")
            print("Itens:")
            for item in pedido.get('itens_pedido', []):
                print(f"  - {item.get('nome_peca', 'N/A')} (x{item.get('quantidade', 'N/A')})")
            print(f"Região: {pedido.get('regiao_entrega', 'N/A')}")
            print(f"Tempo Estimado: {pedido.get('tempo_estimado_entrega', 'N/A')}{status_atraso}")
            print(f"Protocolo: {pedido.get('numero_protocolo', 'N/A')}")
            print(f"Rastreio: {pedido.get('codigo_rastreio', 'N/A')}")
            print(f"Status: {pedido.get('status_entrega', 'N/A')}")
            print("-" * 30)
    pausar_tela()

def menu_entregas():
    """Menu para gerenciar as operações de pedidos e entregas."""
    while True:
        limpar_tela()
        print("=" * 50)
        print("        MENU DE PEDIDOS E ENTREGAS        ")
        print("=" * 50)
        print("1. Registrar Novo Pedido")
        print("2. Listar Todos os Pedidos")
        # print("3. Atualizar Status de Entrega (em desenvolvimento)")
        # print("4. Cancelar Pedido (em desenvolvimento)")
        print("0. Voltar ao Menu Principal")
        print("-" * 50)

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            registrar_pedido()
        elif opcao == '2':
            listar_pedidos()
        elif opcao == '0':
            print("Voltando ao Menu Principal...")
            pausar_tela()
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            pausar_tela()

# Para testar o módulo entregas diretamente (opcional)
if __name__ == "__main__":
    menu_entregas()