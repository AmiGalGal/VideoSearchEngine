import os
import VideoEmbedder
import json


def getFiles(folder):
    allowed = [".mp4"]
    final_list = []

    for root, dirs, files in os.walk(folder):
        for f in files:
            suffix = os.path.splitext(f)[1].lower()
            if suffix in allowed:
                full_path = os.path.join(root, f)
                final_list.append(full_path)

    return final_list

def getVectors(Files):
    vectors = []
    for f in Files:
        vectors.append(VideoEmbedder.VideoVector(f))
    return vectors

def Createjson(VideoVectors, files, output):
    data = []

    for VideoVector, filename in zip(VideoVectors, files):
        data.append({
            "Video-vector": VideoVector,
            "filename": filename
        })
        with open(output, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)


def createDB(Folder):
    name = "lcLihsJnwlIt.json"
    Files = getFiles(Folder)
    vectors = getVectors(Files)
    Createjson(vectors, Files, name)

#createDB(r"C:\Users\amiel\PycharmProjects\PythonProject\SearchEngine\VideoSearchEngine\Videos")