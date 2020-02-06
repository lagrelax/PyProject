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
from sklearn.decomposition import PCA

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

# plt.bar(cor_with_price.index,cor_with_price.Corr)
# plt.xticks(cor_with_price.index, cor_with_price.index, rotation='vertical')
# plt.show()

# fill the missings with median
train_numeric=train_numeric.apply(lambda x: x.mask(x.isna(),lambda y:np.nanmedian(y)))

# 1460 obs of 35 features
dv= train_numeric.drop('SalePrice',axis=1,inplace=False)

# Normalization
apply_norm=True
if apply_norm:
    dv=dv.apply(lambda x: x.mask(x==x,(x-np.mean(x))/np.std(x)))

train_features=dv.columns
dv_cov=np.cov(dv,rowvar=0)

# PCA
pca=PCA(n_components=5)
dv_pca=pd.DataFrame(data=pca.fit_transform(dv),columns=['PCA1','PCA2','PCA3','PCA4','PCA5'])

# Regression
X=sm.add_constant(dv_pca)
Y=train_numeric.SalePrice
reg_pca_numeric = sm.OLS(Y,X).fit()
reg_pca_numeric.summary()

# Prediction
test_df=test[train_features]
## Fill NA with median
medians=test_df.apply(lambda x: np.nanmedian(x),axis=0).to_dict()
test_df=test_df.fillna(value=medians)

if apply_norm:
    test_df=test_df.apply(lambda x: x.mask(x==x,(x-np.mean(x))/np.std(x)))

test_pca=pca.transform(test_df)

predict_reg_pca_numeric=pd.Series(reg_pca_numeric.predict(sm.add_constant(test_pca)))

file_name=r'Output/Full_numeric_pca_reg_predict.csv'
if apply_norm:
    file_name=r'Output/Full_numeric_pca_reg_predict_norm.csv'
writeOutput(predict_reg_pca_numeric,file_name)
