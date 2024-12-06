import requests
from bs4 import BeautifulSoup
import json

# URL of the Scopus record
url = "https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=85207964401&origin=inward"

# Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
}

# Send the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract the title
    title = soup.title.text.strip()
    
    # Find the section with id="abstractSection"
    abstract_section = soup.find("section", id="abstractSection")

    # Extract the text from the <p> tag
    abstract = abstract_section.find("p").text.strip() if abstract_section else "Abstract not found"

# 

    # Save the extracted title to a JSON file
    data = {
        "title": title ,
        "abstract": abstract
    }
    
    # Save soup content to a .txt file
    # with open("soup_output.txt", "w", encoding="utf-8") as file:
    #     file.write(soup.prettify())
        
    # print("Soup content saved to soup_output.txt")
        
    with open("scopus_results.json", "w", encoding="utf-8") as json_file:
      json.dump(data, json_file, ensure_ascii=False, indent=4)

    print("Title saved to scopus_title.json")
    
else:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")


