# Free Background Remover API (FastAPI + rembg)

API مجاني 100% لإزالة خلفية الصور عبر رابط مباشر للصورة. مبني على **FastAPI** و **rembg (U²-Net)**.

## 🧪 تجربة سريعة محليًا
```bash
python -m venv .venv && . .venv/bin/activate  # على ويندوز: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 7860
```
جرّب:
```
http://127.0.0.1:7860/remove?url=https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg&format=png&download=1
```

## 🚀 النشر مجانًا (Render أو Railway)
### Render.com
1. اعمل Repo على GitHub وارفع الملفات.
2. على Render: New ➜ Web Service.
3. اختار الريبو.
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. بعد النشر استخدم: `https://YOUR-RENDER-URL/remove?url=...`

### Railway.app
1. New Project ➜ Deploy from GitHub.
2. Add ➜ Service (Python). 
3. Variables: PORT=7860
4. Start Command: `uvicorn app:app --host 0.0.0.0 --port ${PORT}`

> ملاحظة: الخطط المجانية قد تنام بعد فترة خمول. أول طلب بعد النوم قد يأخذ ثوانٍ إضافية للبدء.

## 📚 الواجهات
- **GET** `/remove?url=<IMAGE_URL>&format=png|webp&download=0|1`  
- **GET** `/health`

## ⚠️ ملاحظات
- استخدم روابط مباشرة لصور (jpg/png/webp). الروابط التي تتطلب تسجيل دخول لن تعمل.
- أقصى دقة وأداء يعتمد على موارد الخادم (GPU غير مطلوب لكنه أسرع إن توفر).

## 🧩 Docker (اختياري)
```dockerfile
# Dockerfile
FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libgl1 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
ENV PORT=7860
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT}
```
بناء وتشغيل:
```bash
docker build -t free-bg-api .
docker run -p 7860:7860 free-bg-api
```