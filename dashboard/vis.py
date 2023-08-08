import pandas as pd

df = pd.read_csv("netflix_processed.csv")

def read_titles(type_read, cast_read, listed_in_read):
    row = 0
    df_dic = {}
    title, show_type, country, desc, listed_in = [], [], [], [], []
    for cast in df['cast']:
        for i in cast.split(','):
            i = i.strip()

            if i == cast_read:

                title.append(df['title'][row])
                show_type.append(df['type'][row])
                country.append(df['country'][row])
                desc.append(df['description'][row])
                listed_in.append(df['listed_in'][row])
        row += 1 

    df_dic = {'title':title, 'type':show_type, 'country':country, 'description':desc, 'listed_in': listed_in}
    df_new = pd.DataFrame.from_dict(df_dic,orient='index').transpose()

    row1 = 0
    df_dic1 = {}
    title1, show_type1, country1, desc1, listed_in1 = [], [], [], [], []
    for genre in df_new["listed_in"]:
        for j in genre.split(','):
            j = j.strip()

            if j == listed_in_read:
                
                title1.append(df_new['title'][row1])
                show_type1.append(df_new['type'][row1])
                country1.append(df_new['country'][row1])
                desc1.append(df_new['description'][row1])

        row1 += 1

    df_dic1 = {'title':title1, 'type':show_type1, 'country':country1, 'description':desc1}
    df_new1 = pd.DataFrame.from_dict(df_dic1,orient='index').transpose()

    df_latest1 = df_new1.loc[(df_new['type'] == type_read)]

    return df_latest1
