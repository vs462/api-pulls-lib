import streamlit as st
import saving_functions as sf
import pandas as pd
import base64
import json 
import SessionState

session_state = SessionState.get(data = None, data_df = None, view = None)

st.set_page_config(layout="wide")
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True) # make buttons display horizontally 
st.markdown('<style>' + open('styles.css').read() + '</style>', unsafe_allow_html=True)
st.title('Pull data from APIs')

def initialise(): 
    session_state.data = get_data()  

    if session_state.data is not None:
        st.markdown('<p class="sep-line"> </p>', unsafe_allow_html=True)       
        view_results(session_state.data)
            
def get_data():  
    data = session_state.data 
    
    api_list = ('Select', 'Appfollow', 'Trustpilot', 'Intercom') 
    col1, col2 = st.beta_columns([1,3]) # col 1 would take 1/3 of the width     
    st.sidebar.markdown(' ## Choose an API', unsafe_allow_html=True)
    tool = st.sidebar.selectbox("", api_list)   

    if tool =='Appfollow':
        from api_pulls.pull_from_appfollow import appfollow  
        data = appfollow(data)
    
    if tool =='Intercom':
        from api_pulls.pull_from_intercom import intercom 
        data = intercom(data)
        
    return data


def view_results(data): 
    st.markdown('## Results', unsafe_allow_html=True)
    st.markdown(f'### Fetched {len(data)} responses', unsafe_allow_html=True)
    col1, col2, col3 = st.beta_columns(3)

    with st.beta_expander('View as table'): 
        if st.button('View') or session_state.view:
            session_state.view = True
            if session_state.data_df is None:
                session_state.data_df = pd.DataFrame(data)
            st.write(session_state.data_df)
    
    with st.beta_expander('Save as csv'):  
        if st.button('Save'):
            if session_state.data_df is None:
                session_state.data_df = pd.DataFrame(data)
            download_filename = st.text_input('Enter file name','file_name.csv', help='file_name.csv')
            download_link(session_state.data_df, download_filename, 'Save as CSV')

    with st.beta_expander('Save to S3 as JSONL'):      
        s3_location(data)


    with st.beta_expander('Save as json'):  
        data_json = json.dumps(data)
        download_filename = st.text_input('Enter file name','file_name.json',help='file_name.json')
        download_link(data_json, download_filename, 'Save as JSON')

    
def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)
    b64 = base64.b64encode(object_to_download.encode()).decode() # some strings <-> bytes conversions necessary here    
    st.markdown(f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>' , unsafe_allow_html=True)

def s3_location(data):
    loc_file_path = '/Users/vasilisa/desktop/api_pulls/data'  
    file_name = st.text_input('Enter file name','file_name.jsonl')
    bucket = st.selectbox('Choose bucket', sf.list_buckets())     
    prefix = st.text_input('Enter prefix','folder/subfolder', help="Folder doesn't have to exist")    
    if st.button('save'):
        msg = sf.upload_to_s3(data, loc_file_path, file_name, bucket, prefix)
        st.markdown(f'### {msg}')
      

initialise()
