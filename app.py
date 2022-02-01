import os, sys, pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sympy import plot
import xlrd as xl
import altair as alt
excelfiles = []
wells = []
well_names = []
#Get Current Path
file_path = os.getcwd()
#read excel filesimport os, sys, pandas as pd
from unicodedata import name
import streamlit as st,numpy as np
excelfiles = []
wells = []
well_names = []
#read excel files
for fil in os.listdir(file_path):
    if 'xlsx' not in fil:
        continue
    excelfiles.append(fil)
#open and read excel files
st.header("SPE Dataset Dashboard 2022")
file_factor = len(excelfiles)/100
count_files = 0
progress_bar = st.progress(0)
@st.cache(suppress_st_warning=True)
def read_headers():
    for file_name in excelfiles:
        ind = excelfiles.index(file_name)
        if 'xlsx' not in file_name :
            continue
        progress_bar.progress(int(ind/file_factor))
        st.write(os.path.join(file_path ,file_name))
        xls = pd.ExcelFile(os.path.join(file_path ,file_name))
        df = pd.read_excel(xls,sheet_name="Well Data",header=None)
        df_proddata = pd.DataFrame( pd.read_excel(xls,sheet_name='Production Data')).drop(0)
        well =str(df.iloc[1][1])+' '+str(df.iloc[2][1]) 
        well_names.append(well)
        st.session_state[well] = df_proddata
    st.write('Created side bar, Well Count', len(well_names))
    st.session_state.wells = well_names
read_headers()
if st.session_state.wells is not None:
    print(len(st.session_state.wells))
    sidebar = st.sidebar.radio(options=st.session_state.wells,label="Select A Well")
elif st.session_state.wells is None:
    st.session_state.wells = []
if sidebar is not None:
    st.subheader("Current Well  :"+ sidebar)
left_col,right_column = st.columns(2)

if sidebar is not None:
    if st.session_state[sidebar] is not None:
         df = pd.DataFrame(st.session_state[sidebar])
         df.set_index('Time (Days)')
         with left_col:
             selectbox1 = st.selectbox(options=pd.DataFrame(st.session_state[sidebar]).columns,label='Variable 1')
             left_col.line_chart(df[selectbox1])
             selectbox2 = st.selectbox(options=pd.DataFrame(st.session_state[sidebar]).columns,label='Variable 2')
             left_col.area_chart(df[selectbox2])   
         with right_column:
             selectbox3 = st.selectbox(options=pd.DataFrame(st.session_state[sidebar]).columns,label='Variable 3')
             right_column.line_chart(df[selectbox3])
             selectbox4 = st.selectbox(options=pd.DataFrame(st.session_state[sidebar]).columns,label='Variable 4')
             right_column.bar_chart(df[selectbox4])
         multiselect = st.multiselect(options=pd.DataFrame(st.session_state[sidebar]).columns,label="Select To Compare")
         st.line_chart(df[multiselect])
         scatter = alt.Chart(df).mark_point(point=alt.OverlayMarkDef(color='red',opacity=0.5,radius=100)).encode(
             x='Time (Days)',y='Oil Volume',color='Lease'
         ).interactive()
         st.altair_chart(scatter,use_container_width=True)
