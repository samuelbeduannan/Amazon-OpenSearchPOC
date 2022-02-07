import streamlit as st
from elasticsearch import Elasticsearch
import pandas as pd
import json
from opensearchpy import OpenSearch

host = 'localhost'
port = 9200
auth = ('******', '*******') # For testing only. Don't store credentials in code.

# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = auth,
    verify_certs = False,

)
index_name = 'news_articles'
# Delete the index.
response = client.indices.delete(
    index = index_name
)

print('\nDeleting index:')
print(response)

# Create an index with non-default settings.

index_body = {
  'settings': {
    'index': {
      'number_of_shards': 5
    }
  }
}

response = client.indices.create(index_name, body=index_body)
print('\nCreating index:')
print(response)


# Add a document with news articles content to the index.
news_articles = pd.read_csv(r'News.csv')

news_articles = news_articles.fillna('')

for i in range(0,len(news_articles['Article Title'])):
    doc_1 = {'title':news_articles['Article Title'][i], 'text':news_articles['Article Text'][i], 'publishing_date':news_articles['Article Date'][i], 'author':news_articles['Article Author'][i]}
    response = client.index(
    index = index_name,
    body = doc_1,
    id = i,
    refresh = True)
    print('\nAdding document:')
    print(response)

# Search for the document.
q = 'miller'
query = {
  'size': 5,
  'query': {
    'multi_match': {
      'query': q,
      'fields': ['title^2', 'director']
    }
  }
}

body = {
  "from":0,
  "size":5,
  "query":{
  "match":{
  "text":'covid'
  }
  }
  }            
res = client.search(index=index_name, body=body)
print('\nSearch results:')
print(response)