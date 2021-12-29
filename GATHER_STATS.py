# My function called GATHER_STATS() takes a username as input.  It pulls information from a website for that username and returns in into a list called 'listclean' with the neccessary info

import http.client
from sys import exit
import urllib
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from cs50 import get_string


def GATHER_STATS(username):
    # This is the base URL where the user's information for the game is stored
    urlbase = 'https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player='

    # We have to combine the base url with the inputted username to get the actual link that has the information we want
    url = urlbase + username

    # The followign code goes to the url described above and dumps the data into bytes.  https://docs.python.org/3.1/howto/urllib2.html
    req = Request(url)
    try:
        response = urlopen(req)

    # If I can't reach the website, prompt user that the site is invalid and to check the username and then exits the script.
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.  Is the username correct?')
        print('Error code: ', e.code)
        exit()
    # If the site can't be reached, prompt user about High Scores being down and then exits the script.
    except URLError as e:
        print('We failed to reach a server.  The OSRS High Scores are likely down.')
        print('Reason: ', e.reason)
        exit()
   # Otherwise, it reaches the site and reads the respones from the website and puts it in a variable 'datadump' which is bytes
    else:
        datadump = response.read()

    # Our information is currently in bytes which is hard to use.  Convert 'datadump' from bytes into a String variable called 'stringdump'
    stringdump = datadump.decode()

    # We now have a big string called 'stringdump' which has all of our information
    # Convert our information into a list by parsing out information.  Each line of the string corresponds to a Skill and should be a new part of list
    # Store my list in a variable called 'listdump'
    listdump = stringdump.split("\n")

    # The Webpage has a lot of extra information we don't care about.  Here we make a new variable 'listclean' which only includes the first 24 rows
    # These 24 rows correspond to our Total Information, and then each of the 23 skills in the game.
    listclean = listdump[:24]

    # The function list(username) returns the cleaned up list 'listclean' to be used in other functions
    return listclean