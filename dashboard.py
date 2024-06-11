import streamlit as st
from domain_analysis_module import domainAnalysis
from company_founders import companyFounderDescription
from company_description import companyDescription
from social_media_module import social_Links
from investors_module import Inverstors
from value_proposition_module import valuePro
from competitor_analysis import companyCompetitors
from company_news import duckduckgo_news_search
from research_paper_finder import researcher
import json

def load_data(website_url, model_choice):
    if ('website_input' not in st.session_state or st.session_state.website_input != website_url or 'data_loaded' not in st.session_state):
        st.session_state.website_input = website_url
        st.session_state.data_loaded = True
        modules = {
            'domain_analysis': domainAnalysis().domain_rank_module,
            'historical_rank': domainAnalysis().historical_rank_module,
            'founder_description': companyFounderDescription().createDescription,
            'company_description': companyDescription().createDescription,
            'social_links': social_Links().findSocialLinks,
            'investors': Inverstors().investors_values,
            'company_values': valuePro().find_values,
            'papers': researcher().findRelativePapers
        }
        for key, func in modules.items():
            try:
                st.session_state[key] = func(website_url, model_choice)
            except Exception as e:
                st.error(f"Error loading {key}: {e}")

def display_data(page, website):
    if page == 'Domain Analysis':
        st.subheader('Domain Analysis')
        st.write(st.session_state.domain_analysis.get('Organic Search Overview', 'N/A'), '\n', st.session_state.domain_analysis.get('Paid Search Overview', 'N/A'), '\n')

    elif page == 'Historical Rank Analysis':
        st.subheader('Historical Rank Analysis')
        st.write(st.session_state.historical_rank.get('Historical Overview', 'N/A'))

    elif page == "Company Founders":
        st.subheader('Company Founders')
        st.write(st.session_state.founder_description)

    elif page == "Company Description":
        st.subheader("Company Description")
        st.write('-' * 10)
        sections = ['Overview', 'Features', 'Pricing']
        for section in sections:
            st.subheader(f"Company {section}")
            st.write(st.session_state.company_description.get(section, {}).get(f'Company {section}', 'N/A'), '\n', st.session_state.company_description.get(section, {}).get('References', 'N/A'))
            st.write('-' * 10)

    elif page == "Social Media Links":
        st.subheader('Social Media Links')
        st.write(st.session_state.social_links)

    elif page == "Investors":
        st.subheader("Investors")
        st.write(st.session_state.investors)

    elif page == "Company Advantages":
        st.subheader('Value Propositions')
        st.write(st.session_state.company_values)

    elif page == "Competitor Analysis":
        st.subheader('Company Competitors')
        try:
            st.session_state.competitors = companyCompetitors().competitorsFinder(website, 'ChatGPT', st.session_state.model_choice)
            st.session_state.selected_company = None
            st.session_state.results = None
        except Exception as e:
            st.error(f"Error fetching competitors: {e}")

        if 'competitors' in st.session_state and st.session_state.competitors:
            st.write("Competitors List:")
            competitors_list = st.session_state.competitors.get('Competitor', [])
            for competitor in competitors_list:
                st.write(competitor)

    elif page == "Company News":
        st.subheader('Company News')
        try:
            # Haberler henüz yüklenmemişse yükle
            if 'search_news_dict' not in st.session_state:
                st.session_state.search_news_dict = duckduckgo_news_search(website)
            
            # Haberleri listele
            search_news_dict = st.session_state.search_news_dict
            if not search_news_dict:
                st.write("No news found.")
            for news in search_news_dict:
                if news.get('image'):
                    st.image(news['image'], width=100)
                st.markdown(f"### [{news['title']}]({news['url']})")
                st.write(news['body'])
                st.markdown(f"**Source:** {news['source']}")
                st.markdown("---")
        except Exception as e:
            st.error(f"Error fetching company news: {e}")

    elif page == "Research Papers":
        st.subheader('Research Papers')
        try:
            st.json(st.session_state.papers)
        except json.JSONDecodeError as e:
            st.error(f"Error displaying research papers: {e}")

def main():
    st.title("Website Analysis Tool")

    page_options = ['Domain Analysis', 'Historical Rank Analysis', "Company Description", "Company Founders", "Social Media Links", "Investors", "Company Advantages", 'Competitor Analysis', 'Company News', "Research Papers"]
    selected_page = st.sidebar.radio("Select Analysis Page:", page_options, index=page_options.index(st.session_state.get('selected_page', 'Domain Analysis')))
    st.session_state.selected_page = selected_page

    website_input = st.text_input("Enter the URL of the website:", st.session_state.get('website_input', ""))

    model_choice = st.radio(
        "Choose an AI Model:",
        ('gpt-4o', 'gpt-3.5-turbo-0125'),
        index=0 if st.session_state.get('model_choice', 'gpt-4o') == 'gpt-4o' else 1
    )
    st.session_state.model_choice = model_choice

    if st.button("Start Analysis"):
        if website_input:
            load_data(website_input, model_choice)
            st.session_state.trigger_analysis = True
        else:
            st.error("Please enter a valid URL to start the analysis.")

    if st.session_state.get('trigger_analysis', False):
        display_data(selected_page, website_input)

if __name__ == "__main__":
    main()
