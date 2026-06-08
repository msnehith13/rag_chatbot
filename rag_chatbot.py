import openai
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from extract_pdf import extract_text_from_pdf

openai.api_key = "YOUR_API_KEY"

model = SentenceTransformer("all-MiniLM-L6-v2")

text = extract_text_from_pdf("data/capitals.pdf")
chunks = text.split("\n")

embeddings = model.encode(chunks)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))


def retrieve_context(query):

    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, k=3)

    context = ""
    for idx in indices[0]:
        context += chunks[idx] + "\n"

    return context


def ask_chatgpt(context, question):

    prompt = f"""
Context:
{context}

Question:
{question}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content']


while True:

    question = input("==> ")

    if question.lower() == "q":
        break

    context = retrieve_context(question)

    answer = ask_chatgpt(context, question)

    print("\nResponse:\n")
    print(answer)
    print("\n----------")