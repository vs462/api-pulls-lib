import json
import boto3

def save_jsonl_localy(data, output_path, append=False):
    mode = 'a+' if append else 'w'
    with open(output_path, mode, encoding='utf-8') as f:
        for line in data:
            json_record = json.dumps(line, ensure_ascii=False)
            f.write(json_record + '\n')
       
def upload_to_s3(data, loc_file_path, file_name, bucket, prefix):
    ''' upload file from a local folder to S3 '''
    s3 = boto3.resource('s3')   
    
    loc_file_name = f"{loc_file_path}/{file_name}"
    save_jsonl_localy(data, loc_file_name)
    s3_file_name = f"{prefix}/{file_name}"
   
    s3.Bucket(bucket).upload_file(loc_file_name, s3_file_name)
    
# loc_file_path = '/Users/vasilisa/desktop/api_pulls/data'
# file_name = 'test_sm_google.jsonl'
# bucket = 'cm-data-ops'    
# prefix = 'testing'




