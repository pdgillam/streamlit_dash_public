import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from data.fake_data import get_sample, generate_fake_data
from components.ui import df_to_csv_bytes, filter_df, load_data_cached, try_show_aggrid
from components.plots import line_chart_plotly, bar_chart_plotly, scatter_altair


st.set_page_config(page_title='Dashboard Template', layout='wide')

st.title('Streamlit Dashboard Template')

# Sidebar controls
st.sidebar.header('Controls')
rows = st.sidebar.slider('Rows to generate', min_value=50, max_value=5000, value=500, step=50)
start_date = st.sidebar.date_input('Start date', value=(datetime.utcnow() - timedelta(days=30)).date())
end_date = st.sidebar.date_input('End date', value=datetime.utcnow().date())
categories = st.sidebar.multiselect('Categories', options=['A', 'B', 'C'], default=['A', 'B', 'C'])
text_search = st.sidebar.text_input('Search text')

# Load data (cached via helper)
with st.spinner('Generating data...'):
    df = load_data_cached(generate_fake_data, n=rows, start_date=pd.to_datetime(start_date), end_date=pd.to_datetime(end_date), seed=42)

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric('Rows', len(df))
col2.metric('Avg value', f"{df['value'].mean():.2f}")
col3.metric('Avg score', f"{df['score'].mean():.3f}")
col4.metric('Open %', f"{(df['status'] == 'open').mean() * 100:.1f}%")

# Filtering
filtered = filter_df(df, categories=categories, start_date=start_date, end_date=end_date, text_search=text_search)

st.markdown('## Charts')
left, right = st.columns([2, 1])
with left:
    st.plotly_chart(line_chart_plotly(filtered), use_container_width=True)
    st.plotly_chart(bar_chart_plotly(filtered), use_container_width=True)
with right:
    st.altair_chart(scatter_altair(filtered), use_container_width=True)

st.markdown('## Data')
# Try AgGrid (if installed) for interactive selection; otherwise fall back to st.dataframe.
selected = try_show_aggrid(filtered.reset_index(drop=True), height=400)
if selected is not None:
    st.markdown('### Selected row')
    st.write(selected)
else:
    st.write('No row selected (AgGrid not available or no selection)')

# Downloads
csv_bytes = df_to_csv_bytes(filtered)
st.download_button('Download CSV', data=csv_bytes, file_name='data.csv', mime='text/csv')

st.markdown('---')
st.caption('Template created for demo purposes. Customize components/ and data/ for your use case.')

