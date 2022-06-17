import os 
import pandas as pd



def Get_links(query):
    query_string = "+".join(query.split()).strip()
    df = pd.read_csv('states.csv')

    for i in range(0,len(df)):
        state = df.loc[i,'State']
        print(state)
        command = f"scrapy crawl yp -o output_links/{i}-{state.replace(' ', '_')}.csv -a query={query_string} -a location={state.replace(' ','+')}"
        os.system(command)

def Get_Data():
    df = pd.read_csv('states.csv')

    for i in range(0,len(df)):
        file = f"{i}-{df.loc[i,'State'].replace(' ','_')}.csv"
        print(file)
        command = f"scrapy crawl yp_scraper -a input_file=output_links/{file} -o output_data/{file.replace('.csv','_data.csv')}"
        os.system(command)

def Merge_data(query):
    files = os.listdir('output_data/')
    all_data = []
    for file in files:
        all_data.append(pd.read_csv('output_data/' + file))
    df = pd.concat(all_data)
    df = df.drop_duplicates()
    df.to_csv(f"{query.replace(' ','_')}.csv", index=False)
    print(df)

def main(query):
    Get_links(query=query)
    Get_Data()
    Merge_data(query=query)

if __name__ == '__main__':
    main(query = "Garden Center")





    
