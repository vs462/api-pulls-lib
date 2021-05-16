from appfollow_api import AppFollowAPI
import streamlit as st
import SessionState
from datetime import datetime
import time 
from secrete import appfollow_api_secrete, appfollow_cid

session_state = SessionState.get(checkboxed=False)
state = SessionState.get(display_page = 0)  # Pick some initial values.

def appfollow():
    col1, col2 = st.beta_columns([2,1])  
    st.write(datetime.now())

    with col1:
        external_ids = st.text_input('Enter id(s)','com.vanuatu.aiqfome',help='com.vanuatu.aiqfome')
        start_date = st.text_input('Enter start date','2021-05-01',help='2020-11-01')
        end_date= st.text_input('Enter end date','2021-05-03',help='2021-03-01')
        external_id_list = external_ids.replace(' ','').split(",")
    with col2:
        cid = st.text_input('Enter cid',appfollow_cid, help = appfollow_cid)
        api_secret = st.text_input('Enter API secret', appfollow_api_secrete, help = appfollow_api_secrete)

    if st.button('run') or session_state.checkboxed:
        session_state.checkboxed = True
        data = get_appfollow_review(cid, api_secret, external_id_list, start_date, end_date)        
        return data
 

def get_appfollow_review(client_id, api_secret, external_id, start_date='1900-01-01', end_date='2100-01-01'):
    api = AppFollowAPI(client_id, api_secret) 

    ext_id_list = [external_id] * (type(external_id) is str) or external_id
    
    responses_list = []
    kwargs = {'from':start_date, 'to':end_date}    
    info_ph = st.empty()

    for ext_id in ext_id_list:
        page_counter = api.reviews(ext_id, **kwargs)
        pages = page_counter['reviews']['page']['total']
        try:
            for page in range(1, pages+1):
                info_ph.info(f'Current page: {page}, App: {ext_id}')
                raw_data = api.reviews(ext_id, page=page, **kwargs)                
                for event in raw_data['reviews']['list']:
                     event['external_id'] = ext_id
                     responses_list.append(event)      
        except Exception as e:
            print(e)
    return responses_list














