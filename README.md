# Sistema de Gerenciamento de Fornecedora de Materiais de Construção

Bem-vindo(a) ao Sistema de Gerenciamento desenvolvido para otimizar as operações de uma fornecedora de materiais de construção. Este programa, construído em Python, permite o controle de estoque, cadastro de clientes, gerenciamento de funcionários e o fluxo completo de pedidos e entregas.

---

## 🚀 Funcionalidades Principais

Este sistema abrange as seguintes áreas operacionais:

1.  **Gerenciamento de Clientes:**
    * Cadastro detalhado de Pessoas Físicas (PF) e Jurídicas (PJ).
    * Informações específicas para PJ, como região (Capital/Interior), status de rede e inadimplência.
    * Geração de código de cliente único.
    * Marcação de cliente como ativo/inativo.
    * Listagem e busca de clientes por nome, CPF ou CNPJ.

2.  **Gerenciamento de Estoque de Peças:**
    * Registro de peças com nome, material, ID único e quantidade.
    * Atualização da quantidade de peças.
    * Alerta automático quando a quantidade de uma peça chega a zero ("FORA DE ESTOQUE!").
    * Listagem e busca de peças.

3.  **Gerenciamento de Funcionários:**
    * Cadastro de funcionários com nome, sobrenome, CPF e contato.
    * Definição de cargos: Gerente de Operações, Chefe de Tráfego, Chefe de Rota e Motorista.
    * Atribuição de região de responsabilidade (Capital/Interior) para Gerentes e Chefes.
    * Listagem e busca de funcionários.

4.  **Gerenciamento de Pedidos e Entregas:**
    * Seleção interativa de cliente e peças do estoque para cada pedido.
    * Verificação de disponibilidade de estoque em tempo real.
    * Atualização automática do estoque após a criação de um pedido.
    * Atribuição automática da equipe de entrega com base na região (Gerente de Operações, Chefe de Tráfego, Chefe de Rota da região específica e um Motorista aleatório).
    * Geração de painel de "Nota Fiscal" com:
        * Data e hora da solicitação.
        * Tempo estimado de entrega.
        * Número de protocolo da entrega.
        * Código de rastreio único.
    * Indicação clara de "ENTREGA ATRASADA" se o tempo estimado for excedido.
    * Listagem de todos os pedidos registrados.

---

## 📁 Estrutura do Projeto

O projeto está organizado em módulos Python para facilitar a manutenção e a expansão. Os dados são persistidos em arquivos JSON, localizados em um diretório `data/`.

```
fornecedora_materiais/
├── gerenciador.py               # Módulo principal com o menu de navegação e interface.
├── clientes.py                  # Módulo para todas as operações de clientes.
├── estoque.py                   # Módulo para todas as operações de estoque de peças.
├── funcionarios.py              # Módulo para todas as operações de gerenciamento de funcionários.
├── entregas.py                  # Módulo para o fluxo de registro e gerenciamento de pedidos e entregas.
├── utils.py                     # Módulo de funções utilitárias (limpeza de tela, JSON, geração de IDs).
├── data/                        # Diretório para armazenamento dos dados em JSON.
│   ├── clientes.json            # Armazena os dados dos clientes.
│   ├── estoque.json             # Armazena os dados das peças em estoque.
│   ├── funcionarios.json        # Armazena os dados dos funcionários.
│   └── pedidos.json             # Armazena os dados dos pedidos e entregas.
└── README.md                    # Este arquivo de documentação.
```

---

## 🛠️ Como Usar

### Pré-requisitos

Certifique-se de ter o **Python 3** instalado em seu sistema. Meu **Notebook Lenovo IdeaPad 1 15IAU7 i5 12th Gen**, com 8GB de RAM, já é adequado para isso!

### Instalação

1.  **Clone ou baixe o repositório:**
    ```bash
    git clone [LINK_DO_SEU_REPOSITORIO]
    # Ou baixe o arquivo .zip e descompacte
    ```
    *Nota: Se você não está usando Git, simplesmente crie a estrutura de pastas e arquivos como descrito acima e cole os códigos nos arquivos correspondentes.*

2.  **Navegue até o diretório do projeto:**
    ```bash
    cd fornecedora_materiais
    ```

### Executando o Programa

Para iniciar o sistema, execute o arquivo principal `gerenciador.py` no terminal:

```bash
python gerenciador.py
```
O programa irá exibir o menu principal e você poderá navegar pelas diferentes opções (Clientes, Estoque, Funcionários, Pedidos e Entregas).

---

## 👨‍💻 Desenvolvimento

### Tecnologias Utilizadas

* **Python 3.x:** Linguagem de programação principal.
* **JSON:** Formato para armazenamento de dados simples.

### Próximos Passos e Melhorias (Ideias Futuras)

* **Edição e Exclusão:** Implementar funcionalidades para editar e remover registros em todos os módulos (clientes, peças, funcionários, pedidos).
* **Relatórios:** Gerar relatórios de vendas, estoque, performance de entregas, etc.
* **Validações Robustas:** Aprimorar as validações de CPF, CNPJ, e-mail, telefone.
* **Interface Gráfica (GUI):** Migrar de uma interface de terminal para uma GUI (ex: Tkinter, PyQt, Kivy) para uma experiência de usuário mais rica.
* **Banco de Dados:** Substituir arquivos JSON por um banco de dados (SQLite, PostgreSQL) para maior escalabilidade e segurança dos dados.
* **Login de Usuários:** Adicionar um sistema de autenticação e controle de acesso para funcionários.
* **Histórico de Preços:** Registrar o preço de compra/venda das peças.
* **Notificações:** Implementar notificações para entregas atrasadas ou baixo estoque.

---

## 🤝 Contribuição

Contribuições são bem-vindas! Se você tiver sugestões ou quiser melhorar o código, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## 💰 Apoie meu trabalho:
[![Patreon](https://img.shields.io/badge/Patreon-F96854?style=for-the-badge&logo=patreon&logoColor=white)](https://patreon.com/vitordsbarros)
