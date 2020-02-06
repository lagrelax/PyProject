import pandas as pd
import os

def writeOutput(df,file_name):
    df.index = df.index + 1461
    df = pd.DataFrame(df, columns=['SalePrice'])
    df.to_csv(file_name, index=True, index_label='Id')
