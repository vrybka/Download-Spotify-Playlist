
from spotapi import PublicPlaylist
import yt_dlp
from youtubesearchpython import VideosSearch
import re
import sys

def extract_uri(url):
    match = re.search(r"playlist/([A-Za-z0-9?=&]+)", url)
    return match.group(1) if match else None

def find_url_of_first_search_result(searchInput):
    videosSearch = VideosSearch(searchInput, limit = 1)
    result = videosSearch.result()
    searchResult = result["result"]
    resultDict = searchResult[0]
    url = resultDict['link']
    return url

def download_video(url, title):
    ydl_opts = {
    'format': 'bestaudio',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    # 'outtmpl': '%(title)s.%(ext)s'
    'outtmpl': title
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])      

def main(argv):
    playlist_url = argv[1] # playlist link provided as argument
    print("Starting Download....")
    
    # extracting uri from playlist url
    uri = extract_uri(playlist_url)

    # getting playlist info
    p = PublicPlaylist(uri)
    playlist = p.get_playlist_info(limit=5000)
    songs=[]
    total_tracks = playlist["data"]["playlistV2"]["content"]["totalCount"]

    # getting song's artist and name
    for i in range(0,total_tracks):
        name = playlist["data"]["playlistV2"]["content"]["items"][i]["itemV2"]["data"]["name"]
        artist = playlist["data"]["playlistV2"]["content"]["items"][i]["itemV2"]["data"]["artists"]["items"][0]["profile"]["name"]
        songs.append(artist + " - " + name)

    errors = []
    for i in range(0,total_tracks):
        try:
            # searching for song
            url = find_url_of_first_search_result(songs[i])
            # downloading song
            download_video(url, songs[i])
            print("----------------",i+1," out of ",total_tracks," songs downloaded----------------")
        except:
            print("Error occcured when downloading.")
            print("Skip and continue.")
            errors.append(songs[i])
            continue
            
    print("Done!")
    print()
    if errors:    
        print("Oops! The download gods have refused to bless the following songs.. ")
        for i in range(0,len(errors)):
            print(errors[i]) 

if __name__=="__main__":
    main(sys.argv)