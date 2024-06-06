import streamlit as st
from duckduckgo_search import DDGS

# Haber arama fonksiyonu
def duckduckgo_news_search(query):
    results = DDGS().news(keywords='"'+query+'"', region="wt-wt", safesearch="off", timelimit="m", max_results=10)
    return results

def display_news_results(results):
    for news in results:
        if news['image']:
            st.image(news['image'], width=100)
        st.markdown(f"### [{news['title']}]({news['url']})")
        st.write(news['body'])
        st.markdown(f"**Source:** {news['source']}")
        st.markdown("---")
