
import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query
import plotly.express as px

st.set_page_config(
  page_title = 'GTNH - Items',
  layout='wide'
)

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

# Perform query.
rows = execute_query(conn.table("items_ae2").select("*"), ttl=10)

st.title("GTNH - Applied Energistics Items Track")

distinct_items = []
for distinct in rows.data.distinct('item'):
    distinct_items.append(distinct)

st.write(distinct_items)

fig = px.line(rows.data, x='datetime', y='quantity', color='item')

st.write(fig)



