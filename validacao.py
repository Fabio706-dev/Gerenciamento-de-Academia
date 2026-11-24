IDADE_MINIMA = 16

def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print("  Campo obrigatório.")


def ler_numero(mensagem, tipo):
    """Lê um número (int ou float) e repete até ser válido."""
    while True:
        try:
            return tipo(input(mensagem).replace(",", "."))
        except ValueError:
            print("  Digite um número válido.")


def ler_idade():
    while True:
        idade = ler_numero("Idade: ", int)
        if idade >= IDADE_MINIMA:
            return idade
        print(f"  A idade mínima é {IDADE_MINIMA} anos.")


def ler_peso():
    while True:
        peso = ler_numero("Peso (kg): ", float)
        if peso > 0:
            return peso
        print("  O peso deve ser maior que zero.")


def cpf_valido(cpf):
    """11 dígitos, não todos iguais, e dígitos verificadores corretos."""
    if len(cpf) != 11 or not cpf.isdigit() or cpf == cpf[0] * 11:
        return False
    for tamanho in (9, 10):
        soma = sum(int(cpf[i]) * (tamanho + 1 - i) for i in range(tamanho))
        if (soma * 10 % 11) % 10 != int(cpf[tamanho]):
            return False
    return True


def ler_cpf():
    while True:
        cpf = "".join(c for c in input("CPF: ") if c.isdigit())
        if cpf_valido(cpf):
            return cpf
        print("  CPF inválido.")