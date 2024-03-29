import os 
import pandas as pd

def Get_links():
    query = "Garden Center"

    query_string = "+".join(query.split()).strip()
    df = pd.read_csv('states.csv')

    for i in range(0,len(df)):
        state = df.loc[i,'State']
        print(state)
        command = f"scrapy crawl yp -o output_links/{i}-{state.replace(' ', '_')}.csv -a query={query_string} -a location={state.replace(' ','+')}"
        os.system(command)

def Get_Data():
    files = os.listdir('output_links/')
    files.sort()

    for file in files:
        command = f"scrapy crawl yp_scraper -a input_file=output_links/{file} -o output_data/{file.replace('.csv','_data.csv')}"
        os.system(command)

def main():
    Get_links()
    Get_Data()


if __name__ == '__main__':
    main()





    
