import streamlit as st
import saving_functions as sf
import pandas as pd
import base64
import json 
import SessionState
from datetime import datetime

session_state = SessionState.get(checkboxed=False)

st.set_page_config(layout="wide")
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True) # make buttons display horizontally 
st.markdown('<style>' + open('styles.css').read() + '</style>', unsafe_allow_html=True)
st.title('Pull data from APIs')
            
def initialise():  
    st.markdown(' ## Choose an API', unsafe_allow_html=True)
    api_list = ('Select', 'Appfollow', 'Trustpilot')  
    col1, col2 = st.beta_columns([1,3]) # col 1 would take 1/3 of the width 
    tool = col1.selectbox("", api_list)     
    st.markdown('<p class="sep-line"> </p>', unsafe_allow_html=True)     
    data = None
    if tool =='Appfollow':
        from api_pulls.pull_from_appfollow import appfollow  
        data = appfollow()
        
    if tool =='Trustpilot':
        from api_pulls.pull_from_trustpilot import appfollow 

    if data:
        view_results(data)

    st.markdown('<p class="sep-line"> </p>', unsafe_allow_html=True)

def view_results(data):  
    st.markdown('<p class="sep-line"> </p>', unsafe_allow_html=True)
    st.markdown('## Results', unsafe_allow_html=True)
    st.markdown(f'### Fetched {len(data)} responses', unsafe_allow_html=True)
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        if st.checkbox('Save as json'):  
            data_json = json.dumps(data)
            download_filename = st.text_input('Enter file name','file_name.json',help='file_name.json')
            download_link(data_json, download_filename, 'Save as JSON')
    with col2:            
        if st.checkbox('Save as csv'):  
            data_df = pd.DataFrame(data)
            download_filename = st.text_input('Enter file name','file_name.csv',help='file_name.csv')
            download_link(data_df, download_filename, 'Save as CSV')
    with col3:
        if st.checkbox('Save to S3 as JSONL'):
            s3_location(data)
            
def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)
    b64 = base64.b64encode(object_to_download.encode()).decode() # some strings <-> bytes conversions necessary here    
    st.markdown(f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>' , unsafe_allow_html=True)

def s3_location(data):
    loc_file_path = '/Users/vasilisa/desktop/api_pulls/data'  
    file_name = st.text_input('Enter file name','test_sm_google.jsonl',help='some_name.jsonl')
    bucket = st.selectbox('Choose bucket', sf.list_buckets())     
    prefix = st.text_input('Enter start prefix','testing',help='folder/subfolder')    
    if st.button('save'):
        sf.upload_to_s3(data, loc_file_path, file_name, bucket, prefix)
    
def trustpilot():
    from api_pulls import pull_from_trustpilot
    


    

initialise()

