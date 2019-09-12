import mastodon
import pprint
import sys

import spotipy
import spotipy.util as util
import simplejson as json

from mastodon import Mastodon
mastodon = Mastodon(
    access_token = "", #Enter Bot Access Token
    api_base_url = "", #Instance URL
)

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

#We grab token using prompts bcs its easier than tokens. you need to run
# export SPOTIPY_CLIENT_ID=''
# export SPOTIPY_CLIENT_SECRET=''


scope = 'user-top-read'
token = util.prompt_for_user_token(username, scope) #We need a small ass scope

orig_stdout = sys.stdout #Save orig stdout to avoid any errors lol

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    ranges = ['short_term', 'medium_term', 'long_term'] #If you only want to post short / medium / long remove them from this list.
    for range in ranges:
        outputname = range+".txt"
        sys.stdout = open(outputname, "w+")
        results = sp.current_user_top_tracks(time_range=range, limit=10) #We can change the limit easily
        for i, item in enumerate(results['items']):
            print(i+1, ':' , item['name'], '//', item['artists'][0]['name']) #hack

sys.stdout.close()
sys.stdout=orig_stdout 

ranges_nice = ["Short Term", "Medium Term", "Long Term"]
j = 0
for range in ranges:
    filename = range+".txt"
    with open(filename, "r") as file:
        data = file.read() #Hackier
    mastodon.status_post(ranges_nice[j]+ "\n" + data) 
    j = j + 1

