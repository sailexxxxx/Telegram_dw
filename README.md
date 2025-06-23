# Telegram Downloader Bot

Bot de Telegram que descarga videos/reels/historias públicas de Instagram, TikTok o Facebook y los envía en MP4 o MP3, eliminando los archivos para liberar espacio (ideales para deploys en Render.com).

## 🧩 Estructura
- `bot.py`: lógica del bot.
- `requirements.txt`: dependencias.
- `README.md`: esta guía.

## 🚀 Despliegue en Render
1. Clona repo en tu cuenta de GitHub.
2. Crea un Web Service en Render usando ese repo.
3. Configura variable de entorno:
   - `BOT_TOKEN` → Token de tu bot.
4. En **Start Command**, pon:
   ```bash
   python bot.py
   ```
5. Despliega y comienza a usar.
