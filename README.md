# CVOptimizer — Projeto de Avaliação Intermediária  

Aplicação web para análise e otimização de currículos (CV) desenvolvida com Streamlit e armazenamento local em SQLite.

> Observação: Este README foi estruturado com o auxílio de um modelo de IA.

---

# 1. Descrição do Problema e Solução Proposta

## Problema

Muitos candidatos enviam currículos genéricos para diferentes vagas e não possuem:

- Feedback estruturado por seção (resumo, experiência, habilidades, educação)
- Indicadores quantitativos da qualidade do currículo
- Comparação entre versões do mesmo currículo ou entre currículos de outros candidatos.
- Identificação clara de palavras-chave ausentes em relação a uma vaga

Ferramentas baseadas em IA que fazem esse tipo de análise existem, mas geralmente são pagas, complexas ou exigem integração com APIs externas.

---

## Solução Proposta

O **CVOptimizer** é uma aplicação web que:

- Permite upload de currículos (.pdf ou .docx)
- Armazena histórico em banco SQLite
- Gera análise estruturada por seções
- Exibe scores quantitativos por seção
- Mostra palavras-chave ausentes
- Permite comparação entre análises

Nesta versão, a análise é **simulada (mock)**, mas toda a arquitetura foi projetada para permitir futura integração com IA generativa real.

---

## Integração Futura com IA Generativa

A aplicação foi estruturada de forma modular para permitir que, futuramente, um modelo de IA possa:

- Extrair automaticamente informações de PDFs/DOCX
- Avaliar semanticamente o conteúdo do currículo
- Sugerir melhorias personalizadas por seção
- Reescrever trechos automaticamente
- Ajustar o currículo para uma vaga específica
- Calcular compatibilidade com descrição de vaga

O módulo `mock_analysis.py` poderá ser substituído por chamadas reais a APIs de LLM.

---

# 2. Escolhas de Design

## Arquitetura

- **Framework Web:** Streamlit  
- **Banco de Dados:** SQLite (via `sqlite3`)
- **Modelo para desenvolvimento:** GitHub Copilot 
- **Estrutura modular:**
  - `app.py`
  - `database.py`
  - `mock_analysis.py`
  - `pages/*.py`

---

## Justificativas

### Por que Streamlit?

- Permite prototipagem rápida
- Interface e backend no mesmo arquivo (reduz complexidade)
- Ideal para MVP
- Deploy simples via Streamlit Cloud

### Por que SQLite?

- Banco leve e nativo do Python
- Não exige servidor externo
- Fácil integração
- Ideal para protótipo funcional

### Por que GitHub Copilot?

- Possui versão gratuita
- Integração direta com o VSCode
- Não exige criação de conta (possível utilizar somente com a conta do GitHub).
- Resultados satisfatórios

---

## Componentes de UI utilizados

- `st.metric()` → visualização de scores  
- `st.bar_chart()` → comparação de seções  
- `st.columns()` → layout organizado  
- `st.expander()` → exibição de detalhes  
- `st.tabs()` → navegação estruturada  

Esses componentes foram escolhidos para tornar a interface visualmente rica, mesmo sendo um protótipo.

---

## Alternativas Consideradas

- React + FastAPI → descartado por aumentar complexidade e tempo de implementação
- Gradio → menos flexível para múltiplas páginas e persistência estruturada

---

# 3. O que Funcionou Bem

O uso do GitHub Copilot foi eficaz nas seguintes partes:

### ✔ Estrutura do Banco SQLite
- Criação das tabelas `resumes` e `analyses`
- Funções CRUD básicas
- Conexão e inicialização do banco

### ✔ Mock de Análise
- Geração de função com scores aleatórios
- Simulação de palavras-chave ausentes

### ✔ Interface Streamlit
- Página de upload
- Dashboard com tabela de currículos
- Visualização com métricas
- Gráfico de barras por seção
- Estrutura inicial da página de comparação

---

## Prompts Utilizados

1.
> generate a .gitignore for a project of a cv optimizer with streamlit and sqlite

2.
> Generate a generic initial README.md in portuguese

3.
> Generate a Python module using sqlite3 for CVOptimizer.
> Create a SQLite database with tables:
> 1. resumes (id, name, email, upload_date, file_path)
> 2. analyses (id, resume_id, summary_score, experience_score, skills_score, education_score, keywords_missing, analysis_date)
> Include functions to:
> - create_tables()
> - insert_resume(name, email, file_path)
> - insert_analysis(resume_id, summary_score, experience_score, skills_score, education_score, keywords_missing)
> - get_all_resumes()
> - get_analyses_for_resume(resume_id)
> Make the code modular so it can be imported into app.py


4.
> Generate a Python module to simulate resume analysis.
> Each analysis should return a dictionary with keys:
> summary_score, experience_score, skills_score, education_score, keywords_missing
> Values should be randomized integers (0-100) for scores, and a list of 3-5 missing keywords.

5.
> Create a Streamlit page to upload a resume (PDF or DOCX) and enter basic info (name, email).
> Save the resume info to the SQLite database using database.py.
> Show a success message when uploaded.

6.
> Create a Streamlit page that lists all uploaded resumes in a table.
> Show columns: Name, Email, Upload Date
> Add a button "View Analysis" next to each resume (even if analysis is mocked)

7.
> Create a Streamlit page that shows the analysis of a selected resume.
> Display section scores using st.metric in columns.
> Show a bar chart with scores for summary, experience, skills, and education.
> Display missing keywords in an expander.
> Use the generate_mock_analysis() function from mock_analysis.py

8.
> Create a Streamlit page to compare two resume analyses.
> Display side-by-side scores for summary, experience, skills, education.
> Highlight improvements or gaps with colors.
> Show missing keywords for each resume.

9.
> Enhance the Streamlit UI:
> - Use st.tabs for navigation
> - Use st.columns for metrics
> - Use st.expander for details
> - Optionally, add st.line_chart or st.bar_chart to show trends

Os prompts foram utilizados de forma incremental, com revisão e ajustes manuais após cada geração. Para a criação destes prompts foi utilizada uma ferramenta da IA para auxiliar na adequação.

---

# 4. O que Não Funcionou / Limitações

Algumas limitações e ajustes necessários:

- Ajustes visuais para melhorar organização da UI
- Tabela da aba "Lista currículo", foi gerada pelo Copilot com o cabeçalho no final e uma por linha.
- Na ausência de dados no banco as abas contidas no diretório pages "quebram".

Além disso:

- Não há integração real com IA (por requisito da avaliação)
- A análise é apenas simulada, não semântica
- Não há autenticação do usuário

---

# 5. Uso Efetivo do Agente de Codificação

O projeto foi desenvolvido majoritariamente com auxílio do GitHub Copilot.

Estratégia utilizada:

1. Criar arquivo base
2. Auxílio de ferramente externa (chat gpt) para a criação dos prompts para o Copilot.
3. Permitir geração automática de código
4. Revisar manualmente
5. Ajustar e refatorar
6. Commit incremental

A estrutura inicial foi gerada por IA, com supervisão humana para validação e ajustes.

Este README também foi estruturado com auxílio de modelo de IA.

---

# Execução

O projeto pode ser executado localmente, digitando o comando abaixo no diretório do projeto:

```bash
streamlit run app.py
```

A aplicação, atualmente, também pode ser executada por meio do link:

https://cvoptimizer-iagenerativa-aeypxfwpdwtmmftazjefvt.streamlit.app


---

# Requisitos

- Python 3.8+ (recomendado 3.12+)  
- streamlit  
- sqlite3 (nativo do Python)

---

# Conclusão

O CVOptimizer demonstra:

- Estrutura completa de aplicação web
- Persistência de dados
- Interface interativa
- Fluxo preparado para integração futura com IA generativa
- Uso extensivo e documentado de agente de codificação