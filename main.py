import DATABASE
import planos
import alunos
import validacao

def main():
    conn = DATABASE.conecta()
    if conn is None:
        print("Não foi possível iniciar o sistema sem conexão com o banco.")
        return

    try:
        while True:
            print("\n===== GERENCIAMENTO DE ACADEMIA =====")
            print("1 - Gerenciar Planos de Treino")
            print("2 - Gerenciar Alunos")
            print("0 - Sair")
            escolha = input("Escolha: ").strip()

            if escolha == "1":
                planos.menu_planos(conn)
            elif escolha == "2":
                alunos.menu_alunos(conn)
            elif escolha == "0":
                break
            else:
                print("Opção inválida.")
    except (KeyboardInterrupt, EOFError):
        print()
    finally:
        DATABASE.encerra_conexao(conn)
        print("Sistema encerrado.")


if __name__ == "__main__":
    main()