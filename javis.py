import time
import telepot
import musixmatch
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


"""
$ python3.6 javid.py <token>

Public on telegram at: t.me/javis_everest_bot

The bot requires users to prompt in a title, an artist name or a line of lyrics.

The bot woll scrape data from Musixmatch and return to users the full lyrics.
"""


def on_chat_message(msg):
    """
    When bot receive a text message from users.
    If the text is:
    - /help or /start: show users the guide to interact with bot.
    - Otherwises, find the songs match user's inputs.
    """
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    # If users prompt in a picture or a video, we can't do anything.
    if content_type != 'text':
        return

    command = msg['text'].lower()

    if command.find('/help') == 0 or command.find('/start') == 0:
        greeting = """Hi there, I'm J.A.V.I.S
I am created by Harrison Cao Thai.

I will help you find the lyrics of whatever songs you want.

Please enter a song tilte, an artist, lines or all of them to search for lyrics.
Example:
    Shape of You : Find lyrics of this song
    Hello by Lionel Richie : Hello performed by Richie, not the one by Adele
    Justin Bieber : Find some popular songs of Justin Bieber
    I'm not looking for somebody : I remember this line was in my favourite song 
    etc.
"""
        bot.sendMessage(chat_id, greeting)
        return None

    # Find the songs users are looking for. 
    tracks = musixmatch.tracks(command.replace(' ', '%20'))

    try:
        if not tracks:
            raise AttributeError

        # Create a list of songs to send back to users
        # The callback_data for each song is the url to that song
        track_list = []
        for track_url, track_name in tracks.items():
            track_list.append([InlineKeyboardButton(
                text=track_name, callback_data=str(track_url))])
    
        markup = InlineKeyboardMarkup(inline_keyboard=track_list)

        # Send back a lists of songs that match users' input
        bot.sendMessage(chat_id, 'Here is a list of songs that match!', reply_markup=markup)
    except AttributeError:
        warning = "Sorry... We can't find any song that match"
        bot.sendMessage(chat_id, warning)

def on_callback_query(msg):
    """
    After send users a list of song, deal with users' choices.
    """
    try:
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        print('Callback Query:', query_id, from_id, query_data)
        # Try to get the lyrics of the song user chose.
        lyrics = musixmatch.lyrics(query_data)
        # Call helper function to send the lyrics to users.
        send_long_lyrics(lyrics, bot, from_id)
    except:
        warning = "Oops... Something's gone wrong. Harry must be working on it!"
        bot.sendMessage(from_id, warning)

def send_long_lyrics(lyrics, bot, from_id):
    """
    Send to users the lyrics after scraping it from musixmatch,
    """
    leng = len(lyrics)
    try:
        # Break lyrics into smaller parts if its length exceeds 4096 chracters.
        if (leng < 4096):
            bot.sendMessage(from_id, lyrics)
            return None;
        
        breakline = lyrics[:4095].rfind('\n')
        if breakline > 0:
            bot.sendMessage(from_id, lyrics[:breakline])
            lyrics = lyrics[breakline+1:]
        else:
            bot.sendMessage(from_id, lyrics[:4095])
            lyrics = lyrics[4096:]

        send_long_lyrics(lyrics, bot, from_id)
    except:
        warning = "Oops... Something's gone wrong. Harry must be working on it!"
        bot.sendMessage(from_id, warning)


TOKEN = '334519609:AAF3l8Z08Efjx8l3qB6pMD7MesNGsTHpl40'
bot = telepot.Bot(TOKEN)

bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
print('Listening....')

while 1:
    time.sleep(10)
