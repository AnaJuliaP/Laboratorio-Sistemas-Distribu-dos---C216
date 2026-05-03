from typing import List
from app.schemas.aluno import Aluno, AlunoCreate, AlunoUpdate


class AlunoService:
    def __init__(self):
        self._alunos: List[Aluno] = []
        # Contador sequencial por curso — nunca decrementa (IDs não reutilizados)
        self._contadores: dict[str, int] = {}

    def listar(self) -> List[Aluno]:
        return self._alunos

    def buscar_por_id(self, aluno_id: str) -> Aluno | None:
        for aluno in self._alunos:
            if aluno.id == aluno_id:
                return aluno
        return None

    def criar(self, dados: AlunoCreate) -> Aluno:
        curso = dados.curso
        # Incrementa o contador do curso (nunca reutiliza)
        self._contadores[curso] = self._contadores.get(curso, 0) + 1
        matricula = self._contadores[curso]
        aluno_id = f"{curso}{matricula}"

        novo_aluno = Aluno(
            id=aluno_id,
            matricula=matricula,
            nome=dados.nome,
            email=dados.email,
            curso=curso,
        )
        self._alunos.append(novo_aluno)
        return novo_aluno

    def atualizar(self, aluno_id: str, dados: AlunoUpdate) -> Aluno | None:
        aluno = self.buscar_por_id(aluno_id)
        if not aluno:
            return None
        if dados.nome is not None:
            aluno.nome = dados.nome
        if dados.email is not None:
            aluno.email = dados.email
        if dados.curso is not None:
            aluno.curso = dados.curso
        return aluno

    def deletar(self, aluno_id: str) -> bool:
        aluno = self.buscar_por_id(aluno_id)
        if not aluno:
            return False
        self._alunos.remove(aluno)
        return True

    def resetar(self) -> None:
        """Remove todos os alunos E zera os contadores."""
        self._alunos.clear()
        self._contadores.clear()