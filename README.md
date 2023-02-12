# ShazamToYoutube
**Program search results may differ from the Shazam CSV data.**

Shazam to YouTube Auto-Adds Playlists.

This is a Python script that reads a CSV file containing song titles and artists and automatically adds the songs to it using the YouTube API with OAuth2 authentication.
* A Google Cloud Platform project with the YouTube Data API v3 enabled
* OAuth2 credentials for the project

1. Install the required Python libraries by running the following command:
```
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pandas
```
2. Follow the instructions on the Google Cloud Platform Console to create a new project and enable the YouTube Data API v3.
3. Create a new set of OAuth2 credentials for the project and download the JSON file. (refer [this](https://www.youtube.com/watch?v=PKLG5pfs4nY) up to 6:58)
4. Rename the JSON file to credentials.json and move it to the project directory.

## Usage
1. Replace SHAZAM_CSV(line 14) with the downloaded Shazam CSV filename.
2. Modify the PLAYLISTID in the code(line 17)

