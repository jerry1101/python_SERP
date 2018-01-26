import pandas as pd

from collections import Counter


def reformat(infile='./result.txt',outfile='./55newresult.txt'):
    f1 = open(infile, 'r')
    f2 = open(outfile, 'w')
    try:
        for line in f1:
            tmp = line.replace(";['']", "").strip()
            f2.write(tmp+(";"*(11-tmp.count(";")))+"\n")
    except Exception as e:
        print(e)
        pass
    finally:
        f1.close()
        f2.close()


# read into dataframe
def read_serp_result(file='./55newresult.txt'):
    df=pd.read_csv(file,header=None,delimiter=";")

    for index, row in df.iterrows():
        print(row[0])
        print(row[1])
        print(row[2])
        print('------')
    print(len(df))
    print(df.iloc[4:9,:])


# gte top retailers


def get_top_wine_retailer(category='Beer', top_columns=['R1', 'R2', 'R3', 'R4', 'R5']):
    df = load_serp_result()
    # get top columns
    sub_df = df.loc[df['type'].str.startswith(category), top_columns]
    #print(sub_df)

    rank_list= list(sub_df.values.flatten())

    cnt = Counter(rank_list)
    with open('./counter.txt', 'w') as outputfile:
        for tag, count in cnt.items():
            print(tag+';' + str(count))
            outputfile.write("{};{}\n".format(tag,str(count)))


    return Counter(rank_list)


def load_serp_result():
    header_list = ['type', 'keyword', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10']
    df = pd.read_csv('./allnewresult.txt', delimiter=';', names=header_list)
    return df


# analysis

#1.

def main():

    #reformat('./allresult.txt','./allnewresult.txt')

    get_top_wine_retailer('Spirits')


if __name__ == '__main__':

    main()
