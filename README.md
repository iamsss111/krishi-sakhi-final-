
# ✅ Krishi Sakhi (Streamlit Cloud - Final Version)

### Features
- Language selection: English / Malayalam
- Voice prompts (Malayalam + English) using gTTS
- Voice input using **browser Web Speech API** (works in Chrome)
- GPS auto-detection using HTML5 Geolocation
- Green and white farmer-friendly UI

---
## ✅ How to Deploy on Streamlit Cloud
1. Upload these files to a **public GitHub repo**.
2. Go to [Streamlit Cloud](https://share.streamlit.io/).
3. Connect GitHub and click **New App**.
4. Select:
   - Repository: `yourusername/yourrepo`
   - Branch: `main`
   - Main file: `app.py`
5. Deploy and wait for build to complete.
6. You will get a live demo URL like:
   `https://krishi-sakhi.streamlit.app`

---
## ✅ How to Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

---
## ✅ Notes
- Works on **Chrome desktop and Android browsers**.
- GPS requires **location permission**.
- Internet required for voice prompts.
