"""
Testes automatizados — Gerenciador de Alunos
Cobre: cadastro (3+ alunos/curso), listagem, busca por ID,
       atualização, remoção e reset.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.routes.aluno_routes import service   # acesso direto para reset entre testes

client = TestClient(app)


@pytest.fixture(autouse=True)
def limpar_estado():
    """Reseta o serviço antes de cada teste para garantir isolamento."""
    service.resetar()
    yield
    service.resetar()


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def cadastrar(nome: str, email: str, curso: str):
    return client.post("/api/v1/alunos/", json={
        "nome": nome,
        "email": email,
        "curso": curso,
    })


# ─────────────────────────────────────────────────────────────
# CADASTRO — pelo menos 3 alunos por curso
# ─────────────────────────────────────────────────────────────

class TestCadastro:

    def test_cadastrar_tres_alunos_ges(self):
        alunos = [
            ("Alice Souza",   "alice@ges.edu",   "GES"),
            ("Bruno Lima",    "bruno@ges.edu",   "GES"),
            ("Carla Mendes",  "carla@ges.edu",   "GES"),
        ]
        ids_esperados = ["GES1", "GES2", "GES3"]
        for (nome, email, curso), id_esp in zip(alunos, ids_esperados):
            resp = cadastrar(nome, email, curso)
            assert resp.status_code == 201, resp.text
            data = resp.json()
            assert data["id"] == id_esp
            assert data["curso"] == "GES"
            assert data["matricula"] == int(id_esp[3:])

    def test_cadastrar_tres_alunos_gec(self):
        alunos = [
            ("Daniel Costa",  "daniel@gec.edu",  "GEC"),
            ("Eduarda Faria", "eduarda@gec.edu", "GEC"),
            ("Felipe Torres", "felipe@gec.edu",  "GEC"),
        ]
        ids_esperados = ["GEC1", "GEC2", "GEC3"]
        for (nome, email, curso), id_esp in zip(alunos, ids_esperados):
            resp = cadastrar(nome, email, curso)
            assert resp.status_code == 201, resp.text
            assert resp.json()["id"] == id_esp

    def test_cadastrar_tres_alunos_gti(self):
        alunos = [
            ("Gabi Nunes",    "gabi@gti.edu",    "GTI"),
            ("Heitor Ramos",  "heitor@gti.edu",  "GTI"),
            ("Iris Barros",   "iris@gti.edu",    "GTI"),
        ]
        for i, (nome, email, curso) in enumerate(alunos, start=1):
            resp = cadastrar(nome, email, curso)
            assert resp.status_code == 201
            assert resp.json()["id"] == f"GTI{i}"

    def test_ids_independentes_por_curso(self):
        """Contadores de cursos diferentes são independentes."""
        r1 = cadastrar("Ana GES",  "ana@ges.edu",  "GES")
        r2 = cadastrar("Ana GEC",  "ana@gec.edu",  "GEC")
        assert r1.json()["id"] == "GES1"
        assert r2.json()["id"] == "GEC1"

    def test_curso_invalido_retorna_422(self):
        resp = cadastrar("X", "x@x.com", "XYZ")
        assert resp.status_code == 422

    def test_campos_obrigatorios(self):
        resp = client.post("/api/v1/alunos/", json={"nome": "Só Nome"})
        assert resp.status_code == 422


# ─────────────────────────────────────────────────────────────
# LISTAGEM
# ─────────────────────────────────────────────────────────────

class TestListagem:

    def test_listar_vazio(self):
        resp = client.get("/api/v1/alunos/")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_listar_apos_cadastros(self):
        cadastrar("A", "a@a.com", "GES")
        cadastrar("B", "b@b.com", "GEC")
        cadastrar("C", "c@c.com", "GTI")
        resp = client.get("/api/v1/alunos/")
        assert resp.status_code == 200
        lista = resp.json()
        assert len(lista) == 3
        ids = [a["id"] for a in lista]
        assert "GES1" in ids
        assert "GEC1" in ids
        assert "GTI1" in ids


# ─────────────────────────────────────────────────────────────
# BUSCA POR ID
# ─────────────────────────────────────────────────────────────

class TestBusca:

    def test_buscar_aluno_existente(self):
        cadastrar("João", "joao@ges.edu", "GES")
        resp = client.get("/api/v1/alunos/GES1")
        assert resp.status_code == 200
        assert resp.json()["nome"] == "João"

    def test_buscar_aluno_inexistente(self):
        resp = client.get("/api/v1/alunos/GES999")
        assert resp.status_code == 404

    def test_buscar_segundo_aluno_do_curso(self):
        cadastrar("Primeiro", "p@gec.edu", "GEC")
        cadastrar("Segundo",  "s@gec.edu", "GEC")
        resp = client.get("/api/v1/alunos/GEC2")
        assert resp.status_code == 200
        assert resp.json()["nome"] == "Segundo"


# ─────────────────────────────────────────────────────────────
# ATUALIZAÇÃO PARCIAL (PATCH)
# ─────────────────────────────────────────────────────────────

class TestAtualizacao:

    def test_atualizar_nome(self):
        cadastrar("Antigo Nome", "ant@ges.edu", "GES")
        resp = client.patch("/api/v1/alunos/GES1", json={"nome": "Novo Nome"})
        assert resp.status_code == 200
        assert resp.json()["nome"] == "Novo Nome"
        assert resp.json()["email"] == "ant@ges.edu"   # campo não alterado

    def test_atualizar_email(self):
        cadastrar("Maria", "antiga@gec.edu", "GEC")
        resp = client.patch("/api/v1/alunos/GEC1", json={"email": "nova@gec.edu"})
        assert resp.status_code == 200
        assert resp.json()["email"] == "nova@gec.edu"

    def test_atualizar_aluno_inexistente(self):
        resp = client.patch("/api/v1/alunos/GES99", json={"nome": "X"})
        assert resp.status_code == 404

    def test_atualizar_multiplos_campos(self):
        cadastrar("Old", "old@gti.edu", "GTI")
        resp = client.patch("/api/v1/alunos/GTI1", json={
            "nome": "New",
            "email": "new@gti.edu",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["nome"] == "New"
        assert data["email"] == "new@gti.edu"
        assert data["id"] == "GTI1"   # ID não muda


# ─────────────────────────────────────────────────────────────
# REMOÇÃO
# ─────────────────────────────────────────────────────────────

class TestRemocao:

    def test_deletar_aluno_existente(self):
        cadastrar("Del", "del@ges.edu", "GES")
        resp = client.delete("/api/v1/alunos/GES1")
        assert resp.status_code == 200
        assert "GES1" in resp.json()["mensagem"]

    def test_aluno_deletado_nao_aparece_na_listagem(self):
        cadastrar("A", "a@ges.edu", "GES")
        cadastrar("B", "b@ges.edu", "GES")
        client.delete("/api/v1/alunos/GES1")
        lista = client.get("/api/v1/alunos/").json()
        ids = [a["id"] for a in lista]
        assert "GES1" not in ids
        assert "GES2" in ids

    def test_id_nao_e_reutilizado_apos_delete(self):
        """Após deletar GES1, o próximo cadastro deve ser GES2, não GES1."""
        cadastrar("Primeiro", "p@ges.edu", "GES")
        client.delete("/api/v1/alunos/GES1")
        resp = cadastrar("Segundo", "s@ges.edu", "GES")
        assert resp.json()["id"] == "GES2"

    def test_deletar_aluno_inexistente(self):
        resp = client.delete("/api/v1/alunos/GEC999")
        assert resp.status_code == 404


# ─────────────────────────────────────────────────────────────
# RESET
# ─────────────────────────────────────────────────────────────

class TestReset:

    def test_resetar_lista(self):
        cadastrar("A", "a@ges.edu", "GES")
        cadastrar("B", "b@gec.edu", "GEC")
        resp = client.delete("/api/v1/alunos/")
        assert resp.status_code == 200
        assert client.get("/api/v1/alunos/").json() == []

    def test_apos_reset_contadores_reiniciam(self):
        cadastrar("X", "x@ges.edu", "GES")
        client.delete("/api/v1/alunos/")
        resp = cadastrar("Y", "y@ges.edu", "GES")
        assert resp.json()["id"] == "GES1"


# ─────────────────────────────────────────────────────────────
# MIDDLEWARE — verifica header customizado
# ─────────────────────────────────────────────────────────────

class TestMiddleware:

    def test_header_x_app_version_presente(self):
        resp = client.get("/api/v1/alunos/")
        assert resp.headers.get("x-app-version") == "1.0"

    def test_header_x_app_name_presente(self):
        resp = client.get("/")
        assert resp.headers.get("x-app-name") == "Gerenciador de Alunos"