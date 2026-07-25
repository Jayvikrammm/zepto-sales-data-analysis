import pandas as pd
import numpy as np

"""
Zepto E-commerce Data Analysis
Author: Jay Vikram
Date: 2026-07-25

Analyzes product pricing, stock status, discounts, and category revenue using the Zepto v2 dataset.
"""

df = pd.read_csv('/Users/vxcxy/Downloads/archive/zepto_v2.csv',encoding='cp1252')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# to analyze the data once imported
print(df.head(5))
print(df.dtypes)
print(df.shape)
print(df.describe())
print(df.isnull().sum())
print(df.duplicated().sum())

# convert paise into rupee
df['mrp'] = (df['mrp']/100).astype('int')


""" Insights """

# Found top 10 best-value products based on discount percentage
print(df.nlargest(5,['discountPercent'])[['name','discountPercent']])

# Found high-MRP products that are currently out of stock
df_in_stock = df.query('outOfStock == True')
print(df_in_stock.drop_duplicates(subset='name').nlargest(5,['mrp'])[['name','mrp']])

# Estimated potential revenue for each product category
df['revenue'] = df['discountedSellingPrice'] * df['availableQuantity']
category_revenue = df.groupby('Category')['revenue'].sum().sort_values(ascending=False)
print(category_revenue)

# Filtered expensive products (MRP > ₹500) with less than 10% discount (multiple filter)
print(df[(df['mrp'] > 500) & (df['discountPercent'] < 10)][['name','discountPercent','mrp']].sort_values(by='discountPercent', ascending=False))

# Ranked top 5 categories offering highest average discounts
print(df.groupby('Category')['discountPercent'].mean().sort_values( ascending=False).head(5))

# Calculated price per gram to identify value-for-money products
df['price_per_gram'] = (df['discountedSellingPrice']/df['weightInGms']).round(1)
print(df[(df['weightInGms'] >= 100)][['name','mrp','price_per_gram']])

# Grouped products based on weight into Low, Medium, and Bulk categories
# used numpy for creating multiple criteria

conditions = [ df['weightInGms'] < 1000,
              (df['weightInGms'] >= 1000) & (df['weightInGms'] == 5000),
              (df['weightInGms'] > 5000) & (df['weightInGms'] <= 10000)]

choice = ['Low','Medium','Bulk']

df['weight_tier'] = np.select(conditions, choice, default='unknown')

print(df[['name','weightInGms','weight_tier']].drop_duplicates(subset='name').sort_values(by='weightInGms', ascending=False))
print(df.query("weight_tier == 'Bulk'").name.unique())


# total inventory weight per product category
df['total_weight'] = df['weightInGms'] * df['availableQuantity']
print(df.groupby('Category')['total_weight'].sum().sort_values(ascending=False).nlargest(5))


