from data.alunos import alunos
from utils.helpers import cabecalho, pausar, formatar_aluno, email_valido


def atualizar_aluno() -> None:
    """U – Atualizar nome e/ou email de um aluno existente."""
    cabecalho("Atualizar Aluno")

    matricula = input("  Matrícula do aluno: ").strip().upper()
    if matricula not in alunos:
        print("  ❌  Matrícula não encontrada.")
        pausar()
        return

    aluno = alunos[matricula]
    print("\n  Dados atuais:")
    formatar_aluno(aluno)
    print("\n  (Deixe em branco para manter o valor atual)\n")

    novo_nome = input(f"  Novo nome [{aluno['nome']}]: ").strip()
    novo_email = input(f"  Novo email [{aluno['email']}]: ").strip()

    if novo_nome:
        aluno["nome"] = novo_nome

    if novo_email:
        if not email_valido(novo_email):
            print("  ❌  Email inválido. Campo mantido.")
        else:
            aluno["email"] = novo_email

    print("\n  ✅  Dados atualizados com sucesso!")
    pausar()
