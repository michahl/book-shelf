import requests

BASE_URL = "https://openlibrary.org"

def search_by_title(title: str):
    url = f"{BASE_URL}/search.json"
    payload = { 'q': title }

    try:
        response = requests.get(url, params=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print(f'Error fetching data from Open Library: {error}')
        return None
    
def search_by_isbn(isbn: str):
    url = f"{BASE_URL}/search.json"
    payload = { 'isbn': isbn }

    try:
        response = requests.get(url, params=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print(f'Error fetching data from Open Library: {error}')
        return None     

def get_author_details(author_olid: str):
    url = f"{BASE_URL}/authors/{author_olid}.json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:   
        print(f'Error fetching data from Open Library: {error}')
        return None     