import sys
import os
import time
import json
import warnings
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.callbacks import get_openai_callback
from pydantic import BaseModel, Field
from typing import List
try:
    from .safety import sanitize_input, moderate_output
except ImportError:
    from safety import sanitize_input, moderate_output

load_dotenv()

warnings.filterwarnings(
    "ignore",
    message=r"Pydantic serializer warnings:.*",
    category=UserWarning,
    module=r"pydantic\.main",
)

class Response(BaseModel):
    answer: str = Field(description="Respuesta concisa al usuario")
    confidence: float = Field(description="Nivel de confianza de 0 a 1")
    actions: List[str] = Field(description="Lista de acciones recomendadas")


def load_prompt():
    prompt_path = Path(__file__).parent.parent / "prompts" / "main_prompt.md"
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()
    
system_message = load_prompt()
prompt=ChatPromptTemplate([
      ("system", system_message),
      ("human", "{query}"),
])

llm=ChatOpenAI(model="gpt-4o-mini", 
               temperature=0.000003,
               stream_usage=True
               )



def get_response(query: str) -> Response:
    query = sanitize_input(query)
    structured_llm = llm.with_structured_output(Response)
    chain= prompt | structured_llm
    start_time = time.time()


    with get_openai_callback() as cb:
        ai_response = chain.invoke({"query": query})
        ai_response.answer = moderate_output(ai_response.answer)
        latency = int((time.time() - start_time) * 1000)
        
        metrics = {
            "tokens": {
                "prompt": cb.prompt_tokens,
                "completion": cb.completion_tokens,
                "total": cb.total_tokens
            },
            "latency_ms": latency,
            "estimated_cost_usd": cb.total_cost
        }
    return ai_response, metrics


def save_metrics(final_data: dict):
    metrics_path = Path(__file__).parent.parent / "metrics" / "metrics.json"
    metrics_path.parent.mkdir(exist_ok=True)

    history = []
    if metrics_path.exists():
        with open(metrics_path, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []

    history.append(final_data)
    
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(history, indent=2, ensure_ascii=False, fp=f)


def main():
    if len(sys.argv) < 2:
        print("Escribe tu consulta entre comillas")
        sys.exit(1)

    query = sys.argv[1]

    try:
        response_obj, metrics = get_response(query)

        final_output = {
            "response": response_obj.model_dump(),
            "metrics": metrics
        }
        save_metrics(final_output)

        print(json.dumps(final_output, indent=2, ensure_ascii=False))

    except ValueError as e:
        print(json.dumps({"action": "bloquear", "reason": str(e)}, indent=2))

if __name__ == "__main__":
    main()