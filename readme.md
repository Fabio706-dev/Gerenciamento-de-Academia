-olá esse é um softwere de academia que tem como base o uso do CRUD em seu sistema-

(gerenciamento de academia)
Sistema em Python para gerenciar alunos e planos de treino de uma academia, com operações completas de CRUD (Create, Read, Update, Delete) sobre um banco de dados relacional.
Projeto CRUD desenvolvido de forma colaborativa, integrando lógica de programação e banco de dados.

-equipe-

  Nome do Líder	        Fábio gomes de lima junior
  Nome do Integrante 	Carlos Henrique Figueiredo da Cruz
  Nome do Integrante 	Gabriel Bezerra Tenório
  Nome do Integrante    Luiz Bernardino Ferreira Neto


Problema:
Academias costumam controlar alunos e planos de treino em planilhas ou anotações soltas, o que gera dados duplicados, inconsistentes e difíceis de consultar.

-Visão geral-
O sistema é um programa de terminal em Python que cadastra, consulta, atualiza e exclui alunos e planos de treino de uma academia, gravando tudo em um banco PostgreSQL chamado trabalho.
• Planos de Treino: nome, duração (em meses), foco e preço.
• Alunos: nome, CPF, idade, peso e o plano contratado.
• Relacionamento 1:N: um plano pode ter vários alunos, e cada aluno pertence a um único plano. A tabela alunos guarda a chave estrangeira id_plano.
• Operações: as quatro do CRUD (criar, listar e buscar, atualizar, excluir) para as duas entidades, acessadas por menus numerados no terminal.


-Tecnologias e requisitos-

     Item    /  Para que serve

 Python 3     /  Linguagem do sistema
 ostgreSQL    /  Banco de dados relacional (banco trabalho, porta 5432)
 psycopg2     /  Driver que conecta o Python ao PostgreSQL
 python-dotenv / Lê a senha do banco no arquivo .env
 Git e GitHub  / Controle de versão, exigido pelo enunciado do projeto

-Estrutura de arquivos-
O código está dividido em cinco arquivos na mesma pasta. Cada um tem uma responsabilidade.
• main.py: ponto de entrada. Abre a conexão, mostra o menu principal e fecha a conexão ao sair. Usa DATABASE, planos e alunos.
• DATABASE.py: conexão com o PostgreSQL e execução dos comandos SQL. Usa psycopg2 e dotenv.
• validacao.py: leitura e validação do que o usuário digita. Não usa outros arquivos do projeto.
• planos.py: CRUD de planos de treino e menu_planos. Usa DATABASE e validacao.
• alunos.py: CRUD de alunos e menu_alunos. Usa DATABASE, validacao e planos.
Os menus recebem a conexão (conn) como parâmetro, e as funções de CRUD a repassam para DATABASE.executar e DATABASE.consultar. Assim a conexão é aberta uma única vez, em main().


-Banco de dados-
São duas tabelas ligadas por chave estrangeira: alunos.id_plano aponta para planos_treino.id.
Tabela planos_treino
• id (SERIAL): chave primária, gerada automaticamente.
• nome (VARCHAR(100)): obrigatório.
• duracao (INTEGER): obrigatório, maior que 0.
• foco (VARCHAR(100)): obrigatório.
• preco (NUMERIC(10,2)): obrigatório, maior ou igual a 0.
Tabela alunos
• id (SERIAL): chave primária, gerada automaticamente.
• nome (VARCHAR(100)): obrigatório.
• cpf (CHAR(11)): obrigatório, único, só os 11 dígitos.
• idade (INTEGER): obrigatório, maior ou igual a 12.
• peso (NUMERIC(5,2)): obrigatório, maior que 0.
• id_plano (INTEGER): chave estrangeira para planos_treino(id).

-Configuração e execução-
 Instale Python 3 e PostgreSQL.
 Instale as bibliotecas: pip install psycopg2-binaryCrie o banco no psql o python-dotenv.p install psycopg2-binary python-dotenv.
 no pgAdmin: CREATE DATABASE trabalho;.
 Conecte-se ao banco trabalho e rode uma vez o script de criação das tabelas (seção Banco de dados).
 Na mesma pasta dos arquivos, crie um arquivo .env com a senha do usuário postgres: password=sua_senha.
 Execute o sistema com python main.py.

Os dados de conexão ficam na função conecta() do DATABASE.py:
host localhost, banco trabalho, usuário postgres e porta 5432. A senha não fica no código: ela vem do arquivo .env, pela chave password.
Se o PostgreSQL usar outro usuário, porta ou nome de banco, altere esses valores na função. Não envie o .env para o GitHub: inclua .env no .gitignore.


-Referência dos módulos e funções-
DATABASE.py
• conecta() abre a conexão com o PostgreSQL, avisa se deu certo ou erro e devolve a conexão, ou None se falhar.
• encerra_conexao(conn) fecha a conexão, se ela existir.
• executar(conn, sql, params=()) roda INSERT, UPDATE, DELETE ou CREATE e salva (commit). Em caso de erro, faz rollback e relança a exceção.
• consultar(conn, sql, params=()) roda um SELECT e devolve uma lista de linhas, cada uma uma tupla.
validacao.py (constante IDADE_MINIMA = 16)
• ler_texto(mensagem) pede um texto e repete se vier vazio. Devolve o texto sem espaços nas pontas.
• ler_numero(mensagem, tipo) pede um número (int ou float), aceita vírgula decimal e repete se for inválido. Devolve o número do tipo pedido.
• ler_idade() pede a idade e exige o mínimo de IDADE_MINIMA. Devolve int.
• ler_peso() pede o peso e exige valor maior que zero. Devolve float.
• cpf_valido(cpf) confere 11 dígitos, dígitos não todos iguais e os dois dígitos verificadores. Devolve True ou False.
• ler_cpf() pede o CPF, tira pontos e traço e repete até ser válido. Devolve o CPF com 11 dígitos (texto).
planos.py
• listar_planos(conn) mostra a tabela de planos ou avisa que não há nenhum. Devolve a lista de planos.
• cadastrar_plano(conn) pede nome, duração, foco e preço e insere o plano.
• atualizar_plano(conn) lista os planos, pede o ID e os novos dados e atualiza.
• excluir_plano(conn) pede o ID e exclui, a menos que haja alunos usando o plano.
• menu_planos(conn) abre o menu dos planos e repete até o usuário escolher 0 (voltar).
alunos.py
• listar_alunos(conn) mostra os alunos com o nome do plano (JOIN) ou avisa que não há nenhum. Devolve a lista de alunos.
• buscar_aluno_por_cpf(conn) pede o CPF e mostra o aluno encontrado.
• escolher_plano(conn) lista os planos e pede o ID de um plano que exista. Devolve o ID, ou None se não houver planos.
• cadastrar_aluno(conn) exige ao menos um plano, pede os dados, recusa CPF repetido e insere o aluno.
• atualizar_aluno(conn) pede o ID, nome, idade, peso e plano e atualiza (o CPF não muda).
• excluir_aluno(conn) pede o ID e exclui o aluno.
• menu_alunos(conn) abre o menu dos alunos e repete até o usuário escolher 0 (voltar).
main.py
main() conecta, mostra o menu principal (planos, alunos, sair) e garante o fechamento da conexão no finally.


-Validações e integridade-
As regras existem em duas camadas: o Python avisa o usuário e pede de novo; o banco recusa o dado se algo escapar.
• Texto não pode ficar vazio: ler_texto no código e NOT NULL no banco.
• Número precisa ser válido (aceita vírgula): ler_numero no código e o tipo da coluna no banco.
• Idade mínima: ler_idade (16 anos) no código e CHECK (idade >= 16) no banco.
• Peso maior que zero: ler_peso no código e CHECK (peso > 0) no banco.
• CPF válido (11 dígitos, não todos iguais, dígitos verificadores corretos): cpf_valido e ler_cpf no código e CHAR(11) no banco.
• CPF não pode repetir: consulta em cadastrar_aluno no código e UNIQUE no banco.
• O plano do aluno precisa existir: escolher_plano no código e chave estrangeira no banco.
• Plano com alunos não pode ser excluído: verificação em excluir_plano no código e chave estrangeira no banco.
• Duração e preço do plano: ler_numero só confere se é número; o banco aplica CHECK (duracao > 0) e CHECK (preco >= 0).

A validação do CPF refaz o cálculo dos dois últimos dígitos a partir dos nove primeiros. Ela garante que o número é matematicamente válido, mas não consulta a Receita Federal para saber se a pessoa existe.
Duração ou preço inválidos (por exemplo, duração negativa) passam pelo Python e são barrados pelo banco. O menu captura esse erro e mostra "Erro no banco de dados".