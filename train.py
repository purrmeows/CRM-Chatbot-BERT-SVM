import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sentence_transformers import SentenceTransformer
import joblib

# โหลด dataset
DATA_PATH = "datasets/intent_clean_full_NUMBER.csv"
df = pd.read_csv(DATA_PATH)
texts = df["instruction"].astype(str).tolist()
labels = df["intent"].astype(str).tolist()

# encode label
le = LabelEncoder()
y = le.fit_transform(labels)

# สร้าง embedding
model = SentenceTransformer("all-MiniLM-L6-v2")
X = model.encode(texts, batch_size=32, show_progress_bar=True)

# เทรน SVM
base_svm = LinearSVC(class_weight="balanced", max_iter=5000)
svm = CalibratedClassifierCV(base_svm, cv=3)
svm.fit(X, y)

# เซฟโมเดลและ LabelEncoder
joblib.dump(svm, "svm_model.pkl")
joblib.dump(le, "label_encoder.pkl")

print("Training completed and models saved!")
