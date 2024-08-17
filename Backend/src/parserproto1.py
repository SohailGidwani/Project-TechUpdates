import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain_openai import AzureChatOpenAI
from parsera import Parsera

# Initialize your language model client
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    openai_api_version=os.getenv("AZURE_API_VERSION"),
    deployment_name=os.getenv("DEPLOYMENT_NAME"),
    openai_api_key=os.getenv("AZURE_API_KEY"),
    openai_api_type=os.getenv("API_TYPE"),
    temperature=0.0,
)

# Website and elements setup
urls = {
    "TechCrunch": "https://techcrunch.com/",
    "Crunchbase News": "https://news.crunchbase.com/",
    "YCombinator": "https://news.ycombinator.com/",
    "Ars Technica": "https://arstechnica.com",
    "Slashdot": "https://slashdot.org",
    "Lobsters": "https://lobste.rs",
    "Tech Funding News": "https://techfundingnews.com"
}

elements = {
    "TechCrunch": {
        "Title": "article header h2",
        "Details": "article p",
        "Type": "article .tag"
    },
    "Crunchbase News": {
        "Title": "div.news-item h3",
        "Details": "div.news-item p",
        "Type": "div.news-item .category"
    },
    "YCombinator": {
        "Title": "tr.athing td.title a",
        "Details": "tr + tr .subtext",
        "Points": "tr + tr .subtext span.score"
    },
    "Ars Technica": {
        "Title": ".article-summary .article-title",
        "Details": ".article-summary .excerpt",
        "Type": ".article-summary .meta"
    },
    "Slashdot": {
        "Title": ".story .story-title a",
        "Details": ".story .body",
        "Type": ".story .story-title span"
    },
    "Lobsters": {
        "Title": ".story-liner .u-url",
        "Details": ".story-liner .tagline",
        "Points": ".story-liner .score"
    },
    "Tech Funding News": {
        "Title": ".news-article__title",
        "Details": ".news-article__summary",
        "Type": ".news-article__metadata"
    }
}

# Function to scrape a single website
def scrape_site(site, url):
    scrapper = Parsera(model=llm)
    return site, scrapper.run(url=url, elements=elements[site])

# Using ThreadPoolExecutor to run scraping tasks concurrently
results = {}
with ThreadPoolExecutor(max_workers=len(urls)) as executor:
    future_to_site = {executor.submit(scrape_site, site, url): site for site, url in urls.items()}
    for future in as_completed(future_to_site):
        site = future_to_site[future]
        try:
            site_name, site_results = future.result()
            results[site_name] = site_results
            print(f"Results from {site_name}:")
            for item in site_results:
                print(item)
        except Exception as exc:
            print(f"{site} generated an exception: {exc}")

# Now `results` dictionary contains all the scraped data
