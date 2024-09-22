import requests
from bs4 import BeautifulSoup
import os
import re
import chardet


files_directory = 'files'
os.makedirs(files_directory, exist_ok=TRUE) #create directory if it doesnt already exist


#make sure the scraper creates a scraped_urls txt file to read from
def load_scraped_urls(file_path):
    #create a set of those urls
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            return set(line.strip() for line in file)
    return set()

#helper function to save any new scraped urls
def save_scraped_url(url, file_path):
    with open(file_path, 'a', encoding="utf-8") as file:
        file.write(url + "\n")

def scrape_articles():
    
    
    scraped_urls_file = os.path.join(files_directory, 'scraped_urls.txt')

    #set of scraped urls
    scraped_urls = load_scraped_urls(scraped_urls_file)

    #baseURL for the website we want to scrape
    baseURL = "https://cnn.com"
    #grab the specific page of articles you want
    response = requests.get('https://www.cnn.com/world/middleeast/israel')
    soup = BeautifulSoup(response.text.encode("utf-8"), "html.parser")
    
    #make sure to get the website-specific div that contains all the relevant articles
    parent_div = soup.find("div", class_="container__field-links container_lead-plus-headlines-with-images__field-links")
    
    #get the links to those articles
    child_as = parent_div.find_all("a")
    
    #Loop through all those links
    for a in child_as:
        #if article found, this is also website-specific
        if a.find("div", class_="container__text container_lead-plus-headlines-with-images__text"):

            #url to the article
            url = baseURL + a['href']
            #if already in our list of scraped_urls, you can skip it
            if url in scraped_urls:
                continue


            page = requests.get(baseURL + a['href'])
            pageSoup = BeautifulSoup(page.text.encode("utf-8"), "html.parser")
            paragraphs_of = pageSoup.find_all("p", attrs={"data-component-name": "paragraph"})

            #create a clean title and a clean filename
            title = (pageSoup.find('title').text)
            clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
            print("clean title is: " + clean_title)

            filename = title + ".txt"
            clean_filename = re.sub(r'[\\/*?:"<>|\s+]', "", filename)
            filepath = os.path.join(files_directory, clean_filename)
            print("clean filename is: " + filepath)
            #write the article paragraph by paragraph
            with open(filepath, 'w', encoding="utf-8") as file:
                file.write(title + '\n')
                for p in paragraphs_of:
                    file.write(p.get_text() + '\n')  # Write each paragraph to the file
                file.write(url + "\n")
            save_scraped_url(url, scraped_urls_file)

scrape_articles()








