#To Identify playlist duration
import os
import re
from datetime import timedelta
from googleapiclient.discovery import build

# Declaring constant variables
api_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' ##this needs to be replaced
youtube = build('youtube', 'v3', developerKey=api_key)

#Extracting hours,minutes,seconds
hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')
#setting total_seconds zero by default
total_seconds = 0
#Bydefault 5 results will be visible in a page, so iterating via a loop
nextPageToken = None #Since its none, first page will be alone will be in the response
while True:
    pl_request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId="PLhiOMqyjVnVHz3IG1B464-3_fgnppl-CO",  ##this needs to be replaced
        maxResults=50,
        pageToken=nextPageToken
    )

    pl_response = pl_request.execute()
    # collecting all video ID's in a list
    vid_ids = []
    for item in pl_response['items']:
        vid_ids.append(item['contentDetails']['videoId'])
    
    vid_request = youtube.videos().list(
        part="contentDetails",
        id=','.join(vid_ids)
    )

    vid_response = vid_request.execute()
    # from response we are getting duration alone
    #e.g PL32M20S
    for item in vid_response['items']:
        duration = item['contentDetails']['duration']
        # using regular expression we are matching the pattern
        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)
        # checking whether the reponse contains hours,minutes,seconds in each response if not the value 0 will be set
        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0
        #converting hours and minutes to seconds
        video_seconds = timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds
        ).total_seconds()

        total_seconds += video_seconds
    #checking whether next page present
    nextPageToken = pl_response.get('nextPageToken')
    # if next page not present, the while loop will break
    if not nextPageToken:
        break
#converting total seconds to int type for conversion
total_seconds = int(total_seconds)
#divmod will provide 
minutes, seconds = divmod(total_seconds, 60)
hours, minutes = divmod(minutes, 60)

print(f'This playlist will prolong for {hours} hours:{minutes} minutes:{seconds} seconds')