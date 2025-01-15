
import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

# Perform query.
rows = execute_query(conn.table("test").select("*"), ttl=10)

# Print results.

st.write('Dashboard working')

st.write(conn)

st.write(rows)

for row in rows.data:
    st.write(f"{row['item']} has a :{row['quantity']}:")



