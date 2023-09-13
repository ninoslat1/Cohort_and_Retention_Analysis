# -*- coding: utf-8 -*-
"""Cohort and Retention.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GVvesaTX07H4QI7o1xwG_wwloe9fxh57

Membaca file .CSV
"""

import pandas as pd
import numpy as np

data = pd.read_csv('data.csv', engine='python', encoding='ISO-8859-1')
data.head()

"""Formatting Timestamp"""

import dateutil
from datetime import datetime as dt
from pytz import utc

data['datetime'] = data['InvoiceDate'].apply(lambda x: dateutil.parser.parse(x).timestamp())
data['month'] = data['datetime'].apply(lambda x: dt.fromtimestamp(x, utc).month)
data['year'] = data['datetime'].apply(lambda x: dt.fromtimestamp(x, utc).year)
data.head()

"""Membuat Cohort"""

#Format Data -> 2010 Agustus -> 201008

data['cohort'] = data.apply(lambda row: (row['year']*100) + (row['month']), axis=1)

#2010*100 = 201000 + 08 = 201008

cohorts = data.groupby('CustomerID')['cohort'].min().reset_index()
cohorts.columns = ['CustomerID', 'first_cohort']
data = data.merge(cohorts, on='CustomerID', how='left')
cohorts.head()

data.head()

"""Membuat headers tiap Cohort"""

headers = data['cohort'].value_counts().reset_index()
headers.columns = ['Cohorts', 'Count']
headers.head()
headers = headers.sort_values(['Cohorts'])['Cohorts'].to_list()
headers

"""Pivot Data Berbasis Cohort"""

data.head()

"""Drop Missing Value"""

data.dropna(inplace=True)

"""Membuat Jarak Cohort"""

data['cohort_distance'] = data.apply(lambda row: (headers.index(row['cohort']) - headers.index(row['first_cohort'])) if(row['first_cohort'] != 0 and row['cohort'] !=0) else np.nan, axis=1)
data.head()

cohort_pivot = pd.pivot_table(data, index='first_cohort', columns='cohort_distance', values='CustomerID', aggfunc=pd.Series.nunique)
cohort_pivot

#Pembagian nilai cohort di kolom 1 .... n dengan 0
cohort_pivot = cohort_pivot.div(cohort_pivot[0], axis=0)
cohort_pivot

"""Beautify Data"""

import seaborn as sns
import matplotlib.pyplot as plt

fig_dims = (12,8)
fig, ax = plt.subplots(figsize=fig_dims)
sns.heatmap(cohort_pivot, annot=True, fmt='.0%', mask=cohort_pivot.isnull(), ax=ax, square=True, linewidths=6, cmap=sns.cubehelix_palette(8))
plt.show()