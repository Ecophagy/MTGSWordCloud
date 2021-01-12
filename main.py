import requests
from bs4 import BeautifulSoup
from post import Post
from datetime import datetime


def download_posts(game_url, player_name):
    posts = []
    page_number = 1
    last_page = False
    while not last_page:
        page_url = game_url + '?page=' + str(page_number)
        r = requests.get(page_url)
        total_soup = BeautifulSoup(r.content, 'html.parser')

        posts_soup = total_soup.find(id='comments')

        for post_soup in posts_soup.find_all('li', class_='p-comments p-comments-b'):
            poster_name = post_soup.find('span', itemprop='name')
            post_number = post_soup.find('a', class_='j-comment-link')
            date_time_posted = post_soup.find('span', itemprop='dateCreated').get('datetime')

            post_content = post_soup.find('div', class_='j-comment-body-container p-comment-body forum-post-body-content')

            # Remove quotes from the post content
            for quote in post_content.find_all('blockquote', class_='source-quote'):
                quote.decompose()

            post = Post(poster=poster_name.string,
                        content=post_content.text,
                        post_number=int(post_number.string.replace('#', '')),  # Remove prefixing "#"
                        date_time_posted=datetime.strptime(date_time_posted, '%Y-%m-%dT%H:%M:%S'))
            posts.append(post)

        # If you request ?page=x where x > the last page number, you just get back the last page
        # So we check for the absence of the "Next" button
        if total_soup.find('link', rel="next") is None:
            last_page = True
        else:
            page_number = page_number + 1
    pass

if __name__ == '__main__':
    download_posts('https://www.mtgsalvation.com/forums/community-forums/mafia/819846-shoushiling-mafia-day-2', 'TODO')
