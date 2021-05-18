import requests
import json
from datetime import datetime
import streamlit as st
from secrete import api_key_intercom as api_key


def intercom(data):
    col1, col2 = st.beta_columns([2,1])          
    with col1:
        api_key = st.text_input('Enter api_key', api_key)
        from_date = st.text_input('Enter from date','2021-05-01',help='2020-11-01')
        to_date= st.text_input('Enter to date','2021-05-03',help='2021-03-01')  
        
    if st.button('run'):
        conversation_ids = pullConversationListIntercom(api_key, from_date, to_date)  
        data = pull_full_conversations(api_key, conversation_ids)        
        return data
    
    if data:
        return data 

def pullConversationListIntercom(api_key, from_date, to_date):
    from_date = int(datetime.fromisoformat(from_date).timestamp())
    to_date = int(datetime.fromisoformat(to_date).timestamp())
    
    out_list = []
    url = 'https://api.intercom.io/conversations/search'
    
    headers = { 'Authorization': f'Bearer {api_key}'}
    post_request ={'query': {
        'operator': 'AND',
        'value': [
            {'field': 'created_at',
             'operator': '>',
             'value': from_date},
            {'field': 'created_at',
             'operator': '<',
             'value': to_date}]}}

    def pull_conversation_id_list_page(starting_after=None):
        if starting_after is None:
            r = requests.post(url, headers=headers, json=post_request)
            json_data = json.loads(r.text)
            conversations = json_data['conversations']            
            total_pages = json_data['pages']['total_pages']
            info_tot_pages.write(f'Total pages with IDs is {total_pages}')                        
            for conversation in conversations:
                out_list.append(conversation['id'])
            starting_after = json_data['pages']['next']['starting_after']
            pull_conversation_id_list_page(starting_after=starting_after)

        else:            
            post_request['pagination'] = {'per_page': 150, 'starting_after': starting_after}
            r = requests.post(url, headers=headers, json=post_request)
            json_data = json.loads(r.text)            
            conversations = json_data['conversations']
            for conversation in conversations:
                out_list.append(conversation['id'])
            try:
                starting_after = json_data['pages']['next']['starting_after']
                pull_conversation_id_list_page(starting_after=starting_after)
            except KeyError:
                print(json_data['pages'])

    pull_conversation_id_list_page()  
    return out_list


def pull_single_intercom_conversation(api_key, conversation_id):
    url = f'https://api.intercom.io/conversations/{conversation_id}'
    headers = {'Authorization': f'Bearer {api_key}'}
    
    r_conversation = requests.get(url, headers=headers)
    conversation_data = json.loads(r_conversation.text)
    contact_id = conversation_data['contacts']['contacts'][0]['id']
    contact_url = f'https://api.intercom.io/contacts/{contact_id}'
    r_contact = requests.get(contact_url, headers=headers)
    conversation_data['contact_details'] = json.loads(r_contact.text)
    conversation_source = conversation_data['source']

    first_conversation_part = {
        'type': 'conversation',
        'id': conversation_source['id'],
        'delivered_as': conversation_source['delivered_as'],
        'subject': conversation_source['subject'],
        'body': conversation_source['body'],
        'author': conversation_source['author'],
        'attachments': conversation_source['attachments'],
        'url': conversation_source['url'],
        'created_at': conversation_data['created_at'],
        'updated_at': conversation_data['updated_at'],
        'part_type': 'comment'}
    conversation_data['conversation_parts']['conversation_parts'].insert(0, first_conversation_part)
    return conversation_data

def pull_full_conversations(api_key, conversation_id_list):
    out_list = []
    tot_conv.write(f'Total {len(conversation_id_list)} converstation')
    for i, conversation_id in enumerate(conversation_id_list):
        i += 1
        info_page.write(f"Pulling conversation ID {i}")
        full_conversation = pull_single_intercom_conversation(api_key, conversation_id)
        out_list.append(full_conversation)
    return out_list





   