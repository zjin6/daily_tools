import re
import os
from datetime import datetime
import pandas as pd



def read_htmlfile(file_path):
    """From .html to html string format."""
    with open(file_path, "rb") as f:
        html = f.read().decode("utf-8")
    # print(html[:200])
    return html


def fetch_vmess(html):
    """From string to a set of vmess codes."""
    vmess_pattern = r'vmess://[a-zA-Z0-9+/=]+'
    vmess_codes = set(re.findall(vmess_pattern, html))
    print(str(len(vmess_codes)) + ' vmess codes ' + '-' * 40)
    # for i, code in enumerate(vmess_codes):
    #     print(i+1, code[:40])    
    return vmess_codes


def filename_todatetime(filename):
    """Convert filename to datetime_obj."""
    datetime_str = filename.split('.')[0]  # remove file extension
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H')  # convert to datetime object
    return datetime_obj


def htmlfile_todatedic(file_path):
    """From html file to {date:set(vmess)}."""
    filename = os.path.basename(file_path)
    datetime_obj = filename_todatetime(filename)
    html = read_htmlfile(file_path)
    vmess_codes = fetch_vmess(html)
    date_dict = {datetime_obj : vmess_codes}
    
    for key, value in date_dict.items():
        print(f"{key}: {str(value)[:100]} ... \n")
    return date_dict


def batchvmess_fromfolder(folder_path):
    """From a folder to dict{date:set(vmess)}."""
    alldate_dict = {}
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):
            file_path = os.path.join(folder_path, filename)
            date_dict = htmlfile_todatedic(file_path)
            alldate_dict.update(date_dict)
            
    print('all date:set(vmess) is ready ... \n')
    return alldate_dict


def dict_todf(alldate_dict):
    """Transform alldate_dict to dataframe."""
    data = []
    
    for key, value in alldate_dict.items():
        for code in value:
            data.append([key, code])
    
    df = pd.DataFrame(data, columns=['datetime', 'cipher_code'])
    # add a count column to count duplicates of all values in the code column
    df['counted'] = df.groupby('cipher_code')['cipher_code'].transform('count')
    df = df.sort_values(by='datetime', ascending=False)
    print('df is ready ...\n', df)
    return df


def savedf_tocsv(df, folder_path, df_filename='sum_dataframe.xlsx'):
    """Save df to specific path as csv."""
    df_filepath = os.path.join(folder_path, df_filename)
    df.to_csv(df_filepath)
    print(f'saved to {df_filepath}.')    



if __name__ == '__main__':
    folder_path = r'C:\Users\zjin6\Downloads\freefp' #input("folder path to .html: ")
    alldate_dict = batchvmess_fromfolder(folder_path)
    df = dict_todf(alldate_dict)
    
    savedf_tocsv(df, folder_path, df_filename='sum_dataframe.csv')
    
    # filter the DataFrame by datetime within 5 days and counted numbers greater than 4
    filtered_df = df.loc[(df['datetime'] >= df['datetime'].max() - pd.Timedelta(days=3)) & (df['counted'] >= 3)]
    savedf_tocsv(filtered_df, folder_path, df_filename='selected_sum_dataframe.csv')
