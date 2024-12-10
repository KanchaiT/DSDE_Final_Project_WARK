from scholarly import scholarly
import pandas as pd

# Function to scrape metadata from Google Scholar
def scrape_google_scholar(query, max_results=1000):
    results = []
    count = 0
    
    print(f"Fetching up to {max_results} results for query: '{query}'")
    
    # Search Google Scholar for the query
    search_query = scholarly.search_pubs(query)
    
    # Iterate through the results
    for result in search_query:
        if count >= max_results:
            break
        try:
            paper = {
                "title": result.get("bib", {}).get("title", None),
                "author": result.get("bib", {}).get("author", None),
                "journal": result.get("bib", {}).get("journal", None),
                "year": result.get("bib", {}).get("pub_year", None),
                "abstract": result.get("bib", {}).get("abstract", None),
                "url": result.get("eprint_url", None),
                "citations": result.get("num_citations", None),
            }
            results.append(paper)
            count += 1
            print(f"Scraped {count}/{max_results}: {paper['title']}")
        except Exception as e:
            print(f"Error processing result: {e}")
    
    # Save results to a CSV file
    df = pd.DataFrame(results)
    df.to_csv("google_scholar_results.csv", index=False)
    print(f"Scraping completed. Data saved to 'google_scholar_results.csv'")
    
    return df

# Example usage
if __name__ == "__main__":
    query = "machine learning in engineering"
    data = scrape_google_scholar(query, max_results=1000)