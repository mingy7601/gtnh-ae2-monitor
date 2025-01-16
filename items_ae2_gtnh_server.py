
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from st_supabase_connection import SupabaseConnection, execute_query
import plotly.express as px
import pandas as pd

st.set_page_config(
  page_title = 'GTNH - Items',
  layout='wide'
)

count = st_autorefresh(interval=5000, limit=100, key="fizzbuzzcounter")

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

# Perform query.
rows = execute_query(conn.table("items_ae2").select("*"), ttl=100)

st.title("GTNH - Applied Energistics Items Track")

items = execute_query(conn.table("items_ae2").select("item"), ttl=100)

items = pd.DataFrame.from_dict(items.data)

distinct_items = items.item.unique()

#st.write(distinct_items)

df = pd.DataFrame.from_dict(rows.data)

for col in distinct_items:
  temp_df = df.loc[df['item'] == col]
  
  fig = px.line(temp_df, x='datetime', y='quantity', title='Quantity of: ' + col)
  
  st.write(fig)



