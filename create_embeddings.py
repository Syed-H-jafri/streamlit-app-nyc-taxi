import os
from clickhouse_driver import Client
from sentence_transformers import SentenceTransformer
from documents import DOCUMENTS
from dotenv import load_dotenv


load_dotenv()

# Initialize ClickHouse client
ch_client = Client(
    host=os.getenv("CH_HOST"),
    port=int(os.getenv("CH_PORT", "9440")),
    user=os.getenv("CH_USER", "default"),
    password=os.getenv("CH_PASSWORD"),
    database='raw',
    secure=True
)

# Initialize embedding model
print("⏳ Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Model loaded!")

def setup_database():
    """Create the doc_chunks table"""
    print("⏳ Creating doc_chunks table...")

    # Create table
    ch_client.execute("""
        CREATE TABLE IF NOT EXISTS raw.doc_chunks (
            chunk_id    UInt64,
            title       String,
            chunk_text  String,
            embedding   Array(Float32)
        )
        ENGINE = MergeTree()
        ORDER BY chunk_id
    """)
    print("✅ Table created!")

def split_into_chunks(text, chunk_size=200):
    """Split text into smaller chunks"""
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0

    for word in words:
        current_chunk.append(word)
        current_size += 1
        if current_size >= chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_size = 0

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def create_and_store_embeddings():
    """Create embeddings for all documents"""
    print("\n⏳ Creating embeddings...")

    # Clear existing data
    ch_client.execute("TRUNCATE TABLE IF EXISTS raw.doc_chunks")

    chunk_id = 1
    all_rows = []

    for doc in DOCUMENTS:
        print(f"📄 Processing: {doc['title']}")

        # Split into chunks
        chunks = split_into_chunks(doc['content'])

        for chunk in chunks:
            # Create embedding
            embedding = model.encode(chunk).tolist()

            all_rows.append({
                'chunk_id': chunk_id,
                'title': doc['title'],
                'chunk_text': chunk,
                'embedding': embedding
            })
            chunk_id += 1

    # Insert all rows
    ch_client.execute(
        "INSERT INTO raw.doc_chunks VALUES",
        [{
            'chunk_id': row['chunk_id'],
            'title': row['title'],
            'chunk_text': row['chunk_text'],
            'embedding': row['embedding']
        } for row in all_rows]
    )

    print(f"\n✅ Created {len(all_rows)} chunks!")
    print(f"✅ Embeddings stored in ClickHouse!")

def verify():
    """Verify embeddings were stored"""
    count = ch_client.execute("SELECT count() FROM raw.doc_chunks")[0][0]
    print(f"\n✅ Total chunks in database: {count}")

    # Show sample
    samples = ch_client.execute(
        "SELECT chunk_id, title, substring(chunk_text, 1, 50) FROM raw.doc_chunks LIMIT 3"
    )
    print("\n📋 Sample chunks:")
    for row in samples:
        print(f"  ID: {row[0]} | Title: {row[1]} | Text: {row[2]}...")

if __name__ == "__main__":
    print("🚕 NYC Taxi Embeddings Creator")
    print("=" * 40)

    setup_database()
    create_and_store_embeddings()
    verify()

    print("\n🎉 Done! Ready for RAG!")