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

# cor matrix -- 35 cols, not easy to render
#cm=np.corrcoef(test_numeric.values)
#cols=test_numeric.columns
#sns.set()
#hm=sns.heatmap(cm,cbar=True,annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, yticklabels=cols.values, xticklabels=cols.values)

cor_with_price=pd.DataFrame({'Feature':[],'Corr':[]})

for x in train_numeric.columns:
    if not x == 'SalePrice':
        tmp=train_numeric[[x,'SalePrice']].corr()
        cor_with_price=pd.concat([cor_with_price,pd.DataFrame({'Feature':[x],'Corr':[tmp.iloc[0,1]]})])

cor_with_price.set_index('Feature',inplace=True)

plt.bar(cor_with_price.index,cor_with_price.Corr)
plt.xticks(cor_with_price.index, cor_with_price.index, rotation='vertical')
plt.show()

# The following featurs have very high corr
cor_with_price[cor_with_price.Corr>0.6]

# What-if just running a regression on those features?
reg_features=cor_with_price[cor_with_price.Corr>0.6].index.to_list()
reg_df=train_numeric[reg_features+['SalePrice']]
# First check their pattern among independent variables
reg_iv=reg_df[reg_df.columns.difference(['SalePrice'])]
#sns.set()
#sns.pairplot(reg_iv)

reg_iv_cor=reg_iv.corr()
reg_iv_cor
sns.set()
ax=sns.heatmap(reg_iv_cor,annot=True)
ax.set_ylim(6.0, 0)

# Run regression
X=sm.add_constant(reg_df.iloc[:,0:6])
Y=reg_df.SalePrice
reg1 = sm.OLS(Y,X).fit()
reg1.summary()

# Prediction
test_reg1=test[reg_features]

# Fill NA with median
medians=test_reg1.apply(lambda x: np.nanmedian(x),axis=0).to_dict()
test_reg1=test_reg1.fillna(value=medians)

predict_reg1=reg1.predict(sm.add_constant(test_reg1))

writeOutput(predict_reg1,r'Output/reg1_predict.csv')

# Final score 0.63188