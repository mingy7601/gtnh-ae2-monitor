
import streamlit as st
#from streamlit_autorefresh import st_autorefresh
from st_supabase_connection import SupabaseConnection, execute_query
import plotly.express as px
import pandas as pd
import datetime
import time
import pytz

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

# Get the list os items
items = execute_query(conn.table(supabase_table).select("item").filter(("datetime"),"gt",filter), ttl='20m')
items = pd.DataFrame.from_dict(items.data)
distinct_items = items.item.unique()

# Select Box to filter a item
items_filter = st.selectbox("Select the Item", distinct_items)

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
    last_24h = item_track[item_track["datetime"] >= datetime.datetime.now(pytz.timezone("America/Sao_Paulo")) - pd.Timedelta(days=1)]

    if len(last_24h) <= 1:
      kpi_avg = 0
      kpi_change = 0
    else:
      last_24h["real_production"] = last_24h["quantity"].diff().fillna(0)
      total_production = last_24h["real_production"].sum()
      total_hours = (last_24h["datetime"].max() - last_24h["datetime"].min()).total_seconds() / 3600
      st.write(last_24h["datetime"].max())
      st.write(last_24h["datetime"].min())
      kpi_avg = (total_production / total_hours).round(0).astype(int)

      kpi_change = total_production.round(0).astype(int) 
    
    st.metric(label="Average Produced per Hour", value="{:,}".format(kpi_avg))
    st.metric(label="Total Amount Produced", value="{:,}".format(kpi_change))

  with fig_col2:
    fig1 = px.line(item_track, x='datetime', y='quantity', title='Quantity of: ' + items_filter)
    st.write(fig1)


  time.sleep(5)

