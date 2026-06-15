import os
from dotenv import load_dotenv
from groq import Groq
import gradio as gr
from retrieve import build_vector_store, retrieve

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
collection, model = build_vector_store()

def ask(question):
    results = retrieve(question, collection, model, k=5)
    
    context_parts = []
    sources = []
    for chunk, metadata, distance in results:
        context_parts.append(f"[Source: {metadata['source']}]\n{chunk}")
        if metadata['source'] not in sources:
            sources.append(metadata['source'])
    
    context = "\n\n".join(context_parts)
    
    system_prompt = """You are a helpful guide for Computer Science students at Queens College, CUNY.
Answer questions using ONLY the information provided in the context below.
If the context does not contain enough information to answer the question, say exactly:
"I don't have enough information on that in my documents."
Do not use any outside knowledge. Always cite which source document your answer comes from."""

    user_prompt = f"""Context:
{context}

Question: {question}

Answer based only on the context above, and cite your sources."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    answer = response.choices[0].message.content
    return {"answer": answer, "sources": sources}


def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="QC CS Unofficial Guide") as demo:
    gr.Markdown("# 🎓 Queens College CS Unofficial Guide")
    gr.Markdown("Ask anything about CS courses, professors, and degree requirements at QC.")
    
    inp = gr.Textbox(label="Your question", placeholder="e.g. What do students say about Professor Goswami?")
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)
    
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()