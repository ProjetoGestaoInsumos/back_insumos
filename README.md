# Back-Insumos

## Descrição dos Diretórios

- **api/**: Contém as rotas da API. Aqui estão as definições das rotas para os recursos e a autenticação.
  - `resources.py`: Rotas para gerenciamento de itens ou outros recursos.
  - `auth.py`: Rotas relacionadas à autenticação de usuários.

- **models/**: Contém os modelos de dados, usando **SQLAlchemy** para mapeamento objeto-relacional (ORM).
  - `item.py`: Define o modelo de dados para os itens.
  - `user.py`: Define o modelo de dados para os usuários.

- **schemas/**: Contém os schemas de validação de entrada e saída, utilizando **Pydantic** para garantir a estrutura correta dos dados.
  - `item_schema.py`: Define o schema para validação de dados de itens.
  - `user_schema.py`: Define o schema para validação de dados de usuários.

- **services/**: Contém a lógica de negócios, incluindo funções CRUD e outras lógicas de aplicação.
  - `item_service.py`: Funções para manipulação dos itens (criar, ler, atualizar, excluir).
  - `user_service.py`: Funções para manipulação de usuários (criar, autenticar, atualizar).

- **database/**: Contém a configuração do banco de dados.
  - `db.py`: Arquivo responsável pela configuração da conexão com o banco de dados e inicialização do SQLAlchemy.

- **config.py**: Arquivo de configuração geral, contendo variáveis de ambiente e outras configurações do projeto.

- **main.py**: Arquivo principal da aplicação **FastAPI**, onde o servidor é iniciado e as rotas são registradas.

- **requirements.txt**: Arquivo que lista as dependências do projeto. Pode ser usado para instalar as dependências com o comando `pip install -r requirements.txt`.

## Requisitos

- **Python 3.7+**
- **FastAPI**: Framework web moderno e rápido para construção de APIs.
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **PostgreSQL**: Banco de dados relacional.
- **Pydantic**: Para validação de dados.