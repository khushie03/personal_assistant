import requests

def fetch_news(api_key):
    api_url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    json_data = requests.get(api_url).json()
    news_list = []

    if "articles" in json_data:
        articles = json_data["articles"]
        for i in range(min(3, len(articles))):  
            title = articles[i]["title"]
            news_list.append(f"Number {i + 1}: {title}")
    else:
        print("Error: No articles found.")
    
    return news_list

