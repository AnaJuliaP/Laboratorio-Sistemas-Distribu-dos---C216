from data.alunos import alunos
from utils.helpers import cabecalho, pausar, formatar_aluno, linha


def listar_alunos() -> None:
    """R – Listar todos os alunos cadastrados."""
    cabecalho("Lista de Alunos")

    if not alunos:
        print("  Nenhum aluno cadastrado ainda.")
        pausar()
        return

    print(f"  Total: {len(alunos)} aluno(s)\n")
    for aluno in alunos.values():
        formatar_aluno(aluno)
    linha("-")
    pausar()


def buscar_aluno() -> None:
    """R – Buscar aluno por matrícula ou parte do nome."""
    cabecalho("Buscar Aluno")

    termo = input("  Digite matrícula ou parte do nome: ").strip().upper()
    if not termo:
        pausar()
        return

    encontrados = [
        a for a in alunos.values()
        if termo in a["matricula"].upper() or termo in a["nome"].upper()
    ]

    if not encontrados:
        print("  ❌  Nenhum aluno encontrado.")
    else:
        print(f"\n  {len(encontrados)} resultado(s):\n")
        for aluno in encontrados:
            formatar_aluno(aluno)
        linha("-")

    pausar()
