import pandas as pd
import requests
import time
from tqdm import tqdm

# Load CSV with titles
df = pd.read_csv("Book3.csv")

# Prepare output dataframe
results = []

for title in tqdm(df['Title']):
    search_query = "+".join([i for i in title.split(" ")])
    url = f"https://api.semanticscholar.org/graph/v1/paper/search/bulk?query={search_query}&limit=1&fields=title,authors,year,venue,url"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            paper = data["data"][0]
            results.append({
                "title": paper.get("title"),
                "authors": ", ".join(a['name'] for a in paper.get("authors", [])),
                "year": paper.get("year"),
                "venue": paper.get("venue"),
                "doi": paper.get("doi"),
                "url": paper.get("url")
            })
    else:
        results.append({
            "title": title,
            "authors": "",
            "year": "",
            "venue": "",
            "doi": "",
            "url": ""
        })
    
    time.sleep(0.5)  # Avoid rate limits

# Save to new CSV
pd.DataFrame(results).to_csv("titles_with_metadata3.csv", index=False)
print("Done! Saved to titles_with_metadata.csv")