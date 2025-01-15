
import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query
import plotly.express as px

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

# Perform query.
rows = execute_query(conn.table("items_ae2").select("*"), ttl=10)

# Print results.
st.title("GTNH - Applied Energistics Items Track")

#st.write(type(rows))

fig = px.line(rows.data, x='item', y='quantity')

st.write(fig)



