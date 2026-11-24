from psycopg2 import Error

import DATABASE as db
import validacao
import planos


def aluno_existe(conn, id_aluno):
    """Devolve True se existe um aluno com esse ID."""
    return bool(db.consultar(conn, "SELECT id FROM alunos WHERE id = %s", (id_aluno,)))


def listar_alunos(conn):
    alunos = db.consultar(conn, """
        SELECT a.id, a.nome, a.cpf, a.idade, a.peso, p.nome
        FROM alunos a JOIN planos_treino p ON p.id = a.id_plano
        ORDER BY a.id
    """)
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return alunos
    print(f"\n{'ID':<4}{'Nome':<22}{'CPF':<14}{'Idade':<7}{'Peso':<8}{'Plano'}")
    for a in alunos:
        print(f"{a[0]:<4}{a[1]:<22}{a[2]:<14}{a[3]:<7}{float(a[4]):<8.1f}{a[5]}")
    return alunos


def buscar_aluno_por_cpf(conn):
    cpf = validacao.ler_cpf()
    alunos = db.consultar(conn, """
        SELECT a.id, a.nome, a.cpf, a.idade, a.peso, p.nome
        FROM alunos a JOIN planos_treino p ON p.id = a.id_plano
        WHERE a.cpf = %s
    """, (cpf,))
    if not alunos:
        print("Aluno não encontrado.")
        return
    a = alunos[0]
    print(f"ID {a[0]} | {a[1]} | CPF {a[2]} | {a[3]} anos | {float(a[4]):.1f} kg | Plano: {a[5]}")


def escolher_plano(conn):
    """Mostra os planos e pede o ID de um plano que exista."""
    if not planos.listar_planos(conn):
        return None
    while True:
        id_plano = validacao.ler_numero("ID do plano do aluno: ", int)
        if planos.plano_existe(conn, id_plano):
            return id_plano
        print("  Plano não encontrado.")


def cadastrar_aluno(conn):
    if not db.consultar(conn, "SELECT id FROM planos_treino"):
        print("Cadastre um plano de treino antes de cadastrar alunos.")
        return
    nome = validacao.ler_texto("Nome: ")
    cpf = validacao.ler_cpf()
    if db.consultar(conn, "SELECT id FROM alunos WHERE cpf = %s", (cpf,)):
        print("Já existe um aluno com esse CPF.")
        return
    idade = validacao.ler_idade()
    peso = validacao.ler_peso()
    id_plano = escolher_plano(conn)
    db.executar(conn,
                "INSERT INTO alunos (nome, cpf, idade, peso, id_plano) VALUES (%s, %s, %s, %s, %s)",
                (nome, cpf, idade, peso, id_plano))
    print("Aluno cadastrado!")


def atualizar_aluno(conn):
    if not listar_alunos(conn):
        return
    id_aluno = validacao.ler_numero("ID do aluno a atualizar: ", int)
    if not aluno_existe(conn, id_aluno):
        print("Aluno não encontrado.")
        return
    nome = validacao.ler_texto("Novo nome: ")
    idade = validacao.ler_idade()
    peso = validacao.ler_peso()
    id_plano = escolher_plano(conn)
    db.executar(conn,
                "UPDATE alunos SET nome = %s, idade = %s, peso = %s, id_plano = %s WHERE id = %s",
                (nome, idade, peso, id_plano, id_aluno))
    print("Aluno atualizado!")


def excluir_aluno(conn):
    if not listar_alunos(conn):
        return
    id_aluno = validacao.ler_numero("ID do aluno a excluir: ", int)
    if not aluno_existe(conn, id_aluno):
        print("Aluno não encontrado.")
        return
    db.executar(conn, "DELETE FROM alunos WHERE id = %s", (id_aluno,))
    print("Aluno excluído!")


def menu_alunos(conn):
    opcoes = {
        "1": ("Cadastrar aluno", cadastrar_aluno),
        "2": ("Listar alunos", listar_alunos),
        "3": ("Buscar aluno por CPF", buscar_aluno_por_cpf),
        "4": ("Atualizar aluno", atualizar_aluno),
        "5": ("Excluir aluno", excluir_aluno),
    }
    while True:
        print("\n===== ALUNOS =====")
        for numero, (texto, _) in opcoes.items():
            print(f"{numero} - {texto}")
        print("0 - Voltar")
        escolha = input("Escolha: ").strip()

        if escolha == "0":
            break
        if escolha not in opcoes:
            print("Opção inválida.")
            continue
        try:
            opcoes[escolha][1](conn)
        except Error as erro:
            print(f"Erro no banco de dados: {erro}")