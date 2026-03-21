from utils.helpers import cabecalho, linha, pausar
from crud.criar import criar_aluno
from crud.ler import listar_alunos, buscar_aluno
from crud.atualizar import atualizar_aluno
from crud.deletar import deletar_aluno


def menu() -> str:
    """Exibe o menu principal e retorna a opção digitada."""
    cabecalho("Sistema de Alunos – Faculdade Python")
    print("  1 │ Cadastrar aluno")
    print("  2 │ Listar alunos")
    print("  3 │ Buscar aluno")
    print("  4 │ Atualizar aluno")
    print("  5 │ Remover aluno")
    print("  0 │ Sair")
    linha()
    return input("  Escolha uma opção: ").strip()


def main() -> None:
    acoes = {
        "1": criar_aluno,
        "2": listar_alunos,
        "3": buscar_aluno,
        "4": atualizar_aluno,
        "5": deletar_aluno,
    }

    while True:
        opcao = menu()

        if opcao == "0":
            cabecalho("Encerrando o sistema")
            print("  Até logo! 👋\n")
            break
        elif opcao in acoes:
            acoes[opcao]()
        else:
            print("  ❌  Opção inválida. Tente novamente.")
            pausar()


if __name__ == "__main__":
    main()
