import numpy as np
import VideoEmbedder
import torch
import os

def load_json(file_path):
    import json
    import numpy as np
    import torch

    vectors = []
    filenames = []

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        vec = np.array(item["Video-vector"], dtype=np.float32)
        vectors.append(torch.tensor(vec))
        filenames.append(item["filename"])

    return vectors, filenames

def covert(vector):
    if hasattr(vector, "pooler_output"):
        vector = vector.pooler_output

    if torch.is_tensor(vector):
        vector = vector.detach().cpu().numpy()

    vector = np.array(vector).tolist()
    return torch.tensor(vector)

def FindBest(vectors, filenames, query):
    length = len(filenames)
    queryVec = covert(VideoEmbedder.TextToVector(query))
    scores = []
    indexes = []
    for i in range(0, length):
        VideoScore = VideoEmbedder.similarity(queryVec, vectors[i])
        scores.append(VideoScore)
        indexes.append(i)
    sortedIdx = sorted(zip(scores, indexes), reverse=True)
    scores, indexes = zip(*sortedIdx)
    return indexes

def search(query, DB= "lcLihsJnwlIt.json", top = 1):
    v,f = load_json(DB)
    q = query
    bi = FindBest(v,f,q)
    print(bi)
    files = []
    top = min(top, len(bi))
    for i in range(top):
        files.append(f[bi[i]])

    return files
