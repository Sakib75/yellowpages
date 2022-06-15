import os 
import pandas as pd
import boto3
query = "Garden Center"

access_key = input('Enter aws acecss key')
secret_access_key = input('Enter secret access key')
def upload_to_s3(symbol,i):
    client = boto3.client('s3', aws_access_key_id=access_key,aws_secret_access_key=secret_access_key)
    upload_file_bucket = 'glassdoor-ratings'
    upload_file_key = f'yp/{i}-' + str(symbol) + '.csv'
    print(upload_file_key)
    client.upload_file(f"output/{symbol}.csv",upload_file_bucket,upload_file_key,ExtraArgs={'ACL':'public-read'})

query_string = "+".join(query.split()).strip()
df = pd.read_csv('states.csv')
print(df)
for i in range(0,len(df)):
    state = df.loc[i,'State']
    print(state)
    command = f"scrapy crawl yp -o output/{state}.csv -a query={query_string} -a location={state}"
    print(command)
    os.system(command)
    upload_to_s3(state,i)


    
