import re
import os
from datetime import datetime
import pandas as pd



def read_htmlfile(file_path):
    with open(file_path, "rb") as f:
        html = f.read().decode("utf-8")
    # print(html[:200])
    return html


def fetch_vmess(html):
    vmess_pattern = r'vmess://[a-zA-Z0-9+/=]+'
    vmess_codes = re.findall(vmess_pattern, html)
    print(str(len(vmess_codes)) + ' vmess codes ' + '-' * 40)
    for i, code in enumerate(vmess_codes):
        print(i+1, code)    
    return vmess_codes


def filename_todatetime(filename):
    datetime_str = filename.split('.')[0]  # remove file extension
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H')  # convert to datetime object
    return datetime_obj


def folder_todic(folder_path):
    html_dict = {}
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):
            datetime_obj = filename_todatetime(filename)
            file_path = os.path.join(folder_path, filename)
            html = read_htmlfile(file_path)
            vmess_codes = fetch_vmess(html)
            html_dict[datetime_obj] = vmess_codes
    
    print(html_dict)
    return html_dict


def dict_todf(vmess_dict):
    data = []

    for key, value in vmess_dict.items():
        for code in value:
            data.append([key, code])
    
    df = pd.DataFrame(data, columns=['time', 'code'])
    # add a count column to count duplicates of all values in the code column
    df['count'] = df.groupby('code')['code'].transform('count')
    print(df)
    return df


if __name__ == '__main__':
    folder_path = input("folder path to .html: ")
    vmess_dict = folder_todic(folder_path)
    df = dict_todf(vmess_dict)

    # directory = r'C:\Users\zjin6\Downloads\free'
    
    
    
    
    
    
    
    
    
    
    