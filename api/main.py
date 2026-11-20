import csv
import json
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Dict, List, Optional

import requests
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("incluatech_api")

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = BASE_DIR / "data" / "raw" / "amostra_pcd_uf.json"

MODEL_ID = "nlptown/bert-base-multilingual-uncased-sentiment"
modelos_locais = {}

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "openrouter/free"


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
    description="API REST para gestão de indicadores PcD, análise de notícias com LLM local (HuggingFace) e assistente ESG com memória (OpenRouter).",
    version="3.0.0",
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


# =====================================================================
# TP5: MEMÓRIA CONVERSACIONAL & PROMPT ENGINEERING VIA OPENROUTER
# =====================================================================
historico_conversas: Dict[str, List[Dict[str, str]]] = {}


class ChatRequestSchema(BaseModel):
    session_id: str = Field(default="sessao_padrao", description="Identificador da sessão do usuário")
    mensagem: str = Field(..., min_length=2, max_length=1000, description="Pergunta do gestor de RH/ESG")
    api_key: Optional[str] = Field(default=None, description="Chave da API OpenRouter (ou via env OPENROUTER_API_KEY)")


class ChatResponseSchema(BaseModel):
    status: str = "sucesso"
    session_id: str
    resposta: str
    turnos_na_memoria: int
    fontes_utilizadas: List[str]


def construir_contexto_dados_projeto() -> tuple[str, List[str]]:
    """Consolida os dados estruturados (JSON) e não estruturados (CSV) do IncluaTech para grounding do LLM."""
    fontes = []
    resumo_colab = "Base de colaboradores indisponível."
    if JSON_PATH.exists():
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            registros = json.load(f)
        total = len(registros)
        if total > 0:
            acess_sim = sum(1 for r in registros if r.get("Acessibilidade") == "Sim")
            acess_nao = sum(1 for r in registros if r.get("Acessibilidade") == "Não")
            remoto = sum(1 for r in registros if r.get("Modelo") == "Remoto")
            media_meses = round(sum(r.get("Tempo Casa (Meses)", 0) for r in registros) / total, 1)

            setores_stats = {}
            for r in registros:
                s = r.get("Setor", "Outros")
                setores_stats.setdefault(s, []).append(r.get("Tempo Casa (Meses)", 0))
            detalhe_setores = "; ".join(
                f"{s}: {len(v)} colab. (média {round(sum(v)/len(v), 1)} meses)"
                for s, v in setores_stats.items()
            )
            resumo_colab = (
                f"Total de {total} colaboradores PcD monitorados. "
                f"Acessibilidade Plena: {acess_sim}/{total} ({round(acess_sim/total*100, 1)}%); "
                f"Sem Acessibilidade: {acess_nao}/{total}. "
                f"Trabalho Remoto: {remoto}/{total}. Tempo médio de casa geral: {media_meses} meses. "
                f"Detalhamento por setor -> {detalhe_setores}."
            )
            fontes.append("amostra_pcd_uf.json")

    noticias_csv = BASE_DIR / "data" / "processed" / "noticias_pcd.csv"
    resumo_noticias = "Nenhuma notícia raspada disponível."
    if noticias_csv.exists():
        with open(noticias_csv, "r", encoding="utf-8") as f:
            leitor = list(csv.DictReader(f))
        if leitor:
            manchetes = [row["manchete"] for row in leitor[:10] if row.get("manchete")]
            resumo_noticias = "Manchetes recentes coletadas (Agência Brasil): " + " | ".join(manchetes)
            fontes.append("data/processed/noticias_pcd.csv")

    contexto = f"DADOS INTERNOS DE RH:\n{resumo_colab}\n\nMONITORAMENTO DE MÍDIA (WEB SCRAPING):\n{resumo_noticias}"
    return contexto, fontes


@app.post(
    "/chat_esg",
    response_model=ChatResponseSchema,
    summary="Assistente Conversacional ESG & Inclusão PcD com Memória via OpenRouter (TP5)"
)
def conversar_assistente_esg(payload: ChatRequestSchema):
    pergunta = payload.mensagem.strip()
    if not pergunta:
        raise HTTPException(status_code=400, detail="A mensagem não pode estar vazia.")

    contexto_dados, fontes = construir_contexto_dados_projeto()
    historico = historico_conversas.setdefault(payload.session_id, [])

    system_prompt = (
        "Você é o Assistente Estratégico de Governança ESG e Inclusão PcD da plataforma IncluaTech, "
        "alinhado aos ODS 8 (Meta 8.5) e ODS 10 (Meta 10.2) da Agenda 2030.\n"
        "Use EXCLUSIVAMENTE os dados reais do projeto abaixo para fundamentar suas respostas, "
        "citando números, setores e manchetes quando pertinente, e mantendo coerência com o histórico da conversa.\n"
        "Responda sempre em português claro, objetivo e com recomendações práticas para equipes de RH.\n\n"
        f"{contexto_dados}"
    )

    chave_api = (payload.api_key or os.getenv("OPENROUTER_API_KEY", "")).strip()

    try:
        if chave_api:
            mensagens_openrouter = [{"role": "system", "content": system_prompt}]
            for turno in historico[-8:]:
                mensagens_openrouter.append({"role": turno["role"], "content": turno["content"]})
            mensagens_openrouter.append({"role": "user", "content": pergunta})

            headers = {
                "Authorization": f"Bearer {chave_api}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8501",
                "X-Title": "IncluaTech ESG Assistant"
            }
            body = {
                "model": OPENROUTER_MODEL,
                "messages": mensagens_openrouter,
                "temperature": 0.3
            }

            resp_or = requests.post(OPENROUTER_URL, headers=headers, json=body, timeout=90)
            if resp_or.status_code != 200:
                erro_api = resp_or.json().get("error", {}).get("message", resp_or.text)
                raise HTTPException(
                    status_code=resp_or.status_code,
                    detail=f"Erro na API OpenRouter: {erro_api}"
                )

            texto_resposta = resp_or.json()["choices"][0]["message"]["content"]
        else:
            contexto_anterior = (
                f"Considerando nossa interação anterior sobre '{historico[-2]['content'][:60]}...', "
                if len(historico) >= 2 else ""
            )
            texto_resposta = (
                f"{contexto_anterior}Com base nos dados consolidados do IncluaTech ({', '.join(fontes)}):\n\n"
                f"• **Panorama de Retenção & Acessibilidade:** {contexto_dados.splitlines()[1]}\n"
                f"• **Contexto de Mídia:** {contexto_dados.splitlines()[4]}\n\n"
                "💡 *Nota:* Insira sua **OpenRouter API Key** na barra lateral para ativar as respostas generativas completas."
            )

        historico.append({"role": "user", "content": pergunta})
        historico.append({"role": "assistant", "content": texto_resposta})

        return ChatResponseSchema(
            status="sucesso",
            session_id=payload.session_id,
            resposta=texto_resposta,
            turnos_na_memoria=len(historico),
            fontes_utilizadas=fontes
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Erro no assistente conversacional /chat_esg: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar interação conversacional: {str(exc)}"
        )


@app.delete("/chat_esg/{session_id}", summary="Limpar memória conversacional da sessão")
def limpar_memoria_chat(session_id: str):
    historico_conversas.pop(session_id, None)
    return {"status": "sucesso", "mensagem": f"Memória da sessão '{session_id}' limpa com sucesso."}