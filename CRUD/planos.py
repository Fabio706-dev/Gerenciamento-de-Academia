from psycopg2 import Error

import DATABASE
import validacao


def plano_existe(conn, id_plano):
    """Devolve True se existe um plano com esse ID."""
    return bool(DATABASE.consultar(conn, "SELECT id FROM planos_treino WHERE id = %s", (id_plano,)))


def listar_planos(conn):
    planos = DATABASE.consultar(conn, "SELECT id, nome, duracao, foco, preco FROM planos_treino ORDER BY id")
    if not planos:
        print("Nenhum plano cadastrado.")
        return planos
    print(f"\n{'ID':<4}{'Nome':<22}{'Meses':<7}{'Foco':<18}{'Preço':>10}")
    for p in planos:
        print(f"{p[0]:<4}{p[1]:<22}{p[2]:<7}{p[3]:<18}{p[4]:>10.2f}")
    return planos


def cadastrar_plano(conn):
    nome = validacao.ler_texto("Nome do plano: ")
    duracao = validacao.ler_numero("Duração (meses): ", int)
    foco = validacao.ler_texto("Foco (ex.: hipertrofia): ")
    preco = validacao.ler_numero("Preço (R$): ", float)
    DATABASE.executar(conn,
                      "INSERT INTO planos_treino (nome, duracao, foco, preco) VALUES (%s, %s, %s, %s)",
                      (nome, duracao, foco, preco))
    print("Plano cadastrado!")


def atualizar_plano(conn):
    if not listar_planos(conn):
        return
    id_plano = validacao.ler_numero("ID do plano a atualizar: ", int)
    if not plano_existe(conn, id_plano):
        print("Plano não encontrado.")
        return
    nome = validacao.ler_texto("Novo nome: ")
    duracao = validacao.ler_numero("Nova duração (meses): ", int)
    foco = validacao.ler_texto("Novo foco: ")
    preco = validacao.ler_numero("Novo preço (R$): ", float)
    DATABASE.executar(conn,
                      "UPDATE planos_treino SET nome = %s, duracao = %s, foco = %s, preco = %s WHERE id = %s",
                      (nome, duracao, foco, preco, id_plano))
    print("Plano atualizado!")


def excluir_plano(conn):
    if not listar_planos(conn):
        return
    id_plano = validacao.ler_numero("ID do plano a excluir: ", int)
    if not plano_existe(conn, id_plano):
        print("Plano não encontrado.")
        return
    vinculados = DATABASE.consultar(conn, "SELECT id FROM alunos WHERE id_plano = %s", (id_plano,))
    if vinculados:
        print(f"Não é possível excluir: {len(vinculados)} aluno(s) ainda usam este plano.")
        return
    DATABASE.executar(conn, "DELETE FROM planos_treino WHERE id = %s", (id_plano,))
    print("Plano excluído!")


def menu_planos(conn):
    opcoes = {
        "1": ("Cadastrar plano", cadastrar_plano),
        "2": ("Listar planos", listar_planos),
        "3": ("Atualizar plano", atualizar_plano),
        "4": ("Excluir plano", excluir_plano),
    }
    while True:
        print("\n===== PLANOS DE TREINO =====")
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