import json
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("incluatech_api")

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = BASE_DIR / "amostra_pcd_uf.json"

MODEL_ID = "nlptown/bert-base-multilingual-uncased-sentiment"
modelos_locais = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info(f"Carregando modelo LLM local (offline): {MODEL_ID}")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, local_files_only=True)
        model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_ID, local_files_only=True
        )
        modelos_locais["nlp_pipeline"] = pipeline(
            task="sentiment-analysis",
            model=model,
            tokenizer=tokenizer,
            device=-1
        )
        logger.info("Modelo LLM carregado com sucesso do cache local!")
    except OSError as os_err:
        logger.error(f"Modelo não encontrado no cache local: {os_err}")
        modelos_locais["nlp_pipeline"] = None
    except Exception as e:
        logger.error(f"Erro inesperado ao carregar o modelo LLM: {e}")
        modelos_locais["nlp_pipeline"] = None

    yield

    modelos_locais.clear()
    logger.info("Recursos do modelo LLM liberados.")


app = FastAPI(
    title="API IncluaTech - Inclusão PcD & NLP Local",
    description="API REST para gestão de indicadores PcD e análise de notícias com LLM local (HuggingFace).",
    version="2.0.0",
    lifespan=lifespan
)


class ColaboradorSchema(BaseModel):
    ID: str
    Setor: str
    Tipo_Deficiencia: str
    Modelo: str
    Tempo_Casa_Meses: int
    Acessibilidade: str
    Escolaridade: str


class TextoEntradaSchema(BaseModel):
    texto: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Manchete ou trecho textual sobre inclusão PcD para análise.",
        examples=["Cargos de liderança são só 1,5% das vagas para pessoas com deficiência"]
    )
    fonte: Optional[str] = Field(
        default="Agência Brasil",
        description="Origem do texto analisado."
    )


class AnaliseSentimentoSchema(BaseModel):
    categoria_incluatech: str = Field(..., description="Classificação adaptada ao domínio ESG/PcD")
    rotulo_original: str = Field(..., description="Saída bruta do modelo (1 a 5 stars)")
    confianca: float = Field(..., ge=0.0, le=1.0, description="Probabilidade da predição")
    resumo_interpretacao: str = Field(..., description="Explicação amigável para o painel")


class ProcessamentoTextoResponse(BaseModel):
    status: str = Field(default="sucesso")
    texto_analisado: str
    fonte: str
    tipo_analise: str
    motor_llm: str
    resultado: AnaliseSentimentoSchema


def mapear_categoria_pcd(rotulo: str) -> tuple[str, str]:
    mapa = {
        "1 star": (
            "Alerta / Denúncia de Exclusão",
            "O texto aponta barreiras severas, desigualdade ou déficit de inclusão PcD."
        ),
        "2 stars": (
            "Alerta / Ponto de Atenção",
            "O texto indica desafios ou fragilidades nas condições de trabalho/acessibilidade."
        ),
        "3 stars": (
            "Neutro / Informativo",
            "O texto apresenta dados, normas ou informações institucionais sem viés crítico."
        ),
        "4 stars": (
            "Avanço / Iniciativa Positiva",
            "O texto destaca ações afirmativas, boas práticas ou melhorias na empregabilidade PcD."
        ),
        "5 stars": (
            "Alto Impacto Positivo / Inclusão Plena",
            "O texto evidencia conquistas expressivas de acessibilidade e equidade no trabalho."
        ),
    }
    return mapa.get(rotulo, ("Classificação Indefinida", "Não foi possível interpretar o rótulo."))


@app.get("/", summary="Rota Principal")
def home():
    return {
        "status": "Ativo",
        "mensagem": "API IncluaTech operacional.",
        "llm_carregado": modelos_locais.get("nlp_pipeline") is not None
    }


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


@app.post(
    "/processar_texto",
    response_model=ProcessamentoTextoResponse,
    status_code=status.HTTP_200_OK,
    summary="Analisar sentimento e impacto ESG de textos PcD via LLM local"
)
def processar_texto(payload: TextoEntradaSchema):
    classificador = modelos_locais.get("nlp_pipeline")
    if classificador is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Serviço de IA indisponível: o modelo LLM local não está carregado. "
                "Execute o script src/baixar_modelo.py e reinicie a API."
            )
        )

    texto_limpo = payload.texto.strip()
    if len(texto_limpo) < 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O texto enviado deve conter pelo menos 5 caracteres válidos (sem contar espaços)."
        )

    try:
        saida = classificador(texto_limpo, truncation=True, max_length=512)[0]
        rotulo = saida["label"]
        score = round(float(saida["score"]), 4)
        categoria, interpretacao = mapear_categoria_pcd(rotulo)

        return ProcessamentoTextoResponse(
            status="sucesso",
            texto_analisado=texto_limpo,
            fonte=payload.fonte or "Não informada",
            tipo_analise="Classificação de Sentimento e Impacto ESG/PcD",
            motor_llm=MODEL_ID,
            resultado=AnaliseSentimentoSchema(
                categoria_incluatech=categoria,
                rotulo_original=rotulo,
                confianca=score,
                resumo_interpretacao=interpretacao
            )
        )
    except RuntimeError as rt_err:
        logger.error(f"Erro de runtime/memória na inferência: {rt_err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno de processamento no motor PyTorch/Transformers."
        )
    except Exception as exc:
        logger.error(f"Erro inesperado na rota /processar_texto: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Falha interna inesperada ao processar o texto no modelo local."
        )