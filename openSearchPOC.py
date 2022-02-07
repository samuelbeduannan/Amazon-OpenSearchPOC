import streamlit as st
import pandas as pd
import json
from opensearchpy import OpenSearch

host = 'search-sentiment-analysis-lozt4widmwshwm7goxea5dcavm.us-west-2.es.amazonaws.com'
port = 443
auth = ('******', '********') # For testing only. Don't store credentials in code.

# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = auth,
    verify_certs = False,
    use_ssl = True
)


index_name = 'news_articles'
# # Delete the index.
# response = client.indices.delete(
#     index = index_name
# )

# print('\nDeleting index:')
# print(response)
# # Create an index with non-default settings.

# index_body = {
#   'settings': {
#     'index': {
#       'number_of_shards': 5
#     }
#   }
# }

# response = client.indices.create(index_name, body=index_body)
# print('\nCreating index:')
# print(response)


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
                
                res = client.search(index=index_name, body=body)
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

