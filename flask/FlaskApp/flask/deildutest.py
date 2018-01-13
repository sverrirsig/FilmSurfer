from bs4 import BeautifulSoup
import requests
import urllib.request
import os


url_root = 'http://afghanpirate.com/'
url_login = 'http://afghanpirate.com/takelogin.php'
url_top_movies = 'http://afghanpirate.com/browse.php?cat=6&sort=seeders&type=desc'

payload_login = {
    'username': 'jobs',
    'password': 'coolguys2083'
}

def get_page(url):
    r = s.get(url)
    data = r.text
    return BeautifulSoup(data, 'lxml')

with requests.Session() as s:
    r = s.post(url_login, data=payload_login)
    r = s.get(url_top_movies)
    data = r.text

    soup = BeautifulSoup(data, 'lxml')

    #print(soup.prettify())

    body_element = soup.find('table', {'class': 'torrentlist'})
    movies = body_element.find_all('td', {'align': 'left'})
    for movie in movies[3:]:
        if movie.a is not None and movie.a.b is not None:
            name = movie.a.b.text
            link = movie.a['href']
            id = link.split('=')[1]

            print("Name: %s" % name)
            print("Link: %s" % link)
            print(url_root + link)
            torrent_page = get_page(url_root + link)

            download_link = torrent_page.find('a', {'class': 'index'})['href']
            full_link = url_root + download_link
            print(full_link)
            r = s.get(full_link)

            with open('/home/sverrir/Desktop/FilmSurfer/torrents/' + id + '.torrent', 'wb') as f:
                f.write(r.content)

            print("transmission-cli -w /home/sverrir/Desktop/FilmSurfer/torrents_ready/"
                      + " " + '/home/sverrir/Desktop/FilmSurfer/torrents/' + id + '.torrent')
            os.system("transmission-cli -w /home/sverrir/Desktop/FilmSurfer/torrents_ready/"
                      + " " + '/home/sverrir/Desktop/FilmSurfer/torrents/' + id + '.torrent')

            break
