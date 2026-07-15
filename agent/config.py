import re
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

BASE_URL = "http://localhost:8000/v1"
MODEL = "Qwen/Qwen3.6-35B-A3B-Instruct-FP8"

_llm = ChatOpenAI(base_url=BASE_URL, api_key="none", model=MODEL,
                  temperature=0.2, max_tokens=1000,
                  extra_body={"chat_template_kwargs": {"enable_thinking": False}})

class _CleanLLM:
    """Strips Qwen's <think> reasoning so .content is only the real answer."""
    def invoke(self, prompt):
        r = _llm.invoke(prompt)
        r.content = re.sub(r"^.*?</think>\s*", "", r.content, flags=re.S).strip()
        return r

llm = _CleanLLM()
emb = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")