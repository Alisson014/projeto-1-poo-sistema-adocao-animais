from src.api.routes import animal_route

from fastapi import FastAPI


app = FastAPI(
    title="Sistema de Adoção de Animais - API",
    version="1.0.0"
)


# Inclusão das rotas
app.include_router(animal_route.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "API de Adoção de animais rodando com sucesso"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)