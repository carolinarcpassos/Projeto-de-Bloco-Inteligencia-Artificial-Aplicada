# Escolha e Justificativa do Modelo LLM Local — Projeto IncluaTech

## 1. Contexto e Insumo Textual no Projeto
Conforme planejado na Seção 7 do *Project Charter*, o modelo de linguagem processa os textos não estruturados coletados pelos módulos de Web Scraping (`src/coleta_web.py` e `src/coleta_dinamica.py`) e armazenados em `data/processed/noticias_pcd.csv`. O objetivo é classificar automaticamente manchetes sobre inclusão e empregabilidade de Pessoas com Deficiência (PcD) quanto ao seu impacto e polaridade ESG (Alerta/Denúncia, Neutro/Informativo ou Avanço/Positivo).

## 2. Modelo Selecionado
* **Identificador HuggingFace:** `nlptown/bert-base-multilingual-uncased-sentiment`
* **Arquitetura:** BERT (*Bidirectional Encoder Representations from Transformers*) multilíngue com *fine-tuning* para classificação de sentimento em 5 níveis (`1 star` a `5 stars`).

## 3. Avaliação pelos Critérios de Seleção

### a) Desempenho
* **Compreensão Semântica em Português:** Por ser um modelo encoder bidirecional pré-treinado em múltiplos idiomas (incluindo o português), captura nuances contextuais das manchetes jornalísticas da Agência Brasil (como termos de denúncia, déficit de cotas ou conquistas de acessibilidade).
* **Adequação à Tarefa:** A saída em escala de 1 a 5 estrelas acompanhada de escore de probabilidade permite mapear diretamente a polaridade para o domínio do IncluaTech: notas `1–2 stars` sinalizam alertas ou barreiras de inclusão; `3 stars` indicam conteúdo informativo neutro; e `4–5 stars` apontam iniciativas positivas e avanços ESG.

### b) Custo Computacional Local
* **Leveza de Hardware:** O modelo possui cerca de 167 milhões de parâmetros (~670 MB em disco) e utiliza aproximadamente **1,1 GB a 1,4 GB de memória RAM** durante a execução.
* **Execução sem GPU:** Roda de forma fluida diretamente na **CPU** de computadores convencionais de desenvolvimento, com tempo médio de inferência inferior a 200 ms por manchete, dispensando placas de vídeo (GPU) dedicadas.

### c) Acessibilidade Local (Execução 100% Offline)
* Disponível abertamente no HuggingFace Model Hub sob licença aberta.
* Integrado via bibliotecas `transformers` e `torch` (PyTorch). Após o download único para o cache local da máquina, o carregamento é feito com o parâmetro `local_files_only=True`, garantindo operação totalmente local sem necessidade de chaves de API ou conexão externa.

## 4. Plano B (Alternativa Avaliada)
* **Modelo Alternativo:** `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli` (classificação *zero-shot* multilíngue). Foi mantido como alternativa caso seja necessário classificar manchetes em categorias temáticas livres sem mapeamento por polaridade, embora apresente maior latência em CPU (~2,5x mais lento que o BERT escolhido).