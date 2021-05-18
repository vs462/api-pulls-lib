import requests
import json
import dateutil
import streamlit as st

loading = st.sidebar.empty()
info_page = st.sidebar.empty()
info_app  = st.sidebar.empty()
    
#session_state = SessionState.get(loading=loading, info_page = info_page, info_app=info_app)

def trustpilot(data):
    col1, col2 = st.beta_columns([2,1])  
    api_key = 'YhzbqU4GeR6mQ2bHF97PYKUWCSkaaeG0'
    
    with col1:
        business_unit = st.text_input('Enter business_unit','46d31466000064000500a775',help='46d31466000064000500a775')
        start_date = st.text_input('Enter start date','2021-05-01',help='2020-11-01')
        end_date= st.text_input('Enter end date','2021-05-03',help='2021-03-01')
        business_unit_list = business_unit.replace(' ','').split(",")    
    
    if st.button('run'):
        data = pullFromTrustpilot(business_unit_list, api_key, start_date, end_date, business_unit_list)       
        return data
    
    if data:
        return data    


def pullFromTrustpilot(business_units, api_key, start_date, end_date, business_unit_display_name):        
    business_unit_list = [business_units] * (type(business_units) is str) or business_units

    start_date = dateutil.parser.parse(start_date)
    end_date = dateutil.parser.parse(end_date)  
    out_lst = []
    params = {'orderBy': "createdat.desc"}
    
    for business_unit in business_unit_list:
        url = 'https://api.trustpilot.com/v1/business-units/{key}/reviews?perPage=50&page={page}'        
        page_counter = 1                     
        
        while True:
            query_url = url.format(key = business_unit, page = page_counter)
            headers = {'apikey':api_key}
            r = requests.get(query_url, headers=headers, params=params)
            json_data = json.loads(r.text)
            
            loading.write('Getting data...')
            info_page.write(f'Page: {page_counter}')
            info_app.write(f'App: {business_unit}')
            
            try:
                json_data['reviews']
            except:
                st.write(f'Error. Business_unit {business_unit}: ')
                st.write(json_data)
                break
            
            for response in json_data['reviews']:
                clean_response = clean_responses(response, business_unit, 
                                                 business_unit_display_name)
                created_at = dateutil.parser.parse(clean_response['created_at'], ignoretz=True)
                if created_at >= start_date and created_at <= end_date:
                    out_lst.append(clean_response)   
            page_counter+=1  
            
            if not json_data['reviews'] or created_at <= start_date:
                loading.write('Getting data... Done!')
                break
    return out_lst

def clean_responses(response, business_unit, business_unit_display_name):
    clean_response = {}
    clean_response['comment'] = response['text']
    clean_response['score'] = response['stars']
    clean_response['created_at'] = response['createdAt']
    clean_response['language'] = response['language']
    clean_response['title'] = response['title']
    clean_response['response_id'] = response['id']
    clean_response['business_unit'] = business_unit
    #clean_response['business_unit_display_name'] = business_unit_display_name
    return clean_response