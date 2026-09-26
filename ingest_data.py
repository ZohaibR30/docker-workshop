#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd


# In[11]:


# Read a sample of the data
prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
df = pd.read_csv(prefix + 'yellow_tripdata_2021-01.csv.gz')


# In[12]:


# Display first rows
df.head()


# In[13]:


# Check data types
df.dtypes


# In[14]:


# Check data shape
df.shape


# In[15]:


df


# WHAT IS HAPPENING HERE IS THAT THE DATASET HAS INCONSISTENT DATATYPES (THIS WOULDNT HAVE HAD HAPPENED IN .PARQUET)

# TO CATER THIS, THE DATASET IS IMPORTED AGAIN WITH DATATYPES BEING HARD CODED

# In[16]:


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

df = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    dtype=dtype,
    parse_dates=parse_dates
)


# In[22]:


df.dtypes


# NOW LETS PUT THIS DATA IN POSTGRES

# In[ ]:


# !uv add sqlalchemy "psycopg[binary,pool]"


# In[43]:


from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg://root:root@localhost:5432/ny_taxi')


# In[44]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[45]:


df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[51]:


# We don't want to insert all the data at once. Let's do it in batches and use an iterator for that:

df_iter = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000
)


# In[50]:


for df_chunk in df_iter:
    print(len(df_chunk))


# In[41]:


# !uv add tqdm


# In[52]:


from tqdm.auto import tqdm

for df_chunk in tqdm(df_iter):
    df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')


# In[ ]:




