import pandas as pd

# Load the dataset
df = pd.read_excel('/Users/richardhindley/E-commerce-Sales-Analysis/Online Retail.xlsx')
print(df.head())

# Remove rows with missing values
df = df.dropna()

# Convert columns to appropriate data types
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['CustomerID'] = df['CustomerID'].astype(int)

print(df.info())

print(df.describe())

import matplotlib.pyplot as plt
import seaborn as sns

# Plot the distribution of unit prices
plt.figure(figsize=(10, 6))
sns.histplot(df['UnitPrice'], bins=50)
plt.title('Distribution of Unit Prices')
plt.xlabel('Unit Price')
plt.ylabel('Frequency')
plt.show()

# Plot the number of transactions over time
plt.figure(figsize=(14, 7))
df['InvoiceDate'].groupby(df['InvoiceDate'].dt.to_period('M')).count().plot(kind='bar')
plt.title('Number of Transactions Over Time')
plt.xlabel('Month')
plt.ylabel('Number of Transactions')
plt.show()

import datetime as dt

# Define the reference date
reference_date = dt.datetime(2011, 12, 10)

# Calculate RFM values
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (reference_date - x.max()).days,
    'InvoiceNo': 'count',
    'TotalAmount': 'sum'
})

rfm.columns = ['Recency', 'Frequency', 'Monetary']
print(rfm.head())

# Define RFM segments
rfm['R_Segment'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1])
rfm['F_Segment'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4])
rfm['M_Segment'] = pd.qcut(rfm['Monetary'], 4, labels=[1, 2, 3, 4])

# Combine segments to create RFM score
rfm['RFM_Score'] = rfm['R_Segment'].astype(str) + rfm['F_Segment'].astype(str) + rfm['M_Segment'].astype(str)
print(rfm.head())

# Plot RFM segments
plt.figure(figsize=(10, 6))
sns.countplot(x='RFM_Score', data=rfm)
plt.title('Distribution of RFM Scores')
plt.xlabel('RFM Score')
plt.ylabel('Number of Customers')
plt.show()


