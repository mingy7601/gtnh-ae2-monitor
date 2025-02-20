
import streamlit as st
#from streamlit_autorefresh import st_autorefresh
from st_supabase_connection import SupabaseConnection, execute_query
import plotly.express as px
import pandas as pd
import datetime
import time

st.set_page_config(
  page_title = 'GTNH - Items Tracker',
  layout='wide'
)

st.title("GTNH - Applied Energistics Items Track")

supabase_table = "items_ae2"

#count = st_autorefresh(interval=5000, limit=100, key="fizzbuzzcounter")

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

# Filter last items from the last 4 days
filter = datetime.datetime.today() - datetime.timedelta(days=4)

# Perform query from supabase
rows = execute_query(conn.table(supabase_table).select("*").filter(("datetime"),"gt",filter), ttl='20m')

# Get the list os items
items = execute_query(conn.table(supabase_table).select("item"), ttl='10m')
items = pd.DataFrame.from_dict(items.data)
distinct_items = items.item.unique()

# Select Box to filter a item
items_filter = st.selectbox("Select the Item", distinct_items)

# Creating a single-element container.
placeholder = st.empty()

# Update the dash every 15 minutes
for seconds in range(200):

  rows = execute_query(conn.table(supabase_table).select("*").filter(("datetime"),"gt",filter), ttl='20m')
  #st.write(distinct_items)

  sort_table = pd.DataFrame.from_dict(rows.data).sort_values('datetime')

  fig_col1, fig_col2 = st.columns([0.2, 0.8])
  with fig_col1:
    st.markdown("### "+items_filter)

    st.markdown("#### Past 24-hour metrics")
    item_track = sort_table.loc[sort_table['item'] == items_filter]
    item_track['datetime'] = pd.to_datetime(item_track["datetime"])
    last_24h = item_track[item_track["datetime"] >= pd.Timestamp.now() - pd.Timedelta(days=1)]
    
    avg_df = last_24h[["datetime", "quantity"]].copy()
    avg_df.set_index("datetime", inplace=True)
    

    kpi_avg = avg_df.resample("H").mean().round(0).astype(int)
    st.metric(label="Average Produced", value="{:,}".format(kpi_avg))

    kpi_change = (last_24h['quantity'].iloc[-1] - last_24h['quantity'].iloc[0]).round(0).astype(int)
    st.metric(label="Total Amount Produced", value="{:,}".format(kpi_change))




  with fig_col2:
    fig1 = px.line(item_track, x='datetime', y='quantity', title='Quantity of: ' + items_filter)
    st.write(fig1)

  with st.expander("All items:"):

    for col in distinct_items:
      temp_df = sort_table.loc[sort_table['item'] == col]
      
      fig = px.line(temp_df, x='datetime', y='quantity', title='Quantity of: ' + col)
      
      st.write(fig)

  time.sleep(5)

