# Mind Map Generator

This is a simple MindMap Generator which has modular code i.e. you can switch the different components. The frontend for the API is present in another repository under the same organization name

The API is located [here](https://github.com/ZoneIn-MindMaps/MindMapGenerator/blob/main/Pipeline/app.py) and has 2 endpoints one where you can specify a youtube video id and one where you specify a file name whose location is currently an absolute path but can be changed easily inside the code. The saved srt file is saved at the location and renamed using the react frontend

Currently the model uses networkx and wordcloud to generate the mindmap and wordclusters

The model uses SOTA embeddings for vectorizing text and then performs clustering on it. The default clustering algorithm currently is K Means however it can we swapped inside the code easily for any other model of choice

The other files are used as imports or were a part of testing
