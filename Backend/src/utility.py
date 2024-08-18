import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain_openai import AzureChatOpenAI
from parsera import Parsera
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv,find_dotenv

# Load environment variables
load_dotenv(find_dotenv("app.env"))

# Initialize clients
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    openai_api_version=os.getenv("AZURE_API_VERSION"),
    deployment_name=os.getenv("DEPLOYMENT_NAME"),
    openai_api_key=os.getenv("AZURE_API_KEY"),
    openai_api_type=os.getenv("API_TYPE"),
    temperature=0.0
)
qdrant_client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY")) # adjust as per actual config
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define scraping and categorization logic
# def scrape_and_categorize():
#     urls = {
#         "TechCrunch": "https://techcrunch.com/",
#         "Crunchbase News": "https://news.crunchbase.com/",
#         "YCombinator": "https://news.ycombinator.com/",
#         "Ars Technica": "https://arstechnica.com",
#         "Slashdot": "https://slashdot.org",
#         "Lobsters": "https://lobste.rs",
#         "Tech Funding News": "https://techfundingnews.com"
#     }
#     # Website and elements setup with URLs included
#     elements = {
#         "TechCrunch": {
#             "Title": "article header h2",
#             "Details": "article p",
#             "Type": "article .tag",  # Specific type directly from the site
#             "URL": "article header h2 a[href]",
#             "Source": "TechCrunch"
#         },
#         "Crunchbase News": {
#             "Title": "div.news-item h3",
#             "Details": "div.news-item p",
#             "Type": "div.news-item .category",  # Specific type directly from the site
#             "URL": "div.news-item h3 a[href]",
#             "Source": "Crunchbase News"
#         },
#         "YCombinator": {
#             "Title": "tr.athing td.title a",
#             "Details": "tr + tr .subtext",
#             "Type": "tr + tr .subtext .sitebit comhead",  # Infer type from the subtext class, generally "News"
#             "URL": "tr.athing td.title a[href]",
#             "Source": "YCombinator"
#         },
#         "Ars Technica": {
#             "Title": ".article-summary .article-title",
#             "Details": ".article-summary .excerpt",
#             "Type": ".article-summary .meta",  # Specific type directly from the site
#             "URL": ".article-summary .article-title a[href]",
#             "Source": "Ars Technica"
#         },
#         "Slashdot": {
#             "Title": ".story .story-title a",
#             "Details": ".story .body",
#             "Type": ".story .story-category",  # Attempt to infer type from the category class
#             "URL": ".story .story-title a[href]",
#             "Source": "Slashdot"
#         },
#         "Lobsters": {
#             "Title": ".story-liner .u-url",
#             "Details": ".story-liner .tagline",
#             "Type": ".story-liner .tags",  # Tags often serve as a good proxy for type
#             "URL": ".story-liner .u-url[href]",
#             "Source": "Lobsters"
#         },
#         "Tech Funding News": {
#             "Title": ".news-article__title",
#             "Details": ".news-article__summary",
#             "Type": ".news-article__category",  # Using category as type
#             "URL": ".news-article__title a[href]",
#             "Source": "Tech Funding News"
#         }
#     }

    
#     def scrape_site(site, url, elements):
#         scrapper = Parsera(model=llm)
#         results = scrapper.run(url=url, elements=elements[site])
#         for result in results:
#             result['Source'] = site
#         return results

#     all_results = []
#     with ThreadPoolExecutor(max_workers=len(elements)) as executor:
#         futures = [executor.submit(scrape_site, site, url, elements) for site, url in urls.items()]
#         for future in as_completed(futures):
#             all_results.extend(future.result())

#     # Save results
#     with open('scraped_data.json', 'w') as f:
#         json.dump(all_results, f, indent=4)
    
#     return all_results  # Optionally return results for immediate processing

WEBHOOK_URL = "https://webhook.site/7755a0ec-222f-4748-a69a-891838fc85da"

# Function to scrape and categorize
def scrape_and_categorize():
    # Scraping logic
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
    def scrape_site(site, url, elements):
        scrapper = Parsera(model=llm)
        results = scrapper.run(url=url, elements=elements[site])
        for result in results:
            result['Source'] = site
        return results

    all_results = []
    with ThreadPoolExecutor(max_workers=len(elements)) as executor:
        futures = [executor.submit(scrape_site, site, url, elements) for site, url in urls.items()]
        for future in as_completed(futures):
            all_results.extend(future.result())

    # Save results
    with open('scraped_data.json', 'w') as f:
        json.dump(all_results, f, indent=4)

    # Categorization logic
    categories = ["Tech", "Job Openings", "Fundings", "AI", "Security", "Transportation"]
    with open('scraped_data.json', 'r') as f:
        articles = json.load(f)

    def categorize_article(article):
        prompt = f"Given the article title '{article['Title']}' and details '{article['Details']}', return only the category name from the following options: {categories}."
        response = llm.invoke(input=prompt)
        article['Category'] = response.content.strip()
        return article

    categorized_articles = [categorize_article(article) for article in articles]

    # Save the categorized data
    with open('categorized_data.json', 'w') as f:
        json.dump(categorized_articles, f, indent=4)

    # Post to webhook
    requests.post(WEBHOOK_URL, json=categorized_articles)

    return categorized_articles


# Define upload to Qdrant logic
def upload_to_qdrant():
    with open('categorized_data.json', 'r') as f:
        articles = json.load(f)

    for article in articles:
        vector = model.encode(article['Details']).tolist()
        payload = {
            "title": article['Title'],
            "details": article['Details'],
            "type": article['Type'],
            "url": article['URL'],
            "source": article['Source'],
            "category": article['Category']
        }
        qdrant_client.upsert(
            collection_name="tech_news",
            points=[{
                "id": article['URL'],
                "vector": vector,
                "payload": payload
            }]
        )

# Define search logic
def search(query):
    query_vector = model.encode(query).tolist()
    search_results = qdrant_client.search(
        collection_name="tech_news",
        query_vector=query_vector,
        score_threshold=0.5
    )
    formatted_results = [
        {
            'id': result.id,
            'score': result.score,
            'payload': result.payload
        } for result in search_results
    ]
    return formatted_results
