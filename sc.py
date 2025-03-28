import requests              # for making HTTP requests
import pandas as pd             # for data manipulation
from bs4 import BeautifulSoup     # for web scraping
from datetime import datetime, time       # for timestamp

url = "https://realpython.github.io/fake-jobs/"

html_content = requests.get(url).text   # Get the raw HTML content  # Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")   # Parse the HTML content    # Get the main tag that contains the job postings

jobs = soup.find_all("div", class_="column is-half")   # Create a list to store the job postings

job_list = []   # Loop through the job postings and extract relevant information
for job_element in jobs:

    # Extract job title
    job_title = job_element.find("h2", class_="title").text.strip()
    
    # Extract company name
    company_name = job_element.find("h3", class_="subtitle").text.strip()
    
    # Extract location (city and state)
    location = job_element.find("p", class_="location").text.strip()
    city, state = location.split(", ")
    
    # Extract and process the date posted
    date_posted_str = job_element.find("time")["datetime"]
    date_posted = datetime.strptime(date_posted_str, "%Y-%m-%d")
    days_months_weekdays = date_posted.strftime("%A, %d %B")  # e.g., "Thursday, 8 April"
    year = date_posted.year  # e.g., 2021

    # Append the extracted data to the list of dictionaries
    job_description = job_element.find("div", class_="content").text.strip()    # Store the information in a dictionary
    job_dict = {
        "job_title": job_title,
        "company_name": company_name,
        "city": city,
        "state": state,
        "days_months_weekdays": days_months_weekdays,
        "year": year,
    }
    job_list.append(job_dict)   # Convert the list of dictionaries into a DataFrame
df = pd.DataFrame(job_list)   # Display the DataFrame
print(df)
# Save the DataFrame to a CSV file
df.to_csv("fake_jobs.csv", index=False)
