import cv2
import torch
import torchvision.transforms as transforms
import numpy as np
from torchvision.models import resnet18
from torchvision.models import ResNet18_Weights
import torch.nn as nn
import time  # 時間計測用
from collections import Counter  # 感情の出現回数を記録

# 表情ラベル
EMOTIONS = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

# モデルの定義
class EmotionRecognitionModel(nn.Module):
    def __init__(self, num_classes=7):
        super(EmotionRecognitionModel, self).__init__()
        self.base_model = resnet18(weights=ResNet18_Weights.DEFAULT)
        self.base_model.fc = nn.Linear(self.base_model.fc.in_features, num_classes)

    def forward(self, x):
        return self.base_model(x)

# デバイス設定
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Using device: {device}")

def start_get_emotion():
    # モデルのロード
    model = EmotionRecognitionModel(num_classes=len(EMOTIONS)).to(device)
    try:
        model.load_state_dict(torch.load("emotion_model.pth", map_location=device, weights_only=True))
        print("Model loaded successfully.")
    except FileNotFoundError:
        print("Error: Pretrained model file 'emotion_model.pth' not found.")
        exit()

    # 推論モードに設定
    model.eval()

    # 前処理
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Grayscale(num_output_channels=3),  # グレースケールを3チャンネルに変換
        transforms.Resize((48, 48)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])

    # カメラの初期化
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: Cannot access the camera.")
        exit()

    print("Starting camera feed for 3 seconds...")

    # 開始時刻を記録
    start_time = time.time()

    # 感情を記録するリスト
    emotion_counts = []

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # グレースケール変換と顔検出
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            # 顔領域を抽出して前処理
            face = gray[y:y+h, x:x+w]
            try:
                input_tensor = transform(face).unsqueeze(0).to(device)

                # 推論
                with torch.no_grad():
                    output = model(input_tensor)
                    emotion_idx = torch.argmax(output).item()
                    emotion = EMOTIONS[emotion_idx]

                # Neutral以外を記録
                if emotion != "Neutral":
                    emotion_counts.append(emotion)

            except Exception as e:
                print(f"Error during prediction: {e}")
                continue

        # 3秒経過で終了
        if time.time() - start_time > 3:
            print("3 seconds elapsed. Exiting application.")
            break

    # リソース解放
    cap.release()
    print("Analyzing emotions...")

    # Neutral以外で最頻感情を計算
    most_common_emotion = 'Neutral'
    if emotion_counts:
        most_common_emotion = Counter(emotion_counts).most_common(1)[0][0]
        print(f"The most frequent emotion (excluding 'Neutral') is: {most_common_emotion}")
    else:
        print("No emotions detected (excluding 'Neutral').")
    print("Application closed.")
    return most_common_emotion
