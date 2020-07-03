import requests
from bs4 import BeautifulSoup as bs
import re
import time
import os


# Make the patterns that we'll need for filtering
gr_ptrn = re.compile(r'[αεοιηυάέίόήύ]')
ws_ptrn = re.compile(r'\s')
isbn_ptrn = re.compile(r'\d{10}|\d{13}')


def get_isbn():
    isbns = []
    while True:
        isbn = input(
            "Please enter valid ISBN numbers(Only 10 or 13 digits)" +
            "\nand press 'c' to continue:\n"
        ).strip()
        # Try to match the full string with the desired pattern
        if re.fullmatch(isbn_ptrn, isbn):
            isbns.append(isbn)
        if isbn == 'c':
            break
        isbn = ''
    return isbns


def get_page(base_url, data):
    try:
        r = requests.get(base_url, params=data)
    except Exception as e:
        r = None
        print(f"Server responded: {e}")
    return r


def get_editions_details(isbn):
    # Create the search URL with the ISBN of the book
    data = {'q': isbn}
    book_url = get_page("https://www.goodreads.com/search", data)
    # Parse the markup with Beautiful Soup
    soup = bs(book_url.text, 'lxml')

    # Retrieve from the book's page the link for other editions
    # and the total number of editions
    ed_item = soup.find("div", class_="otherEditionsLink").find("a")
    ed_link = f"https://www.goodreads.com{ed_item['href']}"
    ed_num = ed_item.text.strip().split(' ')[-1].strip('()')

    # Return a tuple with all the informations
    return ((ed_link, int(ed_num), isbn))


def get_editions_urls(ed_details):
    # Unpack the tuple with the informations about the editions
    url, ed_num, isbn = ed_details

    # Navigate to all pages for books with more than 100 editions
    for page in range((ed_num // 100) + 1):
        r = requests.get(url, params={
            'page': str(page + 1),
            'per_page': '100',
            'filter_by_format': 'Paperback',
            'utf8': "%E2%9C%93"})

        soup = bs(r.text, 'lxml')

        # Find all elements for the editions of the book
        editions = soup.find_all("div", class_="editionData")

        # Search for greek editions
        with open(f"urls_files/{isbn}_urls.txt", 'a') as fp:
            for book in editions:
                item = book.find("a", class_="bookTitle")
                # Look if this is an edition in the chosen language
                if re.search(gr_ptrn, item.text):
                    rating = book.find_all("div", class_="dataValue")[-1].text
                    rating = re.sub(ws_ptrn, '', rating)
                    # Write the url of the edition and the rating in the file
                    fp.write(f"https://www.goodreads.com{item['href']}" +
                             f"  rating: {rating}\n")
        # Let some time to the goodreads server between the requests
        time.sleep(2)


if __name__ == "__main__":
    # Make the folder for the url files
    try:
        os.mkdir('./urls_files')
    except Exception:
        pass

    # Get the ISBNs from the user
    isbns = get_isbn()

    # Check all the ISBNs
    for isbn in isbns:
        ed_details = get_editions_details(isbn)
        get_editions_urls(ed_details)
