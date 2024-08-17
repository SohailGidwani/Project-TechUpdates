import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain_openai import AzureChatOpenAI
from parsera import Parsera
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('app.env'))

# Initialize your language model client
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    openai_api_version=os.getenv("AZURE_API_VERSION"),
    deployment_name=os.getenv("DEPLOYMENT_NAME"),
    openai_api_key=os.getenv("AZURE_API_KEY"),
    openai_api_type=os.getenv("API_TYPE"),
    temperature=0.0,
)

print(llm)
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
# Website and elements setup with URLs included
elements = {
    "TechCrunch": {
        "Title": "article header h2",
        "Details": "article p",
        "Type": "article .tag",  # Specific type directly from the site
        "URL": "article header h2 a[href]",
        "Source": "TechCrunch"
    },
    "Crunchbase News": {
        "Title": "div.news-item h3",
        "Details": "div.news-item p",
        "Type": "div.news-item .category",  # Specific type directly from the site
        "URL": "div.news-item h3 a[href]",
        "Source": "Crunchbase News"
    },
    "YCombinator": {
        "Title": "tr.athing td.title a",
        "Details": "tr + tr .subtext",
        "Type": "tr + tr .subtext .sitebit comhead",  # Infer type from the subtext class, generally "News"
        "URL": "tr.athing td.title a[href]",
        "Source": "YCombinator"
    },
    "Ars Technica": {
        "Title": ".article-summary .article-title",
        "Details": ".article-summary .excerpt",
        "Type": ".article-summary .meta",  # Specific type directly from the site
        "URL": ".article-summary .article-title a[href]",
        "Source": "Ars Technica"
    },
    "Slashdot": {
        "Title": ".story .story-title a",
        "Details": ".story .body",
        "Type": ".story .story-category",  # Attempt to infer type from the category class
        "URL": ".story .story-title a[href]",
        "Source": "Slashdot"
    },
    "Lobsters": {
        "Title": ".story-liner .u-url",
        "Details": ".story-liner .tagline",
        "Type": ".story-liner .tags",  # Tags often serve as a good proxy for type
        "URL": ".story-liner .u-url[href]",
        "Source": "Lobsters"
    },
    "Tech Funding News": {
        "Title": ".news-article__title",
        "Details": ".news-article__summary",
        "Type": ".news-article__category",  # Using category as type
        "URL": ".news-article__title a[href]",
        "Source": "Tech Funding News"
    }
}


# Function to scrape a single website
def scrape_site(site, url, elements):
    scrapper = Parsera(model=llm)
    print("Now scrapping : ", site)
    results = scrapper.run(url=url, elements=elements[site])
    for result in results:
        result['Source'] = site  # Add the source tag to each result
    return results

# Using ThreadPoolExecutor to run scraping tasks concurrently
all_results = []
with ThreadPoolExecutor(max_workers=len(elements)) as executor:
    futures = [executor.submit(scrape_site, site, url, elements) for site, url in urls.items()]
    for future in as_completed(futures):
        all_results.extend(future.result())

# Save results to JSON
with open('scraped_data.json', 'w') as f:
    json.dump(all_results, f, indent=4)

print("Scraping completed and data saved to 'scraped_data.json'.")
