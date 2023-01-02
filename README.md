Gerador de PDF e PPTX da M Souza


- Linguagem: Python 3.8.14
- Framework: Flask
- Banco de Dados: MySQL
- Versão: 1.0
- Desenvolvedor: Caléb Rangel Porto - github.com/calebporto



Aplicação criada para gerar arquivos PDF e PPTX para download e visualização via link.


Painel Administrativo:

Novo Catálogo - Criar novo catálogo em PDF e PPTX, a partir de um documento .xlsx, que deve conter
obrigatoriamente as colunas 'foto' e 'endereço', aceitando também esses termos em espanhol e em inglês
(fotografía, imagen, picture e image). As imagens são baixadas através do link fornecido na planilha.


Lista de Catálogos - Visualiza os catálogos gerados, com as opções:
- Visualizar: Dá acesso a um link aberto, podendo ser compartilhado com o cliente.
- Baixar PDF: Faz o download do PDF gerado, em ambiente fechado (somente usuário autenticado.)
- Baixar PPTX: Faz o download do PPTX gerado, em ambiente fechado (somente usuário autenticado.)
- Excluir: Remove a planilha do banco de dados, e seus respectivos arquivos PDF e PPTX.

Equipe - Acessível somente para o administrador da plataforma, podendo adicionar colaborador, alterar senha e excluir.


Tecnologias utilizadas:

- Reportlab: Geração de PDFs
- Python-pptx: Geração de PPTX
- Passlib e Bcrypt: hash de senhas
- Flask-Login: Autenticação de usuário e gerenciamento de sessões (via cookie)
- SQLAlchemy: ORM responsável pela comunicação com o banco de dados e sanitização de inputs
- Pandas: Leitura das planilhas .xlsx