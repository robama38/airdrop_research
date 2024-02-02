#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 19:12:22 2024

@author: kevinrubio
"""

import requests
import json

# API Request
url = 'https://api.llama.fi/protocol/xy-finance'
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    # Print the entire data
    print(json.dumps(data, indent=4))  # Pretty printing the JSON data
else:
    print(f"Failed to fetch data: {response.status_code}")
#THIS UNVEILED TO ME THE INNER WORKINGS 