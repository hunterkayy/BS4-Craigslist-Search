# Generates url from Cars.txt. Cars.txt determines the scope of search
# List your search in Cars.txt as follows: Make, Model, Minimum Price, Maximum Price, Miles range
# Scrapes html of search results page
# grabs "title", "price", and "url" of each listing
# Exports the scraped information to an Excel spreadsheet
from bs4 import BeautifulSoup
import requests
import openpyxl

global url, soup, results, postal, make, model, minimum, maximum, file_name1, file_name2
results = []
url_base = "https://baltimore.craigslist.org/search/cta?purveyor=owner&hasPic=1"


def generate_url():
    global url, postal, make, model, minimum, maximum, file_name1, file_name2

    with open('Cars.txt') as f:
        lines = f.readlines()

    for i in range(0, 5):
        info = lines[i]
        info_p = str(info[:-1])

        if i == 0:
            file_name1 = info_p
            make = "&auto_make_model=" + info_p

        if i == 1:
            file_name2 = info_p
            model = "+" + info_p

        if i == 2:
            minimum = "&min_price=" + info_p

        if i == 3:
            maximum = "&max_price=" + info_p

        if i == 4:
            postal = "&postal=" + info_p

    url = url_base + postal + minimum + maximum + make + model


def get_page():
    global soup

    # todo make bot look human

    headers_agents = ({'User-Agent':
                           'Mozilla/5.0 (X11; Linux x86_64)'
                           'AppleWebKit/537.36 (KHTML, like Gecko)'
                           'Chrome/44.0.2403.157 Safari/537.36',
                           'Accept-Language': 'en-US, en;q=0.5'})

    web_page = requests.get(url, headers=headers_agents)
    soup = BeautifulSoup(web_page.text, "html.parser", )


def scrape_page():
    search1 = soup.find(id="search-results")
    search2 = search1.find_all("li")
    result_range = (len(search2))

    for i in range(0, result_range):
        global results
        title = (search2[i]).find("a", {"class": "result-title"})
        price = (search2[i]).find("span", {"class": "result-price"})
        link = title["href"]
        title_string = title.string
        price_string = price.string
        test = [title_string, price_string, link]
        results.append(test)


def export_results():
    global results
    result_range = len(results)
    new_file = file_name1 + " " + file_name2 + ".xlsx"
    path = "C:/Users/My Social Atlas/OneDrive - Social Atlas/Python/"
    template = path + "Book.xlsx"
    wb1_obj = openpyxl.load_workbook(template)
    sheet1 = wb1_obj.active

    for i in range(0, result_range):
        sheet1.append(results[i])

    wb1_obj.save(filename=path + new_file)


generate_url()
get_page()
scrape_page()
export_results()
print(url)

