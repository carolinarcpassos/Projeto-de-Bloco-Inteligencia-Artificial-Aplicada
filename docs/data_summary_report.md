# Data Summary Report (Esboço Inicial)

## 1. Fontes de Dados Mapeadas

| Fonte de Dados | Tipo de Dados | Acesso | Objetivo de Uso |
| :--- | :--- | :--- | :--- |
| **CAGED / MTE (Ministério do Trabalho e Emprego)** | Semiestruturado / API Pública | Dados Abertos MTE | Obter o quantitativo real de PcDs contratados formalmente por estado (UF) e setor econômico. |
| **IBGE (API SIDRA / PNAD Contínua)** | Semiestruturado / JSON | API Pública IBGE | Mapear a população PcD em idade ativa por região geográfica. |
| **Parâmetros da Lei de Cotas (Lei 8.213/91)** | Estruturado | Tabela Estática Interna | Calcular o volume de vagas obrigatórias por porte de empresa e setor para mensurar a conformidade (%). |
| **Base Simulada de Vagas (Gupy/LinkedIn Synthetics)** | Não estruturado / Semiestruturado | Arquivo JSON/CSV simulado | Avaliar requisitos de acessibilidade exigidos x oferecidos nas vagas. |
| **Cache Local (Fallback)** | Estruturado (JSON) | Arquivo `amostra_pcd_uf.json` | Garantir o funcionamento continuado da aplicação em caso de indisponibilidade das APIs governamentais. |

## 2. Qualidade e Desafios dos Dados
* Necessidade de padronizar códigos de UF e CNAE dos setores econômicos.
* Tratamento de campos nulos ou subnotificados sobre tipos específicos de deficiência.
* Necessidade de anonimização total de dados sensíveis (LGPD).