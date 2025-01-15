
import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query

# Initialize connection.
#conn = st.connection("supabase",type=SupabaseConnection)

st_supabase_client = st.connection(
    name="YOUR_CONNECTION_NAME",
    type=SupabaseConnection,
    ttl=None,
)

# Perform query.
rows = execute_query(st_supabase_client.table("items_ae2").select("*"), ttl=0)

# Print results.
for row in rows.data:
    st.write(f"{row['item']} has a :{row['quantity']}:")



