import os
import joblib
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from sentence_transformers import SentenceTransformer

# ---------------------------
# LINE config (ใช้ ENV บน Railway)
# ---------------------------

CHANNEL_ACCESS_TOKEN = os.environ.get("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.environ.get("CHANNEL_SECRET")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# ---------------------------
# Load model ที่เซฟไว้
# ---------------------------
svm = joblib.load("svm_model.pkl")
le = joblib.load("label_encoder.pkl")
model = SentenceTransformer("all-MiniLM-L6-v2")

CONFIDENCE_THRESHOLD = 0.5

def predict_intent(text):
    emb = model.encode([text])
    probas = svm.predict_proba(emb)
    pred = svm.predict(emb)[0]
    confidence = probas.max()
    if confidence < CONFIDENCE_THRESHOLD:
        return "ผมไม่แน่ใจว่าคุณหมายถึงอะไร รบกวนอธิบายอีกครั้ง", confidence
    else:
        intent = le.inverse_transform([pred])[0]
        return intent, confidence

# ---------------------------
# Flask App
# ---------------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "LINE Bot with SVM model is running!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return 'Invalid signature', 400
    return 'OK'

# ---------------------------
# Handle LINE messages
# ---------------------------
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()

    special_responses = {
        "Jame": "เกผู้สูงส่งปกครองเกบนผืนแผ่นดินแห่งอาณาจักรทองคำ<เกบรรพบุรุษ>",
        "Non": "จ้าวปกครองเกอันดำมืดแห่งเกใต้มหาสมุทรสีม่วง<เกบรรพบุรุษ>",
        "Mikito": "เกแห่งท้องนภาปกครองเกบนผืนฟ้าสีคราม<เกบรรพบุรุษ>",
        "Tell": "ไม่ใช่เกแต่อย่างใด เป็นเพียงผู้กล้านิรนามที่นานแสนนานจะปรากฏมาที<ผู้กล้า>"
    }

    if user_text in special_responses:
        reply_text = special_responses[user_text]
    else:
        intent, confidence = predict_intent(user_text)
        reply_text = f"{intent} (Confidence: {round(confidence,3)})"

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
