#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 13:52:31 2024

@author: apurvasij
"""

import requests
import json

url = "https://openlibrary.org/search.json?q=crime+and+punishment&fields=key,title,author_name,editions,editions.key,editions.title,editions.ebook_access,editions.language"

response = requests.get(url)

print(response)