import torch
import torch.nn as nn
import torch.optim as optim
from torchvision.models import resnet18
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from torchvision import transforms
import os
from torchvision.models import ResNet18_Weights

# ハイパーパラメータ
BATCH_SIZE = 64
LEARNING_RATE = 0.001
EPOCHS = 10
DEVICE = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

# 1. ファイルの存在確認
if not os.path.exists('fer2013.csv'):
    raise FileNotFoundError("The file 'fer2013.csv' was not found in the current directory.")

# 2. データセットの読み込みと処理
class FER2013Dataset(Dataset):
    def __init__(self, data, transform=None):
        
        self.data = data
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        # 感情ラベル（0〜6）
        label = int(self.data.iloc[idx]['emotion'])
        
        # ピクセル値をリストとして取得し、48x48の画像に変換
        pixels = np.array(self.data.iloc[idx]['pixels'].split(), dtype=np.float32).reshape(48, 48)
        
        # 画像とラベルを返す
        if self.transform:
            pixels = self.transform(pixels)
        return pixels, label

# データ前処理
transform = transforms.Compose([
    transforms.ToPILImage(),  # Numpy配列をPIL画像に変換
    transforms.Grayscale(num_output_channels=3),  # グレースケール画像を3チャンネルに変換
    transforms.ToTensor(),  # テンソル形式に変換
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])  # 正規化
])

# CSVデータの読み込み
data = pd.read_csv('fer2013.csv')

# データ分割
train_data = data[data['Usage'] == 'Training']
val_data = data[data['Usage'] != 'Training']

# データセットの作成
train_dataset = FER2013Dataset(train_data, transform=transform)
val_dataset = FER2013Dataset(val_data, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

# 3. ResNet18モデルの準備

# 修正したResNet18の使用部分
class EmotionRecognitionModel(nn.Module):
    def __init__(self, num_classes=7):
        super(EmotionRecognitionModel, self).__init__()
        self.base_model = resnet18(weights=ResNet18_Weights.DEFAULT)  
        self.base_model.fc = nn.Linear(self.base_model.fc.in_features, num_classes)

    def forward(self, x):
        return self.base_model(x)


model = EmotionRecognitionModel(num_classes=7).to(DEVICE)

# 4. 損失関数と最適化
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# 5. トレーニングループ
for epoch in range(EPOCHS):
    model.train()
    train_loss = 0.0
    for images, labels in train_loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)

        # 勾配の初期化
        optimizer.zero_grad()

        # 順伝播
        outputs = model(images)
        loss = criterion(outputs, labels)

        # 逆伝播と重み更新
        loss.backward()
        optimizer.step()

        train_loss += loss.item()

    # バリデーション
    model.eval()
    val_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            outputs = model(images)
            loss = criterion(outputs, labels)
            val_loss += loss.item()

            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    print(f"Epoch [{epoch+1}/{EPOCHS}], "
          f"Train Loss: {train_loss/len(train_loader):.4f}, "
          f"Val Loss: {val_loss/len(val_loader):.4f}, "
          f"Val Accuracy: {accuracy:.2f}%")

# 6. モデルの保存
torch.save(model.state_dict(), "emotion_model.pth")
print("Model saved as 'emotion_model.pth'")
