from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import json

app = FastAPI(
    title="API IncluaTech - Inclusão PcD",
    description="API REST para consulta e cadastro de indicadores PcD.",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = BASE_DIR / "amostra_pcd_uf.json"

class ColaboradorSchema(BaseModel):
    ID: str
    Setor: str
    Tipo_Deficiencia: str
    Modelo: str
    Tempo_Casa_Meses: int
    Acessibilidade: str
    Escolaridade: str

@app.get("/", summary="Rota Principal")
def home():
    return {"status": "Ativo", "mensagem": "API IncluaTech operacional."}

@app.get("/colaboradores", summary="Consultar colaboradores (GET)")
def listar_colaboradores():
    if not JSON_PATH.exists():
        raise HTTPException(status_code=404, detail="Base de dados não encontrada.")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@app.post("/colaboradores", summary="Cadastrar novo colaborador (POST)")
def cadastrar_colaborador(novo: ColaboradorSchema):
    if not JSON_PATH.exists():
        dados = []
    else:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            dados = json.load(f)

    registro = {
        "ID": novo.ID,
        "Setor": novo.Setor,
        "Tipo Deficiência": novo.Tipo_Deficiencia,
        "Modelo": novo.Modelo,
        "Tempo Casa (Meses)": novo.Tempo_Casa_Meses,
        "Acessibilidade": novo.Acessibilidade,
        "Escolaridade": novo.Escolaridade
    }

    dados.append(registro)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    return {"mensagem": "Colaborador cadastrado com sucesso!", "dados": registro}