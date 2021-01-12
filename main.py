import requests
from bs4 import BeautifulSoup
from post import Post


def download_posts(game_url, player_name):
    r = requests.get(game_url)
    total_soup = BeautifulSoup(r.content, 'html.parser')

    posts_soup = total_soup.find(id='comments')

    posts = []
    for post_soup in posts_soup.find_all('li', class_='p-comments p-comments-b'):
        poster_name = post_soup.find('span', itemprop='name')
        post_content = post_soup.find('div', class_='j-comment-body-container p-comment-body forum-post-body-content')
        post = Post(poster=poster_name.string, content=post_content.text)
        posts.append(post)

if __name__ == '__main__':
    download_posts('https://www.mtgsalvation.com/forums/community-forums/mafia/819846-shoushiling-mafia-day-2', 'TODO')
