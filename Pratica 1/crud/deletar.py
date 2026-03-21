from data.alunos import alunos
from utils.helpers import cabecalho, pausar, formatar_aluno


def deletar_aluno() -> None:
    """D – Remover um aluno pelo número de matrícula."""
    cabecalho("Remover Aluno")

    matricula = input("  Matrícula do aluno a remover: ").strip().upper()
    if matricula not in alunos:
        print("  ❌  Matrícula não encontrada.")
        pausar()
        return

    formatar_aluno(alunos[matricula])

    confirmacao = input("\n  Confirma remoção? (s/N): ").strip().lower()
    if confirmacao == "s":
        del alunos[matricula]
        print("  ✅  Aluno removido com sucesso!")
    else:
        print("  ℹ️   Operação cancelada.")

    pausar()
