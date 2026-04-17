import cv2
import torch
from transformers import CLIPProcessor, CLIPModel
import numpy as np
import subprocess
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import util

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def ImgToVector(img):

    inputs = processor(images=img, return_tensors="pt")

    with torch.no_grad():
        image_features = model.get_image_features(**inputs)

    return convert(image_features)

def TextToVector(text):
    inputs = processor(
        text=text,
        return_tensors="pt",
        padding=True,
        truncation=True
    )

    with torch.no_grad():
        text_features = model.get_text_features(**inputs)

    return text_features

def getVideoVectors(Frames):
    vectors = []
    for frame in Frames:
        vectors.append(ImgToVector(frame))
    return vectors

def convert(vector):
    if hasattr(vector, "pooler_output"):
        vector = vector.pooler_output

    if torch.is_tensor(vector):
        vector = vector.detach().cpu().numpy()

    vector = np.array(vector).tolist()

    return vector

def avg(vectors):
    final_vector = []
    for i in range(512):
        TempSum = 0.0
        for vector in vectors:
            TempSum += vector[0][i]
        TempSum /= len(vectors)
        final_vector.append(TempSum)
    return final_vector

def VideoVector(Path, n = 60):
    Frames = []
    cap = cv2.VideoCapture(Path)
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % n == 0:
            Frames.append(frame)
        frame_count += 1
    cap.release()
    Vectors=getVideoVectors(Frames)
    return avg(Vectors)

def similarity(query_emb, image_emb):
    return util.cos_sim(query_emb, image_emb)


#def balls():
    x = VideoVector(r"C:\Users\amiel\PycharmProjects\PythonProject\SearchEngine\VideoSearchEngine\Videos\A Way Out 2025.12.27 - 17.18.54.03.DVR.mp4")
    print(type(x))
    print(len(x))
    print(x)


