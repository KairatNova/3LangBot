
import google.generativeai as genai

Model = genai.GenerativeModel(model_name="models/gemini-2.0-flash") #choose model 
prompt = Model.start_chat(history=[ 
#Insert Your Prompt Here, 
# Example Prompt:
 # {
 #  "role": "user",
 # "parts": ["Hello"]
 #},
 # {
 #  "role": "model",
 #  "parts": ["Hello! How can I help you?"]
 # },

])

LANGUAGES = {
    "🇰🇬 Кыргызский": "ky",
    "🇷🇺 Русский": "ru",
    "🇬🇧 Английский": "en",
    "🇩🇪 Немецкий": "de",
}

language_labels = {
    "ky": {
        "🇰🇬 Кыргыз тили": "ky",
        "🇷🇺 Орус тили": "ru",
        "🇬🇧 Англис тили": "en",
        "🇩🇪 Немис тили": "de",
    },
    "ru": {
        "🇰🇬 Кыргызский": "ky",
        "🇷🇺 Русский": "ru",
        "🇬🇧 en": "Английский",
        "🇩🇪 Немецкий": "de",
    },
    "en": {
        "🇰🇬 Кыргызский": "ky",
        "🇷🇺 Русский": "ru",
        "🇬🇧 Английский": "en",
        "🇩🇪 Немецкий": "de",
    },
}
