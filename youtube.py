from youtube_transcript_api import YouTubeTranscriptApi
import json
import os
from codetiming import Timer

def download_transcribe(video_url):
    
    video_id = video_url.split('=')[-1].strip()
    output_path = f'{video_id}.json'
    if os.path.exists(output_path):
        with Timer(text="Loading local transcript took {:.2f} seconds"):
            with open(output_path, 'r', encoding='utf-8') as fp:
                transcript = json.load(fp)
            return transcript
    
    with Timer(text="Downloading transcript took {:.2f} seconds"):
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        with open(output_path, 'w', encoding='utf-8') as fp:
            json.dump(transcript, fp, indent=4)
            
        return transcript
