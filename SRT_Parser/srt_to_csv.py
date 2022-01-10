import re
import pandas as pd
import datetime as dt

def srtParser(path):
    x = []
    ls = []
    format = '%H:%M:%S.%f'
    with open(path, 'r') as f:
        x = f.readlines()
    f.close()
    re_pattern = r'[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9].* -->'
    regex = re.compile(re_pattern)
    times = list(filter(regex.search, x))
    end_times = [time.split(' ')[-1][:-1] for time in times]
    for i in range(len(end_times)):
        end_times[i] = end_times[i][:-4] + "." + end_times[i][-3:]
    start_times = [time.split(' ')[0] for time in times]
    for i in range(len(start_times)):
        start_times[i] = start_times[i][:-4] + "." + start_times[i][-3:]

    lines = [[]]
    for sentence in x:
        if re.match(re_pattern, sentence):
            lines[-1].pop()
            lines.append([])
        else:
            lines[-1].append(sentence)
    lines = lines[1:]
    subs = {start_time:line[0][:-1] for start_time,line in zip(start_times, lines)}

    for i in range(len(lines)):
        start_time = dt.datetime.strptime(start_times[i], format)
        end_time = dt.datetime.strptime(end_times[i], format)
        diff = end_time - start_time
        diffSec = diff.total_seconds()
        ls.append([lines[i][0][:-1], start_times[i], diffSec])
    
    df = pd.DataFrame(ls)
    df.columns = ['Text', 'Start Time', 'Duration']
    df.to_csv("resources/transcript_from_srt.csv", index = False)

srtParser("SRT_Parser/sub.srt")