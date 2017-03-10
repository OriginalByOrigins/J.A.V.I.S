import urllib.request
import ssl
from bs4 import BeautifulSoup as bs

def tracks(command):
    """
    Find a list of songs match based on users' input
    """
    url = 'https://www.musixmatch.com/search/' + command
    # Add header to create a unforbidden access url
    unforbidden_url = urllib.request.Request(
                        url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        soup = get_soup(unforbidden_url)
        results = soup.find_all('div', class_="box-content")[1]
        # Get all relevent songs in a dectionary and return that dict
        #   back for displaying to users.
        tracks = {}
        for li in results.find_all('li', class_="showArtist showCoverart"):
            track_url = li.find('a', class_="title").get('href')[8:]
            if len(track_url) > 64:
                continue
            track_name = (li.find('a', class_="title").text +' by '
                    + li.find('a', class_="artist").text)
            tracks[track_url] = track_name
        return tracks
    except:
        return None

def lyrics(track_url):
    """
    Scrape the lyrics of the song based on the title users chose.
    """
    url = 'https://www.musixmatch.com/lyrics/' + track_url
    # Add header to create a unforbidden access url
    unforbidden_url = urllib.request.Request(
                        url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        soup = get_soup(unforbidden_url)
        lyrics = ''
        lyrics_list = soup.find_all('p', class_="mxm-lyrics__content")
        # Get the whole lyrics by iterate through the returned soup.
        for lyrics_part in lyrics_list:
            lyrics += lyrics_part.text + '\n'
        return lyrics
    except TypeError:
        return None
    except:
        return None

def get_soup(unforbidden_url):
    """
    Get soup of an unforbidden url, using BeautifulSoup4
    """
    try:
        gcontext =  ssl._create_unverified_context()
        sauce = urllib.request.urlopen(unforbidden_url, context=gcontext)
        return bs(sauce.read(), 'html5lib')
    except:
        return None
