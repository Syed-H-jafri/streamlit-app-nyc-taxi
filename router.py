import os
from groq import Groq
from dotenv import load_dotenv
from text_to_sql import ask as ask_sql
from rag import ask_rag

load_dotenv()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def classify_question(question):
    """Classify question as DATA or KNOWLEDGE"""

    prompt = """You are a question classifier for a NYC Taxi analytics system.

Classify the question as either:
- DATA: requires running a SQL query to get numbers/statistics
- KNOWLEDGE: requires explanation or background information

DATA questions examples:
- "What is the average fare?"
- "How many trips were there?"
- "What is total revenue?"
- "Count trips by payment type"

KNOWLEDGE questions examples:
- "Why do cash riders pay more?"
- "How are fares calculated?"
- "What time are taxis busiest?"
- "Explain the payment patterns"

Respond with ONLY one word: DATA or KNOWLEDGE"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"Classify this question: {question}"
            }
        ],
        temperature=0
    )

    classification = response.choices[0].message.content.strip().upper()

    # Make sure response is valid
    if "DATA" in classification:
        return "DATA"
    else:
        return "KNOWLEDGE"

def route_question(question):
    """Route question to correct system"""
    print(f"\n{'='*50}")
    print(f"❓ Question: {question}")
    print(f"{'='*50}")

    # Classify question
    print("🤔 Classifying question...")
    classification = classify_question(question)
    print(f"📊 Classification: {classification}")

    # Route to correct system
    if classification == "DATA":
        print("🔢 Routing to Text-to-SQL...")
        print("-" * 50)
        ask_sql(question)
    else:
        print("📚 Routing to RAG Assistant...")
        print("-" * 50)
        ask_rag(question)

# Main program
if __name__ == "__main__":
    print("🚕 NYC Taxi AI Assistant")
    print("Powered by Text-to-SQL + RAG")
    print("=" * 50)

    # Test questions
    test_questions = [
        "What is the average fare amount?",
        "Why do cash riders pay more than credit card riders?",
        "How many trips were taken in total?",
        "How are NYC taxi fares calculated?",
        "What is the total revenue from credit card payments?",
        "What time of day are taxis busiest?"
    ]

    print("\n🧪 Running test questions...\n")
    for question in test_questions:
        route_question(question)
        print()

    # Interactive mode
    print("\n" + "="*50)
    print("💬 Interactive Mode!")
    print("="*50)

    while True:
        question = input("\n💬 Ask anything (or 'quit' to exit): ")
        if question.lower() == 'quit':
            break
        route_question(question)