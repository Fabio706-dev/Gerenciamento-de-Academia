# Sistema de Academia: Alunos e Planos de Treino (relação 1:N)

IDADE_MINIMA = 16

planos = []
alunos = []


# ---------- Utilitários ----------

def proximo_id(lista):
    return max((item["id"] for item in lista), default=0) + 1


def buscar_por_id(lista, id_procurado):
    for item in lista:
        if item["id"] == id_procurado:
            return item
    return None


def pedir(mensagem, conversor):
    """Repete a pergunta até o conversor aceitar o valor digitado."""
    while True:
        try:
            return conversor(input(mensagem))
        except ValueError as erro:
            print(f" Erro: {erro}")


def converter_numero(texto, tipo, nome):
    try:
        return tipo(texto.strip().replace(",", "."))
    except ValueError:
        raise ValueError(f"O {nome} deve ser um número válido.")


# ---------- Validações ----------

def validar_texto(texto):
    texto = texto.strip()
    if not texto:
        raise ValueError("O texto não pode estar vazio.")
    return texto


def validar_peso(texto):
    peso = converter_numero(texto, float, "Peso")
    if peso <= 0:
        raise ValueError("O peso deve ser maior que zero.")
    return peso


def validar_idade(texto):
    idade = converter_numero(texto, int, "Idade")
    if idade < IDADE_MINIMA:
        raise ValueError(f"A idade mínima é {IDADE_MINIMA} anos.")
    return idade


def validar_duracao(texto):
    duracao = converter_numero(texto, int, "Duração")
    if duracao <= 0:
        raise ValueError("A duração deve ser positiva.")
    return duracao


def validar_valor(texto):
    preco = converter_numero(texto, float, "Valor")
    if preco <= 0:
        raise ValueError("O preço deve ser maior que zero.")
    return preco


def validar_cpf(cpf):
    numeros = "".join(c for c in cpf if c.isdigit())

    if len(numeros) != 11 or numeros == numeros[0] * 11:
        raise ValueError("CPF inválido.")

    for i in (9, 10):
        soma = sum(int(numeros[j]) * (i + 1 - j) for j in range(i))
        digito = (soma * 10 % 11) % 10
        if digito != int(numeros[i]):
            raise ValueError("CPF inválido.")

    if any(aluno["cpf"] == numeros for aluno in alunos):
        raise ValueError("Já existe um aluno com este CPF.")
    return numeros


def validar_plano_id(texto):
    if not texto.strip():
        return None
    plano_id = converter_numero(texto, int, "Id do plano")
    if buscar_por_id(planos, plano_id) is None:
        raise ValueError("Plano de treino não encontrado.")
    return plano_id


def ler_id(texto):
    return converter_numero(texto, int, "Id")


# ---------- Cadastros ----------

def cadastrar_plano():
    plano = {
        "id": proximo_id(planos),
        "nome": pedir("Nome do plano: ", validar_texto),
        "duracao_meses": pedir("Duração (meses): ", validar_duracao),
        "foco": pedir("Foco do plano: ", validar_texto),
        "preco": pedir("Preço (R$): ", validar_valor),
    }
    planos.append(plano)
    print(f"Plano de treino '{plano['nome']}' cadastrado com id {plano['id']}.")


def cadastrar_aluno():
    if not planos:
        print("Aviso: ainda não há planos; o aluno ficará sem plano.")

    aluno = {
        "id": proximo_id(alunos),
        "nome": pedir("Nome do aluno: ", validar_texto),
        "cpf": pedir("CPF: ", validar_cpf),
        "idade": pedir("Idade: ", validar_idade),
        "peso": pedir("Peso (kg): ", validar_peso),
        "plano_id": pedir("Id do plano (Enter para nenhum): ", validar_plano_id),
    }
    alunos.append(aluno)
    print(f"Aluno '{aluno['nome']}' cadastrado com id {aluno['id']}.")


def atribuir_plano():
    if not alunos or not planos:
        print("É preciso ter ao menos um aluno e um plano cadastrados.")
        return

    aluno = buscar_por_id(alunos, pedir("Id do aluno: ", ler_id))
    if aluno is None:
        print("Aluno não encontrado.")
        return

    aluno["plano_id"] = pedir("Id do novo plano: ", validar_plano_id)
    print(f"Plano do aluno '{aluno['nome']}' atualizado.")


# ---------- Listagens ----------

def mostrar_plano(plano):
    print(f"[{plano['id']}] {plano['nome']} | {plano['duracao_meses']} meses "
          f"| {plano['foco']} | R$ {plano['preco']:.2f}")


def mostrar_aluno(aluno):
    plano = buscar_por_id(planos, aluno["plano_id"])
    nome_plano = plano["nome"] if plano else "sem plano"
    print(f"[{aluno['id']}] {aluno['nome']} | CPF {aluno['cpf']} | "
          f"{aluno['idade']} anos | {aluno['peso']} kg | Plano: {nome_plano}")


def listar(lista, mostrar, mensagem_vazia):
    if not lista:
        print(mensagem_vazia)
        return
    for item in lista:
        mostrar(item)


def listar_planos():
    listar(planos, mostrar_plano, "Nenhum plano cadastrado.")


def listar_alunos():
    listar(alunos, mostrar_aluno, "Nenhum aluno cadastrado.")


def listar_alunos_do_plano():
    if not planos:
        print("Nenhum plano cadastrado.")
        return

    plano = buscar_por_id(planos, pedir("Id do plano: ", ler_id))
    if plano is None:
        print("Plano não encontrado.")
        return

    print(f"Alunos do plano {plano['nome']}:")
    do_plano = [a for a in alunos if a["plano_id"] == plano["id"]]
    listar(do_plano, mostrar_aluno, "Nenhum aluno neste plano.")


# ---------- Menu ----------

MENU = """
===== ACADEMIA =====
1 - Cadastrar plano de treino
2 - Cadastrar aluno
3 - Atribuir plano a um aluno
4 - Listar planos
5 - Listar alunos
6 - Listar alunos de um plano
0 - Sair
"""

ACOES = {
    "1": cadastrar_plano,
    "2": cadastrar_aluno,
    "3": atribuir_plano,
    "4": listar_planos,
    "5": listar_alunos,
    "6": listar_alunos_do_plano,
}


def main():
    try:
        while True:
            print(MENU)
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "0":
                break
            elif opcao in ACOES:
                ACOES[opcao]()
            else:
                print("Opção inválida.")
    except (KeyboardInterrupt, EOFError):
        print("\nEntrada interrompida.")
    finally:
        print("Sistema encerrado.")


if __name__ == "__main__":
    main()