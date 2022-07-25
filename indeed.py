from bs4 import BeautifulSoup
import requests
import csv
from time import sleep
from random import randint
from datetime import datetime

def get_url(position, location):
        template = 'https://www.indeed.com/jobs?q={}&l={}'
        url = template.format(position, location)
        return url

def get_record(card):
    '''Extract job date from a single record '''
    atag = card.h2.a
    try:
        job_title = atag.get('title')
    except AttributeError:
        job_title = ''
    try:
        company = card.find('span', 'companyName').text.strip()
    except AttributeError:
        company = ''
    try:
        location = card.find('div', 'companyLocation').text.strip()
    except AttributeError:
        location = ''
    try:
        job_summary = card.find('div', 'job-snippet').text.strip()
    except AttributeError:
        job_summary = ''
    try:
        post_date = card.find('span', 'date').text.strip()
    except AttributeError:
        post_date = ''
    try:
        salary = card.find('div', 'salary-snippet-container').text.strip()
    except AttributeError:
        salary = ''
    
    extract_date = datetime.today().strftime('%Y-%m-%d')
    job_url = 'https://www.indeed.com' + atag.get('href')
    
    return (job_title, company, location, job_summary, salary, post_date, extract_date, job_url)

def main(position, location):
    # Run the main program reouting
    records = []  # creating the record list
    url = get_url(position, location)  # create the url while passing in the position and location.
    
    while True:
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', 'cardOutline')

        for card in cards:
            record = get_record(card)
            records.append(record)

        try:
            url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
            delay = randint(1, 10)
            sleep(delay)
        except AttributeError:
            break

    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Job Title', 'Company', 'Location', 'Salary', 'Posting Date', 'Extract Date', 'Summary', 'Job Url'])
        writer.writerows(records)


print(main('junior developer', 'boston, ma'))
