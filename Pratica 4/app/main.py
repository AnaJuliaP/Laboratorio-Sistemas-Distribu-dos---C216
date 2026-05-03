from fastapi import FastAPI
from app.routes.aluno_routes import router as aluno_router
from app.middlewares.logging import log_requests
from app.middlewares.custom_header import add_custom_header

app = FastAPI(
    title="Gerenciador de Alunos",
    description="API CRUD para gerenciamento de alunos com middlewares",
    version="1.0.0",
)

app.middleware("http")(log_requests)
app.middleware("http")(add_custom_header)

app.include_router(aluno_router)


@app.get("/")
def root():
    return {"mensagem": "Gerenciador de Alunos API 🎓"}