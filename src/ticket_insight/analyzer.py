import importlib.resources
import json
import tomllib
from collections.abc import Mapping

from ticket_insight.pipeline import TicketAnalysisResult, TicketAnalyzer


def _load_prompts() -> dict:
    data = importlib.resources.files("ticket_insight").joinpath("prompts.toml").read_bytes()
    return tomllib.loads(data.decode())


class LLMTicketAnalyzer(TicketAnalyzer):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        _prompts = _load_prompts()
        self._system_prompt: str = _prompts["system"]["content"]
        self._user_template: str = _prompts["user"]["template"]

    def analyze(self, ticket: Mapping[str, object], provider: str) -> TicketAnalysisResult:
        ticket_str = "\n".join(f"{k}: {v}" for k, v in ticket.items())
        prompt = self._user_template.format(ticket_str=ticket_str)

        if provider == "openai":
            result_dict = self._analyze_openai(prompt)
        elif provider == "groq":
            result_dict = self._analyze_groq(prompt)
        elif provider == "gemini":
            result_dict = self._analyze_gemini(prompt)
        else:
            raise ValueError(f"Provider {provider} not implemented.")

        return TicketAnalysisResult(
            category=result_dict.get("category", "Desconhecida"),
            sentiment=result_dict.get("sentiment", "Neutro"),
            priority_suggestion=result_dict.get("priority_suggestion", "Media"),
            priority_reason=result_dict.get("priority_reason", "Não especificado"),
            summary=result_dict.get("summary", "Sem resumo"),
            sla_risk=result_dict.get("sla_risk", "Baixo"),
        )

    def _parse_json(self, content: str) -> dict:
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(f"LLM returned invalid JSON: {content!r}") from exc

    def _analyze_openai_compatible(self, client: object, prompt: str) -> dict:
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.0,
        )
        content = response.choices[0].message.content
        if not content:
            raise ValueError("LLM returned empty response")
        return self._parse_json(content)

    def _analyze_openai(self, prompt: str) -> dict:
        from openai import OpenAI

        return self._analyze_openai_compatible(OpenAI(api_key=self.api_key), prompt)

    def _analyze_groq(self, prompt: str) -> dict:
        from groq import Groq

        return self._analyze_openai_compatible(Groq(api_key=self.api_key), prompt)

    def _analyze_gemini(self, prompt: str) -> dict:
        import google.generativeai as genai

        genai.configure(api_key=self.api_key)
        model_instance = genai.GenerativeModel(
            self.model,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", temperature=0.0
            ),
        )
        combined_prompt = f"{self._system_prompt}\n\n{prompt}"
        response = model_instance.generate_content(combined_prompt)
        content = response.text
        if not content:
            raise ValueError("LLM returned empty response")
        return self._parse_json(content)
