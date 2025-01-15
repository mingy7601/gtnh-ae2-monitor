
import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query
import plotly.express as px
import pandas as pd

st.set_page_config(
  page_title = 'GTNH - Items',
  layout='wide'
)

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

# Perform query.
rows = execute_query(conn.table("items_ae2").select("*"), ttl=10)

st.title("GTNH - Applied Energistics Items Track")

items = execute_query(conn.table("items_ae2").select("item"), ttl=10)

items = pd.DataFrame.from_dict(items.data)

distinct_items = items.item.unique()

#st.write(distinct_items)

df = pd.DataFrame.from_dict(rows.data)

for col in distinct_items:
  temp_df = df.loc[df['item'] == col]
  
  fig = px.line(temp_df, x='datetime', y='quantity', title='Quantity of: ' + col)
  
  st.write(fig)



