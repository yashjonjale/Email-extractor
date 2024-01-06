import requests
from bs4 import BeautifulSoup
import re
import csv
from urllib.parse import urlsplit

def extract_emails(url, depth=1, max_depth=4):
   """
   Extracts emails from a given URL and recursively crawls linked pages within the same domain.

   Args:
       url (str): The URL to start crawling from.
       depth (int, optional): The current crawling depth. Defaults to 1.
       max_depth (int, optional): The maximum crawling depth. Defaults to 4.
   """

   emails = set()  # Use a set to avoid duplicates

   try:
       response = requests.get(url)
       response.raise_for_status()  # Raise an exception for non-200 status codes

       soup = BeautifulSoup(response.content, "html.parser")

       # Extract emails from the current page
       for email in soup.find_all(text=re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")):
           emails.add(email.strip())
    #    for email in soup.find_all(text=re.compile(r"[\w\.-]+at[\w\.-]+dot\w+")):
    #        emails.add(email.strip())
       # Recursively crawl linked pages within the same domain
       if depth < max_depth:
           for link in soup.find_all("a"):
               href = link.get("href")
               if href and is_same_domain(url, href):
                   emails.update(extract_emails(href, depth + 1, max_depth))

   except requests.exceptions.RequestException as e:
       print(f"Error fetching URL: {url}\n{e}")

   return emails

def is_same_domain(url1, url2):
   """
   Checks if two URLs belong to the same domain.
   """

   parsed_url1 = urlsplit(url1)
   parsed_url2 = urlsplit(url2)
   return parsed_url1.netloc == parsed_url2.netloc

def main():
   start_url = input("Enter the URL to start crawling: ")
   max_depth = int(input("Enter the maximum crawling depth (optional, defaults to 1): ") or 1)

   emails = extract_emails(start_url, max_depth=max_depth)
   emails = list(emails)
   print(emails)
   with open("extracted_emails.txt", "w") as textfile:
        for email in emails:
            textfile.write(email + "\n")

   print("Emails have been extracted and saved to extracted_emails.txt")

if __name__ == "__main__":
   main()
