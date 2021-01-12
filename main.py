import requests
from bs4 import BeautifulSoup
from post import Post
from datetime import datetime
import argparse
from wordcloud import WordCloud, STOPWORDS
from os import path


def download_posts(game_url, player_list=None):
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

            # Add post to our list if it matches a player we care about
            # Empty list means we want everyone
            if player_list is None or poster_name.string in player_list:
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
    return posts


def combine_posts(posts):
    concatenated_posts = ""
    for post in posts:
        concatenated_posts = concatenated_posts + post.content
    return concatenated_posts


def generate_word_cloud(text):
    stopwords = set(STOPWORDS)  # Ignore common english words like "a", "an", "the"
    wc = WordCloud(background_color="white",
                   max_words=200,
                   stopwords=stopwords)
    wc.generate(text)
    wc.to_file(path.join(path.dirname(__file__), "wordcloud.png"))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("thread", help="full link to thread to parse")
    parser.add_argument('-p', '--players', nargs='*', help='list of player names to word cloud. Names with spaces in must be wrapped in quotes. Leave empty for all players.')

    args = parser.parse_args()
    if args.players:
        player_list = args.players
    else:
        player_list = None

    posts = download_posts(args.thread, player_list)
    raw_data = combine_posts(posts)
    generate_word_cloud(raw_data)
