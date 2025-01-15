
import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query
import plotly.express as px

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

# Perform query.
rows = execute_query(conn.table("items_ae2").select("*"), ttl=10)

st.set_page_config(
  page_title = 'GTNH - Items',
  layout='wide'
)

st.title("GTNH - Applied Energistics Items Track")

distinct_items = execute_query(conn.table("items_ae2").selectdistinct("items"), ttl=10)

st.write(distinct_items)

fig = px.line(rows.data, x='datetime', y='quantity', color='item')

st.write(fig)



