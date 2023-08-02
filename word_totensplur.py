from pattern.en import pluralize, conjugate
import pandas as pd



def get_tenses(word):
    # print(word)
    tenses = {conjugate(word, tense='1sg'),
            conjugate(word, tense='2sg'),
            conjugate(word, tense='3sg'),
            conjugate(word, tense='pl'),
            conjugate(word, tense='part'),
            conjugate(word, tense='past'),
            conjugate(word, tense='ppart')
            }
    return tenses


def get_plural(word):
    return pluralize(word)


def tensplur_todic(word):
    tenses = get_tenses(word)
    plural = get_plural(word)    
    tenses.add(plural)
    tensplur_dict = {tuple(tenses) : word}   
    print(tensplur_dict)
    return tensplur_dict


def batch_tensplur_todic(word_list):
    alltensplur_dict = {}
    
    for word in word_list:
        tensplur_dic = tensplur_todic(word)    
        alltensplur_dict.update(tensplur_dic)
        
    return alltensplur_dict
    

def dict_todf(alltensplur_dict):
    """Transform alldate_dict to dataframe."""
    data = []
    
    for key, value in alltensplur_dict.items():
        for tensplur in key:
            data.append([tensplur, value])
    
    df = pd.DataFrame(data, columns=['tensplur', 'word'])
    print('df is ready ...\n', df)
    return df


if __name__ == '__main__':

    df_toelf9400 = pd.read_excel(r'C:\Users\zjin6\Downloads\toefl9400.xlsx')
    word_list = df_toelf9400['word'].tolist()
    
    alltensplur_dict = batch_tensplur_todic(word_list)
    df_tensplur = dict_todf(alltensplur_dict)
    
    merged_df = pd.merge(df_tensplur, df_toelf9400, on='word', how='left')
    merged_df.to_excel(r"C:\Users\zjin6\Downloads\toefl9400_tensplur.xlsx")





