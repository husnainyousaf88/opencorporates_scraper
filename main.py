import csv
import time
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import openpyxl

from company import Company


BASE_URL = "https://opencorporates.com"


def scrape(company_name):
    print(f"Downloading... {company_name}")
    encoded_string = quote(company_name).replace("%20", "+")
    url = f"https://opencorporates.com/companies?utf8=%E2%9C%93&utf8=%E2%9C%93&q={encoded_string}&jurisdiction_code=&type=companies"

    options = Options()
    # options.add_argument('--headless')
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    list_items = soup.find("ul", {"id": "companies"}).contents

    result = (company_name, '-', '-', '-', '-', '-', '-', '-', '-')
    if 3 >= len(list_items) > 0:  # if only one result
        link = f"{BASE_URL}{list_items[1].contents[3].attrs['href']}"
        print(link)
        driver.get(link)
        time.sleep(5)

        child_soup = BeautifulSoup(driver.page_source, "html.parser")
        company = Company(soup=child_soup, company_name=company_name)
        result = (company.get_details())

    print(result)
    return result


def read_excel_file(file):
    wb = openpyxl.load_workbook(file)
    sheet = wb.active

    # Skip the header row
    rows = sheet.iter_rows(min_row=2, values_only=True)

    # Extract values from the first column
    return [row[0] for row in rows if row[0] is not None]


def write_csv(data):
    headers = ['Company', 'Name-1', 'Name-2', 'Name-3', 'Name-4', 'Registered Address Street',
               'City', 'Registered Address State', 'Registered Address Zip']

    # Specify the file path
    file_path = 'result.csv'

    # Open the file in write mode and create a CSV writer object
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow(headers)

        # Write the data rows
        writer.writerows(data)


if __name__ == '__main__':
    filename = 'input.xlsx'
    company_names = read_excel_file(filename)

    output = [scrape(c_name) for c_name in company_names]
    write_csv(output)
    print("\n ********* == Execution Completed == ********** ")
    print(f"{len(output)} Records Downloaded")
