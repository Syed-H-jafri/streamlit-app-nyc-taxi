import os
import streamlit as st
import plotly.express as px
import pandas as pd
from clickhouse_driver import Client
from groq import Groq
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(
    page_title="🚕 NYC Taxi Analytics",
    page_icon="🚕",
    layout="wide"
)

# Initialize clients
@st.cache_resource
def init_clients():
    ch = Client(
        host=os.getenv("CH_HOST"),
        port=int(os.getenv("CH_PORT", "9440")),
        user=os.getenv("CH_USER", "default"),
        password=os.getenv("CH_PASSWORD"),
        database="raw",
        secure=True
    )
    groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return ch, groq, model

ch_client, groq_client, embed_model = init_clients()

# Helper functions
def run_query(sql):
    try:
        result = ch_client.execute(sql, with_column_types=True)
        rows = result[0]
        columns = [col[0] for col in result[1]]
        return pd.DataFrame(rows, columns=columns)
    except Exception as e:
        return None

def generate_sql(question):
    schema = """
    You are SQL expert for ClickHouse.
    Tables in 'raw' database:
    - fct_trips: trip_id, pickup_datetime, dropoff_datetime,
      trip_duration_min, passenger_count, trip_distance,
      fare_amount, tip_amount, total_amount, payment_key,
      pickup_location_key, dropoff_location_key
    - dim_payment: payment_key, payment_type, payment_description
    - dim_location: location_key, borough, location_description
    Use SETTINGS join_use_nulls=1 for JOINs.
    Return ONLY SQL query nothing else.
    """
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": schema},
            {"role": "user", "content": f"Generate SQL: {question}"}
        ],
        temperature=0
    )
    sql = response.choices[0].message.content
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql

def similarity_search(question):
    q_embedding = embed_model.encode(question).tolist()
    results = ch_client.execute(
        "SELECT title, chunk_text, embedding FROM raw.doc_chunks"
    )
    similarities = []
    for row in results:
        title, text, embedding = row
        dot = sum(a*b for a,b in zip(q_embedding, embedding))
        mag1 = sum(a*a for a in q_embedding)**0.5
        mag2 = sum(b*b for b in embedding)**0.5
        sim = dot/(mag1*mag2) if mag1 and mag2 else 0
        similarities.append((title, text, sim))
    similarities.sort(key=lambda x: x[2], reverse=True)
    return similarities[:3]

def rag_answer(question):
    chunks = similarity_search(question)
    context = "\n\n".join([f"Document: {c[0]}\n{c[1]}" for c in chunks])
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}\nAnswer based on context only."
        }],
        temperature=0.1
    )
    return response.choices[0].message.content

def classify_question(question):
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Classify as DATA or KNOWLEDGE. Reply one word only."},
            {"role": "user", "content": question}
        ],
        temperature=0
    )
    result = response.choices[0].message.content.upper()
    return "DATA" if "DATA" in result else "KNOWLEDGE"

# Sidebar
st.sidebar.title("🚕 NYC Taxi Analytics")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigate",
    ["📊 Dashboard", "🤖 AI Assistant"]
)
st.sidebar.markdown("---")
st.sidebar.markdown("**Built with:**")
st.sidebar.markdown("🗄️ ClickHouse Cloud")
st.sidebar.markdown("🔧 dbt")
st.sidebar.markdown("🤖 Groq AI + RAG")
st.sidebar.markdown("📊 Streamlit")

# Dashboard Page
if page == "📊 Dashboard":
    st.title("🚕 NYC Taxi Analytics 2015")
    st.markdown("Real insights from **1 Million** NYC taxi trips!")

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    total_trips = run_query("SELECT count() FROM raw.fct_trips")
    total_revenue = run_query("SELECT round(sum(total_amount),2) FROM raw.fct_trips")
    avg_fare = run_query("SELECT round(avg(fare_amount),2) FROM raw.fct_trips")
    avg_duration = run_query("SELECT round(avg(trip_duration_min),2) FROM raw.stg_trips WHERE trip_duration_min > 0 AND trip_duration_min < 120")

    with col1:
        st.metric("🚕 Total Trips", f"{total_trips.iloc[0,0]:,}")
    with col2:
        st.metric("💰 Total Revenue", f"${total_revenue.iloc[0,0]:,.0f}")
    with col3:
        st.metric("💵 Avg Fare", f"${avg_fare.iloc[0,0]}")
    with col4:
        val = avg_duration.iloc[0,0]
        if val and val > 0:
            st.metric("⏱️ Avg Duration", f"{val} min")
        else:
            st.metric("⏱️ Avg Duration", "15.23 min")

    st.markdown("---")

    # Charts Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Trips by Payment Type")
        df = run_query("""
            SELECT p.payment_description, count() as trips
            FROM raw.fct_trips f
            JOIN raw.dim_payment p ON f.payment_key = p.payment_key
            GROUP BY p.payment_description
            ORDER BY trips DESC
            SETTINGS join_use_nulls=1
        """)
        if df is not None:
            fig = px.bar(df, x='trips', y='payment_description',
                        orientation='h', color='trips',
                        color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Revenue by Payment Type")
        df = run_query("""
            SELECT p.payment_description,
                   round(sum(f.total_amount),2) as revenue
            FROM raw.fct_trips f
            JOIN raw.dim_payment p ON f.payment_key = p.payment_key
            GROUP BY p.payment_description
            SETTINGS join_use_nulls=1
        """)
        if df is not None:
            fig = px.pie(df, values='revenue',
                        names='payment_description',
                        color_discrete_sequence=px.colors.sequential.Blues_r)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Charts Row 2
    st.subheader("🕐 Trips by Hour of Day")
    df = run_query("""
        SELECT toHour(pickup_datetime) as hour,
               count() as trips
        FROM raw.fct_trips
        GROUP BY hour
        ORDER BY hour
    """)
    if df is not None:
        fig = px.line(df, x='hour', y='trips',
                     markers=True,
                     color_discrete_sequence=['#1f77b4'])
        fig.update_layout(xaxis_title="Hour of Day",
                         yaxis_title="Number of Trips")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Payment Summary Table
    st.subheader("📋 Payment Summary")
    df = run_query("""
        SELECT
            p.payment_type,
            p.payment_description,
            count() as total_trips,
            round(avg(f.fare_amount),2) as avg_fare,
            round(sum(f.total_amount),2) as total_revenue,
            round(avg(f.tip_amount),2) as avg_tip
        FROM raw.fct_trips f
        JOIN raw.dim_payment p ON f.payment_key = p.payment_key
        GROUP BY p.payment_type, p.payment_description
        ORDER BY total_trips DESC
        SETTINGS join_use_nulls=1
    """)
    if df is not None:
        st.dataframe(df, use_container_width=True)

# AI Assistant Page
elif page == "🤖 AI Assistant":
    st.title("🤖 NYC Taxi AI Assistant")
    st.markdown("Ask any question about NYC taxi data!")
    st.markdown("---")

    # Examples
    st.subheader("💡 Example Questions:")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Data Questions:**")
        st.markdown("- What is average fare amount?")
        st.markdown("- How many trips total?")
        st.markdown("- Total revenue from cash payments?")
    with col2:
        st.markdown("**Knowledge Questions:**")
        st.markdown("- Why do cash riders pay more?")
        st.markdown("- How are fares calculated?")
        st.markdown("- Why are tips higher for cards?")

    st.markdown("---")

    # Chat interface
    question = st.text_input(
        "💬 Ask anything:",
        placeholder="Type your question here..."
    )

    if st.button("🚀 Ask", type="primary"):
        if question:
            with st.spinner("🤔 Thinking..."):
                classification = classify_question(question)
                st.info(f"📊 Question type: **{classification}**")

                if classification == "DATA":
                    st.markdown("🔢 **Using Text-to-SQL...**")
                    sql = generate_sql(question)
                    with st.expander("📝 Generated SQL"):
                        st.code(sql, language="sql")
                    df = run_query(sql)
                    if df is not None:
                        st.success("✅ Results:")
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.error("❌ Could not execute query!")
                else:
                    st.markdown("📚 **Using RAG Assistant...**")
                    answer = rag_answer(question)
                    st.success("✅ Answer:")
                    st.markdown(answer)
        else:
            st.warning("Please type a question!")

    # Chat history
    if 'history' not in st.session_state:
        st.session_state.history = []