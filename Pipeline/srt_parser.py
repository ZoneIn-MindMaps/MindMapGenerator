from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd

def get_transcript(video_id):
    ls = YouTubeTranscriptApi.get_transcript(video_id)
    ls2 = []
    for i in ls:
        ls2.append([i['text'].replace("\n","") , i['start'] , i['duration']])
    df = pd.DataFrame(ls2)
    df.columns =['Text', 'Start Time', 'Duration']
    df.to_csv("transcript.csv", index=False)

if __name__ == '__main__':
    get_transcript("eJ-WJssJgdg")