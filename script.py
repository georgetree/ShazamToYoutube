import csv
import re
import time
import requests
import pandas as pd
from time import sleep
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

SHAZAM_CSV = 'shazamlibrary.csv'
URL_LIST = 'url_list.csv'
EXISTED_FILE_PATH = 'existed_url.csv'
PLAYLISTID = 'Your playlist ID can be found in the URL following the equals sign. ex:playlist?list=xxx Modify the variable to xxx. '
OAUTHJSON = 'credentials.json'
# def fetch_data():
#     csv_file_path = SHAZAM_CSV
#     df = pd.read_csv(csv_file_path,skiprows=1)
#     videos = [{"title": title, "artist": artist} for title, artist in zip(df["Title"], df["Artist"])]
#     return videos
 
def search_url():
    csv_file_path = SHAZAM_CSV
    df = pd.read_csv(csv_file_path,skiprows=1)
    videos = [{"title": title, "artist": artist} for title, artist in zip(df["Title"], df["Artist"])]
   

    with open(URL_LIST, 'w', newline='') as output_file:
        # fieldnames = ['Video-URL']
        # csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        csv_writer = csv.writer(output_file)

        # csv_writer.writeheader()

        for v in videos:
            query = f"{v['artist']} {v['title']}"
            search_url = f"https://www.youtube.com/results?search_query={query}"
            response = requests.get(search_url)
            html = response.text

            # 提取第一個影片的網址
            pattern = r'/watch\?v=([^"]+)+"'
            matches = re.search(pattern, html)
            
            if matches:
                a = matches[0]
                csv_writer.writerow([a[9:20]])
            sleep(0.1)
    # 讀取CSV文件到DataFrame中
    df = pd.read_csv(URL_LIST)

    # 刪除重複的資料
    df.drop_duplicates(inplace=True)
    df.to_csv(URL_LIST, index=False)
def add_playlist():
    SCOPES = ["https://www.googleapis.com/auth/youtube"]


    # Define the YouTube API credentials file path
    creds = None

    # Define the YouTube API version
    API_VERSION = "v3"

    # Define the YouTube API service name
    API_SERVICE_NAME = "youtube"
    RETRY_INTERVAL = 60

    # Authenticate with the YouTube API using OAuth2
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                OAUTHJSON, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Create the YouTube API client
    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=creds)

    # 已經寫入過的資料 放入urls
    urls = []
    if os.path.isfile(EXISTED_FILE_PATH):
        with open(EXISTED_FILE_PATH, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                urls.append(row[0])

    with open(URL_LIST, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # next(csv_reader)
        for cv in csv_reader:
            print(cv[0])
            playlist_item_body = {
                "snippet": {"playlistId": PLAYLISTID, "resourceId": {"kind": "youtube#video", "videoId": cv[0]}}
            }
            playlist_item_request = youtube.playlistItems().insert(part="snippet", body=playlist_item_body)
            if cv[0] not in urls:
                try:
                    playlist_item_response = playlist_item_request.execute()
                    with open(EXISTED_FILE_PATH, 'a', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow([cv[0]])

                except HttpError as error:
                    if error.resp.status in [403, 500, 503]:
                        # Handle rate limit or server errors
                        print(f"An error occurred: {error}")
                        print(f"Retrying in {RETRY_INTERVAL} seconds...")
                        time.sleep(RETRY_INTERVAL)
                        playlist_item_response = playlist_item_request.execute()
                        with open(EXISTED_FILE_PATH, 'a', newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            writer.writerow([cv[0]])
                    else:
                        print(cv[0])
                        continue
if __name__ == '__main__':
    print("search start")
    search_url()
    print("search end")
    print("-------------------")
    print("insert playlist start")
    add_playlist()
    print("insert playlist end")
