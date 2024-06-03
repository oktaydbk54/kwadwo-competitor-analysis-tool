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

def load_data(website_url):
    # Data yükleme ve hesaplama, eğer website_url değiştiyse veya ilk kez çalıştırılıyorsa
    if 'website_input' not in st.session_state or st.session_state.website_input != website_url or 'data_loaded' not in st.session_state:
        st.session_state.website_input = website_url
        st.session_state.data_loaded = True  # Verilerin yüklendiğini belirt
        st.session_state.domain_analysis = domainAnalysis().domain_rank_module(website_url)
        st.session_state.historical_rank = domainAnalysis().historical_rank_module(website_url)
        st.session_state.founder_description = companyFounderDescription().createDescription(website_url)
        st.session_state.company_description = companyDescription().createDescription(website_url)
        st.session_state.social_links = social_Links().findSocialLinks(website_url)
        st.session_state.investors = Inverstors().investors_values(website_url)
        st.session_state.company_values = valuePro().find_values(website_url)
        st.session_state.competitors = companyCompetitors().competitorsFinder(website_url)
        st.session_state.papers = researcher().findRelativePapers(website_url)


def display_data(page,website):
    # Veri gösterimi
    if page == 'Domain Analysis':
        st.subheader('Domain Analysis')
        st.write(st.session_state.domain_analysis['Domain Analysis'])

    elif page == 'Historical Rank Analysis':
        st.subheader('Historical Rank Analysis')
        st.write(st.session_state.historical_rank['Historical Overview'])

    elif page == "Company Founders":
        st.subheader('Company Founders')
        st.write(st.session_state.founder_description)

    elif page == "Company Description":
        st.subheader("Company Description")
        st.write(st.session_state.company_description)
    
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
        st.write(st.session_state.competitors)
        company = st.selectbox("Choose a company from the list:", st.session_state.competitors['Competitor'])
        user_competitor = st.text_input('Please Enter Your Compotitors','')
        if st.button("Confirm Selection"):
            if user_competitor != '':
                results = companyCompetitors().targetCompetitorAnalysis(website,user_competitor)
            else:
                results = companyCompetitors().targetCompetitorAnalysis(website,company)
            st.json(results)

    elif page == "Company News":
        st.subheader('Company News')
        search_news_dict = duckduckgo_news_search(website)
        for news in search_news_dict:
            if news['image']:
                st.image(news['image'], width=100)
            st.markdown(f"### [{news['title']}]({news['url']})")
            st.write(news['body'])
            st.markdown(f"**Source:** {news['source']}")
            st.markdown("---")
    
    elif page == "Research Papers":
        st.subheader('Research Papers')
        st.json(st.session_state.papers)


def main():
    st.title("Website Analysis Tool")

    page_options = ['Domain Analysis', 'Historical Rank Analysis', "Company Description", "Company Founders", "Social Media Links", "Investors","Company Advantages",'Competitor Analysis','Company News',"Research Papers"]
    selected_page = st.sidebar.radio("Select Analysis Page:", page_options, index=page_options.index(st.session_state.selected_page if 'selected_page' in st.session_state else 'Domain Analysis'))
    st.session_state.selected_page = selected_page

    website_input = st.text_input("Enter the URL of the website:", st.session_state.website_input if 'website_input' in st.session_state else "")

    if st.button("Start Analysis"):
        if website_input:
            load_data(website_input)  # Verileri yükle
            st.session_state.trigger_analysis = True
        else:
            st.error("Please enter a valid URL to start the analysis.")

    if 'trigger_analysis' in st.session_state and st.session_state.trigger_analysis:
        display_data(selected_page,website_input)

if __name__ == "__main__":
    main()