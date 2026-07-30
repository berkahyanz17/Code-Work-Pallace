"""
generator.py
Takes a query + retrieved context chunks, builds a prompt, and calls the LLM.
"""

import config

SYSTEM_TEMPLATE = """You are a helpful assistant. Answer the user's question using ONLY
the context provided below. If the answer isn't in the context, say you don't know
instead of guessing.

Context:
{context}
"""


def build_prompt(query: str, context_chunks: list):
    context_text = "\n\n---\n\n".join(c["text"] for c in context_chunks)
    system_prompt = SYSTEM_TEMPLATE.format(context=context_text)
    return system_prompt, query


def generate(query: str, context_chunks: list) -> str:
    system_prompt, user_prompt = build_prompt(query, context_chunks)

    if config.GENERATION_PROVIDER == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=config.GEMINI_API_KEY)
        model = genai.GenerativeModel(
            config.GEMINI_GENERATION_MODEL,
            system_instruction=system_prompt,
        )
        response = model.generate_content(user_prompt)
        return response.text

    elif config.GENERATION_PROVIDER == "deepseek":
        # DeepSeek API is OpenAI-compatible
        from openai import OpenAI
        client = OpenAI(api_key=config.DEEPSEEK_API_KEY, base_url=config.DEEPSEEK_BASE_URL)
        response = client.chat.completions.create(
            model=config.DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content

    else:
        raise ValueError(f"Unknown GENERATION_PROVIDER: {config.GENERATION_PROVIDER}")
