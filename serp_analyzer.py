import pandas as pd
# merge result
# clean up data
def reformat(infile='./result.txt',outfile='./55newresult.txt'):
    f1 = open(infile, 'r')
    f2 = open(outfile, 'w')
    try:
        for line in f1:
            tmp = line.replace(";['']", "").strip()
            f2.write(tmp+(";"*(11-tmp.count(";")))+"\n")
            #f2.write(tmp)
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

# analysis

#1.

def main():
    reformat()
    read_serp_result()


if __name__ == '__main__':

    main()
