from data.alunos import alunos
from utils.helpers import cabecalho, pausar, exibir_cursos, email_valido, curso_valido, gerar_matricula


def criar_aluno() -> None:
    """C – Cadastrar um novo aluno."""
    cabecalho("Cadastrar Aluno")

    nome = input("  Nome completo: ").strip()
    if not nome:
        print("  ❌  Nome não pode ser vazio.")
        pausar()
        return

    email = input("  Email: ").strip()
    if not email_valido(email):
        print("  ❌  Email inválido.")
        pausar()
        return

    exibir_cursos()
    curso = input("  Sigla do curso: ").strip().upper()
    if not curso_valido(curso):
        print("  ❌  Curso inválido.")
        pausar()
        return

    matricula = gerar_matricula(curso)

    alunos[matricula] = {
        "matricula": matricula,
        "nome": nome,
        "email": email,
        "curso": curso,
    }

    print(f"\n  ✅  Aluno cadastrado com matrícula: {matricula}")
    pausar()
