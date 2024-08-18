import os
import json
from langchain_openai import AzureChatOpenAI
# Load environment variables and initialize AzureChatOpenAI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv("app.env"))

# Initialize your language model client
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    openai_api_version=os.getenv("AZURE_API_VERSION"),
    deployment_name=os.getenv("DEPLOYMENT_NAME"),
    openai_api_key=os.getenv("AZURE_API_KEY"),
    openai_api_type=os.getenv("API_TYPE"),
    temperature=0.0,
)

# Load scraped data
with open('scraped_data.json', 'r') as f:
    articles = json.load(f)

# Define categories and categorization function
categories = ["Tech", "Job Openings", "Fundings", "AI", "Security", "Transportation"]

def categorize_article(article):
    # Define a prompt that asks directly for a single category label
    prompt = f"Given the article title '{article['Title']}' and details '{article['Details']}', return only the category name from the following options: {categories} and not even a single word other than the category like only give one word answer. and if not able to match the given with any of the category than mark it as 'unknown'"
    
    # Invoke the model
    response = llm.invoke(input=prompt)
    print(response)
    # The model should respond with only the category name, so we take that directly
    # Assume response.content holds the string that is the category name
    article['Category'] = response.content.strip()
    
    return article


# Categorize all articles
categorized_articles = [categorize_article(article) for article in articles]

# Save the categorized data
with open('categorized_data.json', 'w') as f:
    json.dump(categorized_articles, f, indent=4)
