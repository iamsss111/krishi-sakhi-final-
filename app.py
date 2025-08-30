
import streamlit as st
from gtts import gTTS
import tempfile
import os
from deep_translator import GoogleTranslator
from datetime import datetime
from streamlit_js_eval import streamlit_js_eval

# Page Config
st.set_page_config(page_title="Krishi Sakhi", page_icon="🌱", layout="centered")

# Translator using deep-translator
def tr(text, lang):
    if lang == "മലയാളം":
        try:
            return GoogleTranslator(source='auto', target='ml').translate(text)
        except:
            return text
    return text

# Voice Output
def speak(text, lang):
    tts = gTTS(text=text, lang='ml' if lang == "മലയാളം" else 'en')
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tmp_name = tmp.name
    tmp.close()
    tts.save(tmp_name)
    audio_bytes = open(tmp_name, "rb").read()
    st.audio(audio_bytes, format='audio/mp3')
    try:
        os.remove(tmp_name)
    except:
        pass

# CSS
st.markdown("<style>body{background-color:#f6fff6;} h1,h2,h3{color:#228B22;}</style>", unsafe_allow_html=True)

# Logo and title
st.image("logo.png", width=140)
st.title("🌱 Krishi Sakhi")

# Language
lang = st.radio("Choose language / ഭാഷ തിരഞ്ഞെടുക്കുക", ["English", "മലയാളം"])
lang_code = "ml-IN" if lang == "മലയാളം" else "en-IN"

# Get GPS using JS Eval
coords = streamlit_js_eval(js_expressions="navigator.geolocation.getCurrentPosition(p=>p.coords.latitude+','+p.coords.longitude)", key="get_gps")
if coords:
    st.success(tr(f"Location detected: {coords}", lang))

st.markdown("---")
st.header(tr("Profile Setup", lang))

# Web Speech API instructions
st.markdown("**🎤 Voice input available using your browser microphone. Click 'Start Voice Input' buttons.**")

def voice_input(prompt):
    # Use streamlit-js-eval to get speech input via Web Speech API
    st.write(prompt)
    if st.button("🎤 Start Voice Input: " + prompt):
        spoken_text = streamlit_js_eval(
            js_expressions="new Promise(resolve=>{var rec=new(window.SpeechRecognition||window.webkitSpeechRecognition)();rec.lang='{}';rec.onresult=e=>resolve(e.results[0][0].transcript);rec.start();})".format(lang_code),
            key=prompt
        )
        if spoken_text:
            st.success(f"✅ {prompt}: {spoken_text}")
            return spoken_text
    return ""

# Profile fields
name = st.text_input(tr("Enter your name", lang), value=voice_input(tr("Say your name", lang)))
mobile = st.text_input(tr("Enter mobile number", lang), value=voice_input(tr("Say mobile number", lang)))
place = st.text_input(tr("Enter place name", lang), value=voice_input(tr("Say location", lang)))
land_size = st.text_input(tr("Land size (in acres)", lang), value=voice_input(tr("Say land size", lang)))

water = st.selectbox(tr("Water Source", lang), [tr("Well", lang), tr("Rain", lang), tr("Canal", lang), tr("Borewell", lang)])
irrig = st.selectbox(tr("Irrigation Method", lang), [tr("Drip", lang), tr("Sprinkler", lang), tr("Flood", lang)])
soil = st.selectbox(tr("Soil Type", lang), [tr("Clay", lang), tr("Sandy", lang), tr("Loamy", lang), tr("Laterite", lang)])

st.subheader(tr("Crop Details", lang))
col1, col2, col3, col4 = st.columns(4)
current_crop = None
if col1.button("🌾 " + tr("Paddy", lang)): current_crop = "Paddy"
if col2.button("🍌 " + tr("Banana", lang)): current_crop = "Banana"
if col3.button("🥥 " + tr("Coconut", lang)): current_crop = "Coconut"
if col4.button("🥦 " + tr("Vegetables", lang)): current_crop = "Vegetables"

variety = st.text_input(tr("Variety (or none)", lang), value=voice_input(tr("Say variety", lang)))
sowing = st.date_input(tr("Date of sowing", lang))
season = st.selectbox(tr("Season", lang), [tr("Kharif", lang), tr("Rabi", lang), tr("Summer", lang)])

farming_type = st.radio(tr("Farming Type", lang), [tr("Organic", lang), tr("Chemical", lang)])
comm = st.multiselect(tr("Preferred Communication Mode", lang), [tr("SMS", lang), tr("WhatsApp", lang), tr("Voice Call", lang)])
reminder = st.selectbox(tr("Reminders Preference", lang), [tr("Daily", lang), tr("Weekly", lang), tr("Only Critical Alerts", lang)])

# Submit
if st.button(tr("✅ Complete Profile", lang)):
    profile = {
        "name": name,
        "mobile": mobile,
        "coords": coords,
        "place": place,
        "land_size_acres": land_size,
        "water_source": water,
        "irrigation_method": irrig,
        "soil_type": soil,
        "current_crop": current_crop,
        "variety": variety,
        "date_of_sowing": str(sowing),
        "season": season,
        "farming_type": farming_type,
        "communication_modes": comm,
        "reminder_pref": reminder,
        "created_at": datetime.utcnow().isoformat()
    }
    st.success(tr("Profile saved successfully!", lang))
    st.json(profile)
    summary = f"{tr('Profile created for', lang)} {profile['name']}. {tr('Crop', lang)}: {profile['current_crop'] or tr('Not selected', lang)}."
    speak(summary, lang)
