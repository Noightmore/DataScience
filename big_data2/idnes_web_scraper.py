import requests
from bs4 import BeautifulSoup
import os


# Function to scrape an article
def scrape_article(article_url, data_dir):
    response = requests.get(article_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        article_name = soup.find('h1', class_='article-title').text
        article_content = soup.find('div', class_='article-content').text

        # Create a directory to store scraped data if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)

        # Save the scraped data to a text file
        output_filename = f'{article_name}.txt'
        with open(os.path.join(data_dir, output_filename), 'w', encoding='utf-8') as file:
            file.write(f'Article Name: {article_name}\n')
            file.write(f'Article Content: {article_content}\n')

        print(f'Data from {article_url} has been scraped and saved to {output_filename}')
    else:
        print(f'Failed to retrieve data from {article_url}. Status code: {response.status_code}')


# Function to crawl and scrape articles
def crawl_and_scrape(url, data_dir, depth_limit, data_volume_limit, current_data_volume):
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Failed to retrieve data from {url}. Status code: {response.status_code}')
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    article_links = soup.find_all('a', class_='article-link')

    for link in article_links:
        article_url = link.get('href')
        article_url = 'https://www.idnes.cz' + article_url

        if current_data_volume >= data_volume_limit:
            print(f'Data volume limit of 1 GB reached.')
            return

        scrape_article(article_url, data_dir)
        current_data_volume += os.path.getsize(os.path.join(data_dir, f'{link.text}.txt'))

    if depth_limit > 0:
        next_page_link = soup.find('a', class_='next-page')
        if next_page_link:
            next_page_url = 'https://www.idnes.cz' + next_page_link.get('href')
            crawl_and_scrape(next_page_url, data_dir, depth_limit - 1, data_volume_limit, current_data_volume)


if __name__ == '__main__':
    start_url = 'https://www.idnes.cz/'

    data_directory = 'scraped_data'
    depth_limit = 3  # Depth of crawling
    data_volume_limit = 1024 * 1024 * 1024  # 1 GB data volume limit

    crawl_and_scrape(start_url, data_directory, depth_limit, data_volume_limit, 0)
