from appfollow_api import AppFollowAPI
import streamlit as st
from secrete import appfollow_api_secrete, appfollow_cid

loading = st.sidebar.empty()
info_page = st.sidebar.empty()
info_app  = st.sidebar.empty()

def appfollow(data):
    col1, col2 = st.beta_columns([2,1])  
    with col1:
        external_ids = st.text_input('Enter id(s)','com.vanuatu.aiqfome',help='com.vanuatu.aiqfome')
        start_date = st.text_input('Enter start date','2021-05-01',help='2020-11-01')
        end_date= st.text_input('Enter end date','2021-05-03',help='2021-03-01')
        external_id_list = external_ids.replace(' ','').split(",")
    with col2:
        cid = st.text_input('Enter cid',appfollow_cid, help = appfollow_cid)
        api_secret = st.text_input('Enter API secret', appfollow_api_secrete, help = appfollow_api_secrete)

    if st.button('run'):
       data = get_appfollow_review(cid, api_secret, external_id_list, start_date, end_date) 
       loading.write('Getting data... Done!')
       return data
    
    if data:
        return data 
 

def get_appfollow_review(client_id, api_secret, external_id, start_date='1900-01-01', end_date='2100-01-01'):
    api = AppFollowAPI(client_id, api_secret) 

    ext_id_list = [external_id] * (type(external_id) is str) or external_id
    responses_list = []
    kwargs = {'from':start_date, 'to':end_date}
    
    for ext_id in ext_id_list:
        try:
            page_counter = api.reviews(ext_id, **kwargs)
        except Exception as e:
            st.write('Error:', str(e), f', external id: "{ext_id}"')
            break

        pages = page_counter['reviews']['page']['total']
        try:
            for page in range(1, pages+1):
                loading.write('Getting data...')
                info_page.write(f'Page: {page}')
                info_app.write(f'App: {ext_id}')
                        
                raw_data = api.reviews(ext_id, page=page, **kwargs)                
                for event in raw_data['reviews']['list']:
                     event['external_id'] = ext_id
                     responses_list.append(event)   
                     
        except Exception as e:
            print(e)
    
    return responses_list