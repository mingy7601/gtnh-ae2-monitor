
import streamlit as st
#from streamlit_autorefresh import st_autorefresh
from st_supabase_connection import SupabaseConnection, execute_query
import plotly.express as px
import pandas as pd

st.set_page_config(
  page_title = 'GTNH - Items',
  layout='wide'
)

#count = st_autorefresh(interval=5000, limit=100, key="fizzbuzzcounter")

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

# Perform query.
rows = execute_query(conn.table("items_ae2").select("*").filter(("datetime"),"gt",'2025-01-19'))

st.title("GTNH - Applied Energistics Items Track")

items = execute_query(conn.table("items_ae2").select("item"), ttl='10m')

items = pd.DataFrame.from_dict(items.data)

distinct_items = items.item.unique()

#st.write(distinct_items)

sort_table = pd.DataFrame.from_dict(rows.data).sort_values('datetime')

#fig = px.line(sort_table, x='datetime', y='quantity', color='item')

#st.write(fig)

for col in distinct_items:
  temp_df = sort_table.loc[sort_table['item'] == col]
  
  fig = px.line(temp_df, x='datetime', y='quantity', title='Quantity of: ' + col)
  
  st.write(fig)



