#print('Hello world')

import streamlit as st
from elasticsearch import Elasticsearch
import pandas as pd
import json


es = Elasticsearch(host='******')
# es = Elasticsearch()

news_articles = pd.read_csv(r'News.csv')

news_articles = news_articles.fillna('')

print(news_articles.head())

# es.indices.delete(index="news_articles")

# Storing articles in ElasticSearch Database
for i in range(0,len(news_articles['Article Title'])):
    doc_1 = {'title':news_articles['Article Title'][i], 'text':news_articles['Article Text'][i], 'publishing_date':news_articles['Article Date'][i], 'author':news_articles['Article Author'][i]}
    es.index(index="news_articles", doc_type="Nan", id=i, document=doc_1)


JOB_HTML_TEMPLATE = """

<div style="width:100%;height:100%;margin:1px;padding:5px;position:relative;border-radius:5px;border-bottom-right-radius: 10px;
box-shadow:0 0 1px 1px #eee; background-color: white;
  border-left: 5px solid #6c6c6c;color:black;">
<h2>{}</h2>
<p>{}</p>
<h4>{}</h4>
<h4>{}</h4>
</div>

"""


def main():
    menu = ["Home", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    st.title("Search News Articles")

    if choice == "Home":
        st.subheader("Home")

        # Nav Search Form
        with st.form(key='searchform'):
            col1,col3 = st.columns([2,1])
            
            with col1:
                search_term = st.text_input("Search Keyword")
            # with col2:
            #     location = st.text_input("Search Author")
            with col3:
                st.text("Search")
                submit_search = st.form_submit_button(label="Submit Search")
        
        st.success("You searched for {}".format(search_term))

        # Results
        col1, col2 = st.columns([4,1])

        with col1:
            if submit_search:
                # Create Search Query
                search_value = search_term

                results_title_list = []
                results_author_list = []
                results_publishing_date_list = []
                results_text_list = []

                body = {
                    "from":0,
                    "size":5,
                    "query":{
                        "match":{
                            "text":search_value
                        }
                    }
                }
                
                res = es.search(index="news_articles", body=body)
                # time.sleep(120)

                for i in range(0, len(res)):
                    results_title_list.append(json.loads(json.dumps(res))['hits']['hits'][i]["_source"]["title"])
                    results_text_list.append(json.loads(json.dumps(res))['hits']['hits'][i]["_source"]["text"])
                    results_publishing_date_list.append(json.loads(json.dumps(res))['hits']['hits'][i]["_source"]["publishing_date"])
                    results_author_list.append(json.loads(json.dumps(res))['hits']['hits'][i]["_source"]["author"])
                    st.markdown(JOB_HTML_TEMPLATE.format(results_title_list[i], results_text_list[i], results_publishing_date_list[i], results_author_list[i]), unsafe_allow_html=True)
    else:
        st.subheader("About")

if __name__ == '__main__':
    main()

