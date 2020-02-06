# Import necessary libaries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import norm, skew
from sklearn import linear_model
import statsmodels.api as sm
from util import *

pd.set_option('display.max_columns',10)
color=sns.color_palette()
sns.set_style('darkgrid')

# 0. Read data
train = pd.read_csv('Data/train.csv')
test = pd.read_csv('Data/test.csv')

# Drop the Id col
train.drop('Id',axis=1,inplace=True)
test.drop('Id',axis=1,inplace=True)

# 1. Scatter plot (of numeric cols)
# Select all the numerical cols
train_numeric=train.select_dtypes(include=['float64','int64'])
# Also drop YrSold
train_numeric.drop('YrSold',axis=1,inplace=True)

# Scatter plot -- 35 cols, not easy to interpret
#sns.set()
#sns.pairplot(test_numeric)

cor_with_price=pd.DataFrame({'Feature':[],'Corr':[]})

for x in train_numeric.columns:
    if not x == 'SalePrice':
        tmp=train_numeric[[x,'SalePrice']].corr()
        cor_with_price=pd.concat([cor_with_price,pd.DataFrame({'Feature':[x],'Corr':[tmp.iloc[0,1]]})])

cor_with_price.set_index('Feature',inplace=True)

plt.bar(cor_with_price.index,cor_with_price.Corr)
plt.xticks(cor_with_price.index, cor_with_price.index, rotation='vertical')
plt.show()

# Run regression
reg_features=train_numeric.columns.to_list()
if 'SalePrice' in reg_features:
    reg_features.remove('SalePrice')
reg_df=train_numeric[reg_features+['SalePrice']]

# fill the missings with median
reg_df=reg_df.apply(lambda x: x.mask(x.isna(),lambda y:np.nanmedian(y)))

X=sm.add_constant(reg_df[reg_features])
Y=reg_df.SalePrice
reg_full_numeric = sm.OLS(Y,X).fit()
reg_full_numeric.summary()

# Prediction
test_reg=test[reg_features]

# Fill NA with median
medians=test_reg.apply(lambda x: np.nanmedian(x),axis=0).to_dict()
test_reg=test_reg.fillna(value=medians)

predict_reg_full_numeric=reg_full_numeric.predict(sm.add_constant(test_reg))

writeOutput(predict_reg_full_numeric,r'Output/Full_numeric_reg_predict.csv')
