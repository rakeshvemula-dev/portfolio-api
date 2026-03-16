# ⚡ Portfolio API — FastAPI Backend

A production-ready FastAPI backend that powers the AI chat assistant on [Rakesh Vemula's portfolio](https://rakeshvemula-dev.github.io/portfolio). Built with Python, FastAPI, and Groq's LLaMA 3.1 model.

🌐 **Live API:** [portfolio-api-qakh.onrender.com](https://portfolio-api-qakh.onrender.com)
🎨 **Frontend repo:** [github.com/rakeshvemula-dev/rakeshvemula-dev.github.io](https://github.com/rakeshvemula-dev/rakeshvemula-dev.github.io)

---

## 🏗️ Architecture

```
Portfolio Frontend (GitHub Pages)
          ↓  POST /chat
FastAPI Backend (Render)
          ↓  calls
Groq API (LLaMA 3.1 8B Instant)
          ↓  returns
FastAPI → Frontend → User
```

The API key is stored securely in Render's environment variables — never exposed in frontend code.

---

## ✨ Features

- **`POST /chat`** — accepts conversation history, returns AI response
- **System context injection** — Rakesh's resume is injected as system prompt on every request
- **Conversation memory** — full message history passed on each call
- **CORS configured** — only allows requests from the portfolio domain
- **Environment variable security** — API key never in source code
- **Health check endpoint** — `GET /` for monitoring
- **Auto-deploy** — redeploys on every push to `main` via Render

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| FastAPI | Web framework |
| Uvicorn | ASGI server |
| httpx | Async HTTP client for Groq calls |
| python-dotenv | Environment variable management |
| Groq API | LLM inference (LLaMA 3.1 8B Instant) |
| Render | Deployment platform |

---

## 📁 Project Structure

```
portfolio-api/
├── main.py             → FastAPI app, routes, Groq integration
├── .env                → API keys (never committed)
├── pyproject.toml      → dependencies
├── Procfile            → Render start command
└── .gitignore          → excludes .env and .venv
```

---

## 📡 API Endpoints

### `GET /`
Health check — confirms API is running.

**Response:**
```json
{
  "status": "Portfolio API is running"
}
```

---

### `POST /chat`
Accepts conversation history and returns AI reply.

**Request body:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "What projects has Rakesh built?"
    }
  ]
}
```

**Response:**
```json
{
  "reply": "Rakesh has built three projects..."
}
```

**Error response:**
```json
{
  "detail": "Error message here"
}
```

---

## 🚀 Run Locally

**1. Clone the repo:**
```bash
git clone https://github.com/rakeshvemula-dev/portfolio-api.git
cd portfolio-api
```

**2. Set up virtual environment with uv:**
```bash
uv venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate # Mac/Linux
```

**3. Install dependencies:**
```bash
uv add fastapi uvicorn python-dotenv httpx
```

**4. Create `.env` file:**
```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at [console.groq.com](https://console.groq.com)

**5. Run the server:**
```bash
uvicorn main:app --reload --port 8000
```

**6. Test it:**
- Health check: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`

---

## 🔒 Security

- API key stored in `.env` — excluded from git via `.gitignore`
- CORS restricted to portfolio domain only
- No sensitive data in source code
- Environment variables managed via Render dashboard in production

---

## ☁️ Deployment

Deployed on **Render** free tier.

**Build command:**
```
pip install .
```

**Start command:**
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Environment variables set in Render dashboard:**
```
GROQ_API_KEY=your_actual_key
```

> ⚠️ Note: Render free tier spins down after 15 minutes of inactivity. First request after spin-down may take 30-50 seconds.

---

## 🔮 Future Improvements

- [ ] Add PostgreSQL for chat history logging
- [ ] Add rate limiting per IP
- [ ] Add request authentication
- [ ] Migrate to a persistent hosting plan
- [ ] Add analytics endpoint

---

## 📬 Contact

**Rakesh Vemula**
- 🌐 Portfolio: [rakeshvemula-dev.github.io/portfolio](https://rakeshvemula-dev.github.io/portfolio)
- 💼 LinkedIn: [linkedin.com/in/iamrakeshvemula](https://linkedin.com/in/iamrakeshvemula)
- 🐙 GitHub: [github.com/rakeshvemula-dev](https://github.com/rakeshvemula-dev)
- 📧 Email: rakeshvemula14300@gmail.com

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
