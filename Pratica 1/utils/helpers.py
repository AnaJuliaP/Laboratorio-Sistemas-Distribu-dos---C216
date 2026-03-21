from data.alunos import CURSOS_DISPONIVEIS

def linha(char: str = "─", tamanho: int = 50) -> None:
    print(char * tamanho)


def cabecalho(titulo: str) -> None:
    print("\n\n")
    linha("═")
    print(f"  🎓  {titulo}")
    linha("═")


def pausar() -> None:
    input("\n  Pressione Enter para continuar...")


def exibir_cursos() -> None:
    print("\n  Cursos disponíveis:")
    linha("-")
    for sigla, nome in CURSOS_DISPONIVEIS.items():
        print(f"  {sigla:5} → {nome}")
    linha("-")


def formatar_aluno(aluno: dict) -> None:
    linha("-")
    print(f"  Matrícula : {aluno['matricula']}")
    print(f"  Nome      : {aluno['nome']}")
    print(f"  Email     : {aluno['email']}")
    print(f"  Curso     : {aluno['curso']} – {CURSOS_DISPONIVEIS.get(aluno['curso'], '?')}")

def email_valido(email: str) -> bool:
    """Verifica se o email contém '@' e um '.' no domínio."""
    return "@" in email and "." in email.split("@")[-1]


def curso_valido(sigla: str) -> bool:
    return sigla.upper() in CURSOS_DISPONIVEIS


def gerar_matricula(curso: str) -> str:
    """Retorna matrícula sequencial por curso. Ex: GES1, GES2, ADM1..."""
    from data.alunos import contadores
    contadores[curso] = contadores.get(curso, 0) + 1
    return f"{curso}{contadores[curso]}"
