import os
from groq import Groq
from clickhouse_driver import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("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"))

# Initialize ClickHouse client
ch_client = Client(
    host='localhost',
    port=9000,
    user='default',
    password='',
    database='raw'
)

# Our schema information
SCHEMA = """
You are a SQL expert for ClickHouse database.
The database is called 'raw' and contains these tables:

1. fct_trips - Main fact table with 993,708 NYC taxi trips
   Columns:
   - trip_id: unique trip identifier
   - pickup_datetime: when trip started
   - dropoff_datetime: when trip ended
   - trip_duration_min: duration in minutes
   - passenger_count: number of passengers
   - trip_distance: distance in miles
   - fare_amount: base fare in dollars
   - tip_amount: tip in dollars
   - total_amount: total charged in dollars
   - payment_key: foreign key to dim_payment
   - pickup_location_key: foreign key to dim_location
   - dropoff_location_key: foreign key to dim_location

2. dim_payment - Payment type dimension (4 rows)
   Columns:
   - payment_key: unique key
   - payment_type: CSH, CRE, NOC, DIS
   - payment_description: Cash payment, Credit card payment, etc

3. dim_location - NYC borough dimension (5 rows)
   Columns:
   - location_key: unique key
   - borough: Manhattan, Brooklyn, Queens, Bronx, Staten Island
   - location_description: borough description

Important ClickHouse rules:
- Use SETTINGS join_use_nulls = 1 for JOIN queries
- Use single quotes for strings
- Always prefix table with database: raw.fct_trips

Generate ONLY the SQL query, no explanation.
"""

def generate_sql(question):
    """Convert natural language question to SQL"""
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": SCHEMA
            },
            {
                "role": "user",
                "content": f"Generate SQL for: {question}"
            }
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()

def run_query(sql):
    """Run SQL query against ClickHouse"""
    try:
        # Clean SQL - remove markdown if present
        sql = sql.replace("```sql", "").replace("```", "").strip()
        result = ch_client.execute(sql, with_column_types=True)
        rows = result[0]
        columns = [col[0] for col in result[1]]
        return columns, rows
    except Exception as e:
        return None, str(e)

def ask(question):
    """Main function - ask a question get an answer"""
    print(f"\n❓ Question: {question}")
    print("⏳ Generating SQL...")

    # Generate SQL
    sql = generate_sql(question)
    print(f"\n📝 Generated SQL:\n{sql}")

    # Run query
    print("\n⚡ Running query...")
    columns, rows = run_query(sql)

    if columns is None:
        print(f"❌ Error: {rows}")
    else:
        print(f"\n✅ Results:")
        print(" | ".join(columns))
        print("-" * 50)
        for row in rows[:10]:
            print(" | ".join(str(v) for v in row))
        if len(rows) > 10:
            print(f"... and {len(rows) - 10} more rows")

# Main program
if __name__ == "__main__":
    print("🚕 NYC Taxi Text-to-SQL Assistant")
    print("=" * 40)

    while True:
        question = input("\n💬 Ask a question (or 'quit' to exit): ")
        if question.lower() == 'quit':
            break
        ask(question)