# Documentação Técnica: Integração LLM Local & Arquitetura da API (TP4)

* **Projeto:** IncluaTech — Observatório de Inclusão PcD no Mercado de Trabalho
* **Autora:** Carolina Ramos da Costa Passos
* **Etapa:** TP4 — Integração de Modelo LLM Local com FastAPI, *Response Models* e Tratamento de Erros

---

## 1. Identificação e Escolha do Modelo LLM (Local)

### Contexto e Insumo Textual no Projeto
Conforme planejado na Seção 7 do *Project Charter*, o modelo de linguagem processa os textos não estruturados coletados pelos módulos de *Web Scraping* (`src/coleta_web.py` e `src/coleta_dinamica.py`) e armazenados em `data/processed/noticias_pcd.csv`. O objetivo é classificar automaticamente manchetes sobre inclusão e empregabilidade de Pessoas com Deficiência (PcD) quanto ao seu impacto e polaridade ESG (**Alerta / Denúncia**, **Neutro / Informativo** ou **Avanço / Positivo**).

### Modelo Selecionado
* **Identificador HuggingFace:** `nlptown/bert-base-multilingual-uncased-sentiment`
* **Arquitetura:** BERT (*Bidirectional Encoder Representations from Transformers*) multilíngue com *fine-tuning* para classificação de sentimento em 5 níveis (`1 star` a `5 stars`).

### Avaliação pelos Critérios de Seleção

| Critério | Avaliação Técnica no Projeto IncluaTech |

| **Desempenho** | Modelo encoder bidirecional pré-treinado em múltiplos idiomas (incluindo Português), capturando nuances contextuais das manchetes da Agência Brasil. A saída em escala de 1 a 5 estrelas com escore de probabilidade permite mapear polaridades críticas (`1–2 stars`), neutras (`3 stars`) e positivas (`4–5 stars`). |

| **Custo Computacional Local** | Possui ~167 milhões de parâmetros (~670 MB em disco) e consome entre **1,1 GB e 1,4 GB de RAM** durante a inferência. Roda de forma fluida diretamente na **CPU** (< 200 ms por manchete), dispensando GPU dedicada. |

| **Acessibilidade Local** | Modelo *open-source* hospedado no HuggingFace Model Hub, integrado via `transformers` e `torch` (PyTorch). Após o download único (`src/baixar_modelo.py`), opera com `local_files_only=True`, garantindo execução **100% offline** sem chaves de API externas. |

> **Plano B (Alternativa Avaliada):** `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli` (classificação *zero-shot* multilíngue), mantido como alternativa para categorização temática livre caso não haja mapeamento por polaridade, embora apresente maior latência em CPU.

---

## 2. Integração do LLM Local com FastAPI (`api/main.py`)

A integração foi implementada diretamente no backend REST existente (`api/main.py`), mantendo os endpoints da TP3 (`GET /colaboradores` e `POST /colaboradores`) e adicionando:

* **Carregamento Único via `lifespan`:** O tokenizador e o modelo são carregados apenas uma vez na inicialização do servidor FastAPI com `local_files_only=True`, evitando sobrecarga de memória a cada requisição.

* **Endpoint `POST /processar_texto`:** Recebe a manchete ou texto relacionado à temática PcD, valida os dados de entrada e executa a inferência local em CPU (`device=-1`).

---

## 3. Manipulação e Validação das Respostas (*Response Models*)

Para assegurar um contrato de dados rígido e previsível entre a API FastAPI e o painel Streamlit, foram definidos schemas com **Pydantic**:

* **Schema de Entrada (`TextoEntradaSchema`):** Valida que o campo `texto` tenha entre **5 e 500 caracteres**, além de aceitar o campo opcional `fonte` (padrão: `"Agência Brasil"`).

* **Response Model (`ProcessamentoTextoResponse`):** Vinculado ao decorator `@app.post("/processar_texto", response_model=ProcessamentoTextoResponse)`, garantindo que toda resposta bem-sucedida (`200 OK`) siga rigorosamente a estrutura abaixo:

```json
{
  "status": "sucesso",
  "texto_analisado": "Cargos de liderança são só 1,5% das vagas para pessoas com deficiência",
  "fonte": "Agência Brasil",
  "tipo_analise": "Classificação de Sentimento e Impacto ESG/PcD",
  "motor_llm": "nlptown/bert-base-multilingual-uncased-sentiment",
  "resultado": {
    "categoria_incluatech": "Alerta / Denúncia de Exclusão",
    "rotulo_original": "1 star",
    "confianca": 0.6842,
    "resumo_interpretacao": "O texto aponta barreiras severas, desigualdade ou déficit de inclusão PcD."
  }
}
```

## 4. Tratamento Robusto de Erros HTTP

A API implementa exceções HTTP semânticas (`HTTPException`) para diagnosticar falhas com precisão e orientar tanto clientes técnicos quanto usuários finais no painel Streamlit:

| Código HTTP | Cenário de Falha | Comportamento e Feedback ao Usuário |

| **`400 Bad Request`** | Texto enviado contém apenas espaços em branco após `.strip()`. | Rejeita a requisição antes da inferência e solicita ao menos 5 caracteres válidos. |

| **`422 Unprocessable Entity`** | Payload JSON com tipo inválido, campo ausente ou tamanho fora do intervalo `[5, 500]`. | Validação automática do Pydantic detalhando o campo incorreto; no painel Streamlit, exibe alerta orientativo. |

| **`503 Service Unavailable`** | Modelo LLM não carregado na memória (cache local ausente ou falha no `lifespan`). | Informa que o motor de IA está indisponível e instrui executar `python src/baixar_modelo.py`. |

| **`500 Internal Server Error`** | Erro inesperado de execução ou memória no PyTorch/Transformers (`RuntimeError`). | Registra o erro detalhado no `logging` do servidor e retorna mensagem segura ao cliente sem expor *stack traces*. |

| **Falha de Conexão (UI)** | Servidor Uvicorn desligado durante uso da página `2_📰_Noticias.py`. | Captura `ConnectionError` / `Timeout` no Streamlit e orienta iniciar a API na porta `8000`. |

---

## 5. Roteiro de Verificação e Testes Executados

1. **Download do modelo offline:**
   ```bash
   python src/baixar_modelo.py
   ```

## 6. Inicialização da API FastAPI

   ```bash
   uvicorn api.main:app --reload --port 8000
   ```

## 7. Validação no Swagger UI (http://localhost:8000/docs)

    GET /: Confirma "llm_carregado": true.

    POST /processar_texto (texto válido): Retorna status 200 OK com JSON validado pelo ProcessamentoTextoResponse.

    POST /processar_texto (texto curto, ex.: "abc"): Retorna status 422 Unprocessable Entity.

## 8. Validação Ponta a Ponta no Streamlit (streamlit run Home.py)

Página Notícias (pages/2_📰_Noticias.py) envia a manchete raspada para a API e renderiza a categoria ESG e o escore de confiança.