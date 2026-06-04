# Post LinkedIn — Support Ticket Insight Lab

> Copie o texto abaixo diretamente para o LinkedIn.
> O carrossel exportado como PDF está em `docs/linkedin/slides.pdf`.

---

Construí um sistema que lê cada chamado de suporte de TI e devolve categoria, prioridade sugerida e risco de SLA, o tipo de leitura que a triagem manual raramente faz a tempo.

Num caso com 100 chamados de infraestrutura, 59% já chegavam marcados como alta ou crítica. Sem uma leitura estruturada, esse volume vira fila, ruído e SLA estourado.

O Support Ticket Insight Lab recebe um CSV de tickets, valida o schema, calcula idade e tempo de resolução e envia cada chamado a um LLM que gera 6 dimensões de análise: categoria, sentimento, prioridade, justificativa, resumo e risco de SLA. Tudo cai num dashboard com filtros e exportação.

O resultado prático:
• 59% de prioridade alta/crítica, onde a equipe deveria olhar primeiro
• 1,5 dia de tempo médio de resolução, baseline real para medir melhoria
• VPN, Certificado e Storage no topo dos serviços, alvos claros de causa-raiz

Stack: Python · Streamlit · pandas · OpenAI / Gemini / Groq · GitHub Actions

Quem trabalha com operação de TI: vocês confiariam numa prioridade sugerida por LLM para reordenar a fila, ou só como segunda opinião do analista?

#AnáliseDeDados #InteligênciaArtificial #SuporteTI

---

**Metadados do post**

| Campo | Valor |
|---|---|
| Caracteres (aprox.) | 1.130 |
| Hook | "Construí um sistema que…" |
| Modelo de hook | "Construí um sistema que detecta [problema] que operações humanas nunca veem" |
| Hashtags | 3 (máximo recomendado) |
| Carrossel | `docs/linkedin/slides.pdf` |
| App publicado | https://support-ticket-insight-lab.streamlit.app/ |
| Repositório | https://github.com/anotther/support-ticket-insight-lab |
