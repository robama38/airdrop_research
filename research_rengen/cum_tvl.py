#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 20:11:27 2024

@author: kevinrubio
"""

import pandas as pd
import requests

file_path = '/Users/kevinrubio/Desktop/protocol_list.csv'
df_p = pd.read_csv(file_path)

# List of protocols
protocols = df_p['protocols']

# Initialize an empty DataFrame for the cumulative TVL data
cum_tvl_data = pd.DataFrame(columns=['protocol', 'cum_tvl'])

# Base URL
base_url = 'https://api.llama.fi/protocol/{}'

# Loop through each protocol
for protocol in protocols:
    # Fetching the data
    url = base_url.format(protocol)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Assuming you want to work with data from the same chain for each protocol
        chain = 'Arbitrum'  # Change to the relevant chain if different
        if chain in data['chainTvls']:
            nested_data = data['chainTvls'][chain]['tvl']

            # Convert the nested data to a DataFrame
            df = pd.DataFrame(nested_data)
            
            # Get the earliest timestamp in the data
            earliest_ts = df['date'].min()

            # Specify your end timestamp
            end_ts = 1675659600  # Replace with your desired end date Unix timestamp

            # Filter the DataFrame
            df_filtered = df[(df['date'] >= earliest_ts) & (df['date'] <= end_ts)]

            # Calculate cumulative TVL for the protocol
            cum_tvl = df_filtered['totalLiquidityUSD'].sum()

            # Add the protocol and its cumulative TVL to the DataFrame
            cum_tvl_data = cum_tvl_data.append({'protocol': protocol, 'cum_tvl': cum_tvl}, ignore_index=True)
        else:
            print(f"Chain {chain} not found in data for {protocol}")

    else:
        print(f"Failed to fetch data for {protocol}: {response.status_code}")

# Merging the 'tokens' column from df_p into cum_tvl_data
cum_tvl_data_merged = cum_tvl_data.merge(df_p[['protocols', 'tokens']], 
                                         left_on='protocol', 
                                         right_on='protocols', 
                                         how='left')

# Dropping the 'protocols' column from the merged DataFrame
cum_tvl_data_merged.drop('protocols', axis=1, inplace=True)

com_data = cum_tvl_data_merged[cum_tvl_data_merged['cum_tvl']!=0]

# Save DataFrame to CSV
com_data.to_csv('com_data.csv', index=False)





