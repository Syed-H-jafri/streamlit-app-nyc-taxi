import os
from groq import Groq
from clickhouse_driver import Client
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# Initialize clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
ch_client = Client(
    host='localhost',
    port=9000,
    user='default',
    password='',
    database='raw'
)

# Load embedding model
print("⏳ Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Model ready!")

def similarity_search(question, top_k=3):
    """Find most relevant document chunks"""

    # Convert question to embedding
    question_embedding = model.encode(question).tolist()

    # Get all chunks from ClickHouse
    results = ch_client.execute("""
        SELECT
            chunk_id,
            title,
            chunk_text,
            embedding
        FROM raw.doc_chunks
    """)

    # Calculate similarity scores
    similarities = []
    for row in results:
        chunk_id = row[0]
        title = row[1]
        chunk_text = row[2]
        chunk_embedding = row[3]

        # Calculate cosine similarity
        similarity = cosine_similarity(
            question_embedding,
            chunk_embedding
        )

        similarities.append({
            'chunk_id': chunk_id,
            'title': title,
            'chunk_text': chunk_text,
            'similarity': similarity
        })

    # Sort by similarity
    similarities.sort(key=lambda x: x['similarity'], reverse=True)

    # Return top k results
    return similarities[:top_k]

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sum(a * a for a in vec1) ** 0.5
    magnitude2 = sum(b * b for b in vec2) ** 0.5

    if magnitude1 == 0 or magnitude2 == 0:
        return 0

    return dot_product / (magnitude1 * magnitude2)

def generate_answer(question, relevant_chunks):
    """Generate answer using retrieved chunks"""

    # Build context from chunks
    context = "\n\n".join([
        f"Document: {chunk['title']}\n{chunk['chunk_text']}"
        for chunk in relevant_chunks
    ])

    # Create prompt
    prompt = f"""You are an NYC Taxi data expert.
Use the following information to answer the question.
Base your answer ONLY on the provided context.

Context:
{context}

Question: {question}

Provide a clear and specific answer based on the context above."""

    # Generate answer
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    return response.choices[0].message.content

def ask_rag(question):
    """Main RAG function"""
    print(f"\n❓ Question: {question}")
    print("🔍 Searching relevant documents...")

    # Find relevant chunks
    relevant_chunks = similarity_search(question)

    print(f"📄 Found {len(relevant_chunks)} relevant chunks:")
    for chunk in relevant_chunks:
        print(f"   → {chunk['title']} (similarity: {chunk['similarity']:.3f})")

    print("\n⏳ Generating answer...")

    # Generate answer
    answer = generate_answer(question, relevant_chunks)

    print(f"\n✅ Answer:\n{answer}")

# Main program
if __name__ == "__main__":
    print("🚕 NYC Taxi RAG Assistant")
    print("=" * 40)

    while True:
        question = input("\n💬 Ask a question (or 'quit' to exit): ")
        if question.lower() == 'quit':
            break
        ask_rag(question)