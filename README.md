# Botify
Mastodon Bot that post's your top 10 tracks in the Short, Medium and Long term to the timeline

Check out https://hellsite.site/@goatify for an example!

# Usage

For this you'll need:
 - A spotify developer account, as well as an application. 
 - A mastodon account
 - Python3, including the modules, `mastodonpy` and `spotipy`

Run the export commands with the details from the spotify developer dashboard to add the client details to your env. This might require callback URLs as well
```sh
export SPOTIPY_CLIENT_ID=''
export SPOTIPY_CLIENT_SECRET=''
```

Mastodon token and instance URL can be passed via ENV variables:
```sh
export MASTO_TOKEN='secret'
export MASTO_INSTANCE='https://hellsite.site'
```

# Disclaimer

I wrote this bot as a hack in about an hour. There will be issues, the code is hacky. If you want to help fix them, please do. 

