import pandas as pd
import pyodbc
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime
import numpy as np

file = "cohort.xlsx"

### definitions
def load_data(file):
    df = pd.read_excel(file)
    df['date'] = pd.to_datetime(df['date'])
    return df

def load_cohort(df,date_start='',date_end='',groups=[]):
    if date_start:
        df = df.loc[df['date'].between(date_start,date_end)]
    if groups:
        df = df.loc[df['group'].isin(groups)]
    return df


def load_metrics(df,metric_map={}):
    if metric_map:
        for metric in metric_map.keys():
            exclude = df.loc[(df['metric']==metric) & ((df["value"]<metric_map[metric]['min']) | (df['value']>metric_map[metric]['max']))].index
            df = df.loc[~df.index.isin(exclude)]
    return df



### app


st.title("Cohort Analysis")
st.markdown("Filter your cohort, choose metrics and launch viz + ML.")



st.subheader("Select your cohort")

df_filter = pd.DataFrame({'date':[],'group':[]})
df_filter['date'] = pd.to_datetime(df_filter['date'])
if st.checkbox('Download data'):
    df_filter = load_data(file=file)

    #############
    ## Filters ##
    #############

    # date start, date end
    dates = pd.date_range(start=df_filter['date'].min(),end=df_filter['date'].max(),freq=df_filter['date'].dt.freq)
    date_start = (datetime.datetime.today()-datetime.timedelta(days=90)).strftime('%Y%m%d')
    date_end = datetime.datetime.today().strftime('%Y%m%d')
    date_start = st.sidebar.selectbox('Start date', dates,index=0)
    date_end = st.sidebar.selectbox('End date', dates,index=len(dates)-1)
    if date_start > date_end:
        temp = date_start
        date_start = date_end
        date_end = temp

    # cost center multiselect
    groups = []
    groups = st.sidebar.multiselect('Group selection', df_filter['group'].unique())

    # get cohort
    if st.checkbox('Get Cohort!'):
        df_filter = load_cohort(df_filter,date_start=date_start,date_end=date_end,groups=groups)


        #############
        ## Metrics ##
        #############
        metric_map = {}
        for metric in ['test','assignment','project']:
            st.markdown(metric+" filter")
            # tests
            min_range = np.arange(df_filter.loc[df_filter['metric']==metric,"value"].min(),df_filter.loc[df_filter['metric']==metric,"value"].mean(),1).astype(int)
            metric_min = st.selectbox("Minimum "+metric+" score",min_range,index=0)
            max_range = np.arange(df_filter.loc[df_filter['metric']==metric,"value"].mean(),df_filter.loc[df_filter['metric']==metric,"value"].max(),1).astype(int)
            metric_max = st.selectbox("Maximum "+metric+" score",max_range,index=len(max_range)-1)
            metric_map[metric] = {}
            metric_map[metric]['min'] = metric_min
            metric_map[metric]['max'] = metric_max
            # projects

        # assignments

        # get metrics
        if st.checkbox('Get metrics!'):
            df_filter = load_metrics(df_filter,metric_map=metric_map)


            #########
            ## Viz ##
            #########
            st.subheader("Student View")

            # patient journey
            if st.checkbox('Plot student journey'):
                dates = df_filter['date']
                for student,df_student in df_filter.groupby('id'):
                    metrics = df_student['metric'].unique()
                    fig = make_subplots(rows=len(metrics),cols=1,shared_xaxes=True,vertical_spacing=0.01)
                    for i,metric in enumerate(metrics):
                        df_metric = df_student.loc[df_student['metric']==metric]
                        trace = go.Scatter(x=df_metric['date'],y=[1]*len(df_metric.index),mode='markers')
                        fig.add_trace(trace,row=i+1,col=1)
                        fig.update_layout({'yaxis'+str(i+1):{'title':metric,'range':[0.5,1.5],'showticklabels':False},'xaxis'+str(i+1):{'range':[dates.min()-pd.Timedelta(days=2),dates.max()+pd.Timedelta(days=2)]}})
                    fig.update_layout(showlegend=False,title="student "+str(student))
                    st.plotly_chart(fig)

            # correlation with target

