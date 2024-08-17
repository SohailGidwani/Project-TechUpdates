# import pprint
# import os
# from langchain_openai import AzureChatOpenAI
# from parsera import Parsera

# llm = AzureChatOpenAI(
#     azure_endpoint=os.getenv("AZURE_ENDPOINT"),
#     openai_api_version=os.getenv("AZURE_API_VERSION"),
#     deployment_name=os.getenv("DEPLOYMENT_NAME"),
#     openai_api_key=os.getenv("AZURE_API_KEY"),
#     openai_api_type=os.getenv("API_TYPE"),
#     temperature=0.0,
# )

# url = "https://news.ycombinator.com/"
# elements = {
#     "Title": "News title",
#     "Points": "Number of points",
#     "Comments": "Number of comments",
# }

# scrapper = Parsera(model=llm)
# result = scrapper.run(url=url, elements=elements)

# pprint.pprint(result)  # Using pprint for better formatting


import os
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
    "Title": "tr.athing td.title a",  # Targets only the title link within each post's main row
    "Details": "tr + tr .subtext",     # Correctly targets the subtext row that follows each title row
    "Points": "tr + tr .subtext span.score"  # Specifically targets the points element in the subtext
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

# Loop through each website and scrape
for site, url in urls.items():
    print('\n\n')
    scrapper = Parsera(model=llm)
    result = scrapper.run(url=url, elements=elements[site])
    print(f"Results from {site}:")
    for item in result:
        print(item)
