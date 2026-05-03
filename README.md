# Support Ticket Insight Lab

Aplicacao Python e Streamlit para analisar tickets de suporte de infraestrutura a partir de um CSV enviado pelo usuario.

O MVP valida o schema do CSV, diferencia tickets abertos e fechados, calcula idade ou tempo de resolucao e prepara a base para classificacao, sentimento, sugestao de prioridade, resumo operacional, dashboard e exportacao.

Importante: a aplicacao nao usa dados mockados, CSV de exemplo embutido ou fallback silencioso. Sem upload de CSV, ela mostra apenas instrucoes e requisitos de schema.

## Requisitos

- Python 3.11 ou superior.
- Dependencias em `requirements.txt`.
- Um CSV de tickets com as colunas obrigatorias.

## Instalar e executar localmente

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## Schema do CSV

Colunas obrigatorias:

| Coluna | Tipo esperado | Descricao |
|---|---|---|
| `ticket_id` | texto | Identificador unico do ticket. |
| `title` | texto | Titulo ou assunto do ticket. |
| `description` | texto | Descricao principal da solicitacao ou incidente. |
| `opened_at` | data/datetime | Data de abertura do ticket. |
| `closed_at` | data/datetime/vazio | Data de fechamento. Valor vazio significa ticket aberto. |
| `priority` | texto | Prioridade original no sistema de origem. |

Colunas recomendadas:

`status`, `requester_department`, `requester_location`, `affected_service`, `asset_id`, `assigned_team`, `assignee`, `channel`, `impact`, `urgency`, `resolution_notes`.

## Tratamento de datas

- Tickets com `closed_at` vazio sao tratados como abertos.
- Tickets com `closed_at` preenchido sao tratados como fechados.
- Tickets abertos recebem `analysis_ticket_age_days`.
- Tickets fechados recebem `analysis_resolution_time_days`.
- Datas invalidas, `opened_at` ausente e `closed_at` anterior a `opened_at` geram erro de validacao.

## Configuracao de provedores

A selecao de provedores LLM sera implementada nas proximas tarefas do backlog. O comportamento esperado e:

- usar variaveis de ambiente quando houver chave valida para o provedor selecionado;
- solicitar chave via interface Streamlit quando a chave nao estiver no ambiente;
- manter chaves digitadas somente na sessao Streamlit;
- interromper o processamento com mensagem clara quando a chave estiver ausente;
- nunca usar analise mockada quando o provedor nao estiver configurado.

## Testes e qualidade

```bash
ruff check .
ruff format --check .
pytest
PYTHONPATH=src python -m py_compile app/streamlit_app.py
```

## Deploy no Streamlit Cloud

1. Conecte o repositorio `Anotther/support-ticket-insight-lab` ao Streamlit Cloud.
2. Configure o arquivo principal como `app/streamlit_app.py`.
3. Use `requirements.txt` para instalar as dependencias.
4. Configure secrets do Streamlit Cloud para chaves de provedores quando necessario.

## Estrutura

```text
support-ticket-insight-lab/
├─ app/
│  └─ streamlit_app.py
├─ src/
│  └─ ticket_insight/
├─ tests/
├─ .github/
│  └─ workflows/
├─ README.md
├─ requirements.txt
├─ action_plan.md
└─ resumo_executivo.md
```
