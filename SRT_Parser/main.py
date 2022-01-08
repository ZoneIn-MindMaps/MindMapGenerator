from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
ls = YouTubeTranscriptApi.get_transcript("vxFYfumAAlY")
ls2 = []
with open("transcript.txt", "w") as f:
    for i in ls:
        f.write("Text " + str(i['text']).replace("\n","") + " Start Time " + str(i['start']) + " Duration " + str(i['duration']) + "\n")
        ls2.append([i['text'].replace("\n","") , i['start'] , i['duration']])
df = pd.DataFrame(ls2)
df.columns =['Text', 'Start Time', 'Duration']
df.to_csv("transcript.csv", index=False)