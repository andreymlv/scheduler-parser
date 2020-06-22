
import pandas as pd

def main():

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    with open('p.html') as file:
        read_data = file.read()

    f = open('workfile.txt', 'w')

    dfs = pd.DataFrame(pd.read_html(read_data))

    print(dfs)

    f.write(str(dfs))

    file.close()
    f.close()

if __name__ == '__main__':
    main()

