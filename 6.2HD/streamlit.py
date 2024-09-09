import streamlit as st
import pandas as pd
import numpy as np
import asyncio
import os
st.title('Plotting data with Streamlit')


if os.path.exists('streamlit_data_file.csv'):
    df_sub = pd.read_csv('streamlit_data_file.csv')

df = pd.read_csv('data_file.csv')
df.drop(columns = ['id'], inplace = True)
df['timestamp'] = pd.to_datetime(df['timestamp'])

col11, col12 = st.columns(2)

with col11:
    check= st.checkbox('Use 2 variables (The scatter plot will be displayed)')

    if check:
        chart_type = st.selectbox('Select chart type'
                            , ['Line Graph', 'Bar Chart', 'Area Chart', 'Scatter Plot']
                            , placeholder='Select chart type')
        select_var_x = st.selectbox(
            "Select variables x",
            ("x", "y", "z")
        )
        x_axis = select_var_x
    else:
        chart_type = st.selectbox('Select chart type'
                            , ['Line Graph', 'Bar Chart', 'Area Chart']
                            , placeholder='Select chart type')
        x_axis = 'timestamp'

    select_var = st.multiselect(
        "Select variables y (x is timestamp) or y if you want to have optional y-axis",
        ["x", "y", "z"],
        ["x"],
    )
    y_axis = select_var

    if 'start_idx' not in st.session_state:
        st.session_state.start_idx = 0
    if 'end_idx' not in st.session_state:
        st.session_state.end_idx = 10

    n_samples = st.number_input("Enter the number of samples", min_value=1, max_value=len(df), value=10, key = 'n_samples')
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('Previous'):
            st.session_state.start_idx = max(0, st.session_state.start_idx - n_samples)
    with col2:
        if st.button('Next'):
            st.session_state.start_idx = min(len(df) - n_samples, st.session_state.start_idx + n_samples)
    with col3:
        if st.button('Reset'):
            st.session_state.start_idx = 0
            st.session_state.end_idx = 10
    # Calculate the end index
    st.session_state.end_idx = st.session_state.start_idx + n_samples

    # Ensure start_idx is within valid range after updating
    st.session_state.start_idx = max(0, min(st.session_state.start_idx, len(df) - n_samples))

   
    df_sub = df.iloc[st.session_state.start_idx:st.session_state.end_idx]
    max_samples = st.slider("The samples display", min_value=1, max_value=len(df), value= [st.session_state.start_idx,st.session_state.end_idx])
    st.session_state.start_idx = max_samples[0]
    st.session_state.end_idx = max_samples[1]
    df_prev = df_sub
    df_sub = df.iloc[max_samples[0]:max_samples[1]]

    timer_count = st.number_input("Enter the time for countdown", min_value=1, max_value=100, value=10, key = 'timer_count')

with col12:
    if chart_type == 'Line Graph':
        st.line_chart(df_sub, x= x_axis, y= y_axis)
    elif chart_type == 'Bar Chart':
        st.bar_chart(df_sub, x= x_axis, y= y_axis)
    elif chart_type == 'Area Chart':
        st.area_chart(df_sub, x= x_axis, y= y_axis)
    elif chart_type == 'Scatter Plot':
        st.warning('The plot will automatically choose the first variable from the mulitselect of y-axis.', icon="⚠️")
        st.scatter_chart(df_sub, x= x_axis, y= y_axis[0])
tab1, tab2, tab3 ,tab4, tab5 = st.tabs(["Mean", "Median", "Min", "Max", "Std"])
with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric(label = "Mean X compare to lastest dataset", value = df_sub.x.mean(), delta = df_sub.x.mean() - df_prev.x.mean())
    col2.metric(label = "Mean Y compare to lastest dataset", value = df_sub.y.mean(), delta = df_sub.y.mean() - df_prev.y.mean())
    col3.metric(label = "Mean Z compare to lastest dataset", value = df_sub.z.mean(), delta = df_sub.z.mean() - df_prev.z.mean())
with tab2:
    col1, col2, col3 = st.columns(3)
    col1.metric(label = "Median X compare to lastest dataset", value = df_sub.x.median(), delta = df_sub.x.median() - df_prev.x.median())
    col2.metric(label = "Median Y compare to lastest dataset", value = df_sub.y.median(), delta = df_sub.y.median() - df_prev.y.median())
    col3.metric(label = "Median Z compare to lastest dataset", value = df_sub.z.median(), delta = df_sub.z.median() - df_prev.z.median())
with tab3:
    col1, col2, col3 = st.columns(3)
    col1.metric(label = "Min X compare to lastest dataset", value = df_sub.x.min(), delta = df_sub.x.min() - df_prev.x.min())
    col2.metric(label = "Min Y compare to lastest dataset", value = df_sub.y.min(), delta = df_sub.y.min() - df_prev.y.min())
    col3.metric(label = "Min Z compare to lastest dataset", value = df_sub.z.min(), delta = df_sub.z.min() - df_prev.z.min())
with tab4:
    col1, col2, col3 = st.columns(3)
    col1.metric(label = "Max X compare to lastest dataset", value = df_sub.x.max(), delta = df_sub.x.max() - df_prev.x.max())
    col2.metric(label = "Max Y compare to lastest dataset", value = df_sub.y.max(), delta = df_sub.y.max() - df_prev.y.max())
    col3.metric(label = "Max Z compare to lastest dataset", value = df_sub.z.max(), delta = df_sub.z.max() - df_prev.z.max())
with tab5:
    col1, col2, col3 = st.columns(3)
    col1.metric(label = "Std X compare to lastest dataset", value = df_sub.x.std(), delta = df_sub.x.std() - df_prev.x.std())
    col2.metric(label = "Std Y compare to lastest dataset", value = df_sub.y.std(), delta = df_sub.y.std() - df_prev.y.std())
    col3.metric(label = "Std Z compare to lastest dataset", value = df_sub.z.std(), delta = df_sub.z.std() - df_prev.z.std())

status = df_sub.drop(columns = "timestamp").describe()
st.table(status) 
async def countdown_timer(seconds):
    countdown_placeholder = st.empty()
    for i in range(seconds, 0, -1):
        countdown_placeholder.text(f"Time remaining: {i} seconds")
        await asyncio.sleep(1)
asyncio.run(countdown_timer(timer_count))       
df_sub.to_csv('streamlit_data_file.csv')

