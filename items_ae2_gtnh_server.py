import streamlit as st
from streamlit_autorefresh import st_autorefresh
from st_supabase_connection import SupabaseConnection
from st_supabase_connection import execute_query
import plotly.express as px
import pandas as pd
import tomllib
import datetime
import time
import pytz

with open("./.streamlit/secrets.toml", "rb") as f:
    config = tomllib.load(f)

supabase_url = config["connections"]["supabase"]["SUPABASE_URL"]
supabase_key = config["connections"]["supabase"]["SUPABASE_KEY"]

filter = datetime.datetime.today() - datetime.timedelta(days= 4)

st.set_page_config(
  page_title = 'GTNH - Items Tracker',
  layout='wide'
)

st.title("GTNH - Applied Energistics Items Track")

# Supabase Table
# supabase_table = "gtnh-items"
st_supabase = st.connection(
    name="supabase_connection", 
    type=SupabaseConnection, 
    ttl=None,
    url=supabase_url, 
    key=supabase_key, 
)

items = execute_query(st_supabase.table("gtnh-items").select("*", count="None"), ttl=None)

items = pd.DataFrame.from_dict(items.data)
distinct_items = items.item.unique()

# Select Box to filter a item
items_filter = st.selectbox("Select the Item", distinct_items)

# Connection with supabase
rows = execute_query(st_supabase.table("gtnh-items").select("*").filter(("datetime"),"gt",filter), ttl='20m')

# Convert to DataFrame and Sort the table
sort_table = pd.DataFrame.from_dict(rows.data).sort_values('datetime')

# Chart for Item
fig_col1, fig_col2 = st.columns([0.2, 0.8])
with fig_col1:
  st.markdown("### "+items_filter)

  st.markdown("#### Past 24-hour metrics")

  item_track = sort_table.loc[sort_table['item'] == items_filter]
  item_track['datetime'] = pd.to_datetime(item_track["datetime"])
  now = pd.Timestamp.now(tz="America/Sao_Paulo")
  now = now.tz_localize(None)
  last_24h = item_track[item_track["datetime"] >= now - pd.Timedelta(days=1)]

  if len(last_24h) <= 1:
    kpi_avg = 0
    kpi_change = 0
  else:
    last_24h["real_production"] = last_24h["quantity"].diff().fillna(0)
    total_production = last_24h["real_production"].sum()
    total_hours = (last_24h["datetime"].max() - last_24h["datetime"].min()).total_seconds() / 3600
    kpi_avg = (total_production / total_hours).round(0).astype(int)

    kpi_change = total_production.round(0).astype(int) 
  
  st.metric(label="Average Produced per Hour", value="{:,}".format(kpi_avg))
  st.metric(label="Total Amount Produced", value="{:,}".format(kpi_change))

with fig_col2:
  fig1 = px.line(item_track, x='datetime', y='quantity', title='Quantity of: ' + items_filter)
  st.write(fig1, key='fig1')


# Expander with all items
with st.expander("All items:"):
  for col in distinct_items:
    temp_df = sort_table.loc[sort_table['item'] == col]
    
    fig = px.line(temp_df, x='datetime', y='quantity', title='Quantity of: ' + col)
    
    st.write(fig)