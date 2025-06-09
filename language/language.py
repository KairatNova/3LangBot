

translations = {
    "ru": {
        "start_message": '''Привет 👋! Я — языковой помощник-бот.
Для начала — зарегистрируйтесь нажав на кнопку 👉 /register''',

        "welcome_message": "Добро пожаловать! Я ваш языковой помощник.",
        "welcome_back": "С возвращением! Чем могу помочь?",

  

        "choose_language": "Пожалуйста, выберите язык интерфейса:",
        "register_prompt": "Нажмите на кнопку, чтобы бот зарегистрировал вас",
        "registration_error": "❌ Произошла ошибка при регистрации",
        "already_registered": "ℹ️ Пользователь {username} уже зарегистрирован",

        "success_registration": "✅ Вы успешно зарегистрированы",
        "access_granted": "🔓 Разрешен доступ к боту",
        "menu_text": "Вот меню кнопок",
        "what_interests_you": "Что Вас интересует?",
        "language_changed": "Язык успешно изменен на {language}",

    "registered_start_message": (
            "Я могу:\n"
            "• Переводить слова и фразы 📚\n"
            "• Помогать учить английский, русский и кыргызский языки 🌍\n"
            "• Предлагать видео и тексты для практики 🎬📖\n"
            "• Игры, грамматика и чат с ИИ"),

        #* Профиль пользователя
"profile_template": (
            "👤 <b>Ваш профиль</b>\n\n"
            f"🆔 <b>ID:</b> <code>{{user_id}}</code>\n"
            f"👁️ <b>Username:</b> {{username}}\n"
            f"📛 <b>Имя:</b> {{first_name}}\n"
            f"🌐 <b>Язык:</b> {{language}}\n"
            f"📅 <b>Регистрация:</b> {{reg_date}}\n"
            f"🕒 <b>Последняя активность:</b> {{last_active}}\n\n"
            f"<i>Используйте бота для изучения языков!</i>"
        ),
        "profile_not_found": "❌ Профиль не найден. Пожалуйста, зарегистрируйтесь через /register",
        "profile_load_error": "⚠️ Произошла ошибка при загрузке профиля. Попробуйте позже.",
        "unexpected_error": "⚠️ Произошла непредвиденная ошибка. Попробуйте позже.",
        "not_specified": "не указан",
   # Google Translate
 "enable_translator": "🔁 Включить переводчик",
        "disable_translator": "🚫 Выключить переводчик",
        "translation_history": "📜 История переводов",
        "clear_history": "🧹 Очистить историю",
        "back_button": "🔙 Назад",
        "what_to_translate": "Что перевести?",
        "choose_target_language": "Выберите язык для перевода:",
        "what_to_translate_placeholder": "На какой язык хотите перевести?",
        "translator_disabled": "Переводчик выключен. Нажмите /translate или кнопку для активации.",
        "choose_action": "Выберите действие:",
        "history_empty": "Ваша история переводов пуста.",
        "your_translation_history": "Ваша история переводов",
        "clear_history_button": "🧹 Очистить историю",
        "history_cleared": "История переводов успешно очищена.",
        "history_clear_error": "Не удалось очистить историю переводов.",
        "language_set": "Язык перевода установлен: {language}\nОтправьте текст для перевода или нажмите '🔙 Назад'",
        "original_text": "Оригинал",
        "translated_text": "Перевод",
        "translation_error": "⚠️ Ошибка перевода: {error}",
        "select_language_first": "Сначала выберите язык перевода через /translate",

        # chat gpt
        "chatgpt_intro": """
🇬🇧 <b>Привет! Я Английский Языковой Помощник</b> 🇺🇸
Чем я могу вам помочь?
🎓 <b>Совет</b>: Занимайтесь регулярно по 15-20 минут для лучшего результата!
""",
        "chatgpt_callback_intro": """
🇬🇧 <b>Английский Языковой Помощник chatgpt</b> 🇺🇸

✨ <b>Лимиты использования</b>  
- 2000 токенов в день (~2000 символов)  
- Лимит обновляется каждые 24 часа  
""",
        "stop_button": "stop⛔",
        "chat_stopped": "Чат остановлен. Чтобы начать снова, введите /chatgpt",
        "token_limit_reached": "⚠️ Вы израсходовали дневной лимит токенов (2000). Попробуйте завтра.",
        "generating_answer": "Generating answer⌛",
        "describe_image": "Опишите изображение",
        "unsupported_message": "Этот тип сообщения не поддерживается",
        "token_limit_exceeded": "⚠️ Превышен лимит токенов для этого запроса",
        "tokens_used": "ℹ️ Использовано токенов: {used} (Осталось: {remaining})",
        "error_occurred": "⚠️ Произошла ошибка: {error}", 

                # Inline кнопки
        "translator_btn": "Переводчик",
        "chatgpt_btn": "ChatGPT",
        "learn_words_btn": "Учить слова",
        "word_meaning_btn": "Значение слов",
        "texts_btn": "Тексты",
        "games_btn": "Игры",
        
        # Основное меню
        "menu_btn": "Меню",
        "profile_btn": "Профиль",

        
        # Переводчик
        "choose_target_language": "Выберите язык для перевода:",
        "what_to_translate_placeholder": "На какой язык хотите перевести?",
        "enable_translator": "🔁 Включить переводчик",
        "disable_translator": "🚫 Выключить переводчик",
        "translator_disabled": "Переводчик выключен. Нажмите /translate или кнопку для активации.",
        "back_button": "🔙 Назад",
        "choose_action": "Выберите действие:",
        "language_set": "Язык перевода установлен: {language}\nОтправьте текст для перевода.",
        
        # ChatGPT
        "enable_gpt_btn": "🔵 Включить ChatGPT",
        "disable_gpt_btn": "🔴 Выключить ChatGPT",
        
        # Команды бота
        "start_cmd": "Запуск бота",
        "menu_cmd": "Меню сервисов",
        "chatgpt_cmd": "ИИ Помощник",
        "profile_cmd": "Ваш профиль",
        "language_cmd": "Язык интерфейса",
        "translate_cmd": "Переводчик"

        
    },
    "en": {
        "start_message": '''Hello 👋! I'm a language assistant bot.

To get started — register by clicking the button 👉 /register''',

        "welcome_message": "Welcome! I'm your language assistant.",
        "welcome_back": "Welcome back! How can I help you?",

        "choose_language": "Please choose your interface language:",
        "register_prompt": "Click the button to register with the bot",
        "registration_error": "❌ An error occurred during registration",
        "already_registered": "ℹ️ User {username} is already registered",

        "success_registration": "✅ You have successfully registered",
        "access_granted": "🔓 Access to the bot granted",
        "menu_text": "Here is the menu",
        "what_interests_you": "What are you interested in?",
        "language_changed": "Language successfully changed to {language}",

    "registered_start_message": (
            "I can:\n"
            "• Translate words and phrases 📚\n"
            "• Help you learn English, Russian and Kyrgyz 🌍\n"
            "• Offer videos and texts for practice 🎬📖\n"
            "• Games, grammar and AI chat"
        ),
            #* Профиль пользователя
"profile_template": (
            "👤 <b>Your Profile</b>\n\n"
            f"🆔 <b>ID:</b> <code>{{user_id}}</code>\n"
            f"👁️ <b>Username:</b> {{username}}\n"
            f"📛 <b>First Name:</b> {{first_name}}\n"
            f"🌐 <b>Language:</b> {{language}}\n"
            f"📅 <b>Registration:</b> {{reg_date}}\n"
            f"🕒 <b>Last Active:</b> {{last_active}}\n\n"
            f"<i>Use the bot for language learning!</i>"
        ),
        "profile_not_found": "❌ Profile not found. Please register via /register",
        "profile_load_error": "⚠️ An error occurred while loading the profile. Please try again later.",
        "unexpected_error": "⚠️ An unexpected error occurred. Please try again later.",
        "not_specified": "not specified",

   # Google Translate
 "enable_translator": "🔁 Enable translator",
        "disable_translator": "🚫 Disable translator",
        "translation_history": "📜 Translation history",
        "clear_history": "🧹 Clear history",
        "back_button": "🔙 Back",
        "what_to_translate": "What to translate?",
        "choose_target_language": "Choose target language:",
        "what_to_translate_placeholder": "Which language to translate to?",
        "translator_disabled": "Translator disabled. Use /translate or button to activate.",
        "choose_action": "Choose action:",
        "history_empty": "Your translation history is empty.",
        "your_translation_history": "Your translation history",
        "clear_history_button": "🧹 Clear history",
        "history_cleared": "Translation history cleared successfully.",
        "history_clear_error": "Failed to clear translation history.",
        "language_set": "Translation language set: {language}\nSend text to translate or press '🔙 Back'",
        "original_text": "Original",
        "translated_text": "Translation",
        "translation_error": "⚠️ Translation error: {error}",
        "select_language_first": "First select translation language via /translate",

        # chat gpt
        "chatgpt_intro": """
🇬🇧 <b>Hello! I'm English Language Assistant</b> 🇺🇸
How can I help you?
🎓 <b>Tip</b>: Practice regularly for 15-20 minutes for best results!
""",
        "chatgpt_callback_intro": """
🇬🇧 <b>English Language Assistant chatgpt</b> 🇺🇸

✨ <b>Usage limits</b>  
- 2000 tokens per day (~2000 characters)  
- Limit refreshes every 24 hours  
""",
        "stop_button": "stop⛔",
        "chat_stopped": "Chat stopped. To start again, type /chatgpt",
        "token_limit_reached": "⚠️ You've reached your daily token limit (2000). Try again tomorrow.",
        "generating_answer": "Generating answer⌛",
        "describe_image": "Describe image",
        "unsupported_message": "This message type is not supported",
        "token_limit_exceeded": "⚠️ Token limit exceeded for this request",
        "tokens_used": "ℹ️ Tokens used: {used} (Remaining: {remaining})",
        "error_occurred": "⚠️ An error occurred: {error}", 

                # Inline кнопки
        "translator_btn": "Translator",
        "chatgpt_btn": "ChatGPT",
        "learn_words_btn": "Learn words",
        "word_meaning_btn": "Word meaning",
        "texts_btn": "Texts",
        "games_btn": "Games",
        
        # Основное меню
        "menu_btn": "Menu",
        "profile_btn": "Profile",
        "feedback_btn": "Leave feedback",
        
        # Переводчик
        "choose_target_language": "Choose target language:",
        "what_to_translate_placeholder": "Which language to translate to?",
        "enable_translator": "🔁 Enable translator",
        "disable_translator": "🚫 Disable translator",
        "translator_disabled": "Translator disabled. Use /translate or button to activate.",
        "back_button": "🔙 Back",
        "choose_action": "Choose action:",
        "language_set": "Translation language set: {language}\nSend text to translate.",
        
        # ChatGPT
        "enable_gpt_btn": "🔵 Enable ChatGPT",
        "disable_gpt_btn": "🔴 Disable ChatGPT",
        
        # Команды бота
        "start_cmd": "Start bot",
        "menu_cmd": "Services menu",
        "chatgpt_cmd": "AI Assistant",
        "profile_cmd": "Your profile",
        "language_cmd": "Interface language",
        "translate_cmd": "Translator"
    },

    "ky": {
        "start_message": '''Салам 👋! Мен — тил жардамчы-ботмун.
Баштоо үчүн — баскычты басып катталыңыз 👉 /register''',

        "welcome_message": "Кош келиңиз! Мен сиздин тил жардамчыңыз.",
        "welcome_back": "Кабыл алгыла! Сизге кандай жардам бере алам?",

        "choose_language": "Сураныч, интерфейс тилин тандаңыз:",
        "register_prompt": "Ботко катталуу үчүн баскычты басыңыз",
        "registration_error": "❌ Каттоо убагында ката кетти",
        "already_registered": "ℹ️ {username} колдонуучусу мурунтан эле катталган",
        
        "success_registration": "✅ Ийгиликтүү катталдыңыз",
        "access_granted": "🔓 Ботко кирүүгө уруксат берилди",
        "menu_text": "Бул баскычтар менюсу",
        "what_interests_you": "Сизди эмне кызыктырат?",
        "language_changed": "Тил ийгиликтүү өзгөртүлдү {language}",

    "registered_start_message": (
            "Мен:\n"
            "• Сөздөрдү жана сөз айкаштарын которо алам 📚\n"
            "• Англисче, орусча жана кыргызча үйрөнүүгө жардам берем 🌍\n"
            "• Практика үчүн видеолорду жана тексттерди сунуштайм 🎬📖\n"
            "• Оюндар, грамматика жана ИИ менен сүйлөшүү"
        ),

    #* Профиль пользователя
 "profile_template": (
            "👤 <b>Сиздин профилиңиз</b>\n\n"
            f"🆔 <b>ID:</b> <code>{{user_id}}</code>\n"
            f"👁️ <b>Username:</b> {{username}}\n"
            f"📛 <b>Аты:</b> {{first_name}}\n"
            f"🌐 <b>Тили:</b> {{language}}\n"
            f"📅 <b>Каттоо:</b> {{reg_date}}\n"
            f"🕒 <b>Акыркы активдүүлүк:</b> {{last_active}}\n\n"
            f"<i>Тил үйрөнүү үчүн ботту колдонуңуз!</i>"
        ),
        "profile_not_found": "❌ Профиль табылган жок. Сураныч, /register аркылуу катталыңыз",
        "profile_load_error": "⚠️ Профильди жүктөө убагында ката кетти. Кийинчерээк аракет кылыңыз.",
        "unexpected_error": "⚠️ Күтүлбөгөн ката кетти. Кийинчерээк аракет кылыңыз.",
        "not_specified": "көрсөтүлгөн жок"   ,

        # Google Translate
         "enable_translator": "🔁 Котормочу иштетүү",
        "disable_translator": "🚫 Котормочу өчүрүү",
        "translation_history": "📜 Которуулар тарыхы",
        "clear_history": "🧹 Тарыхты тазалоо",
        "back_button": "🔙 Артка",
        "what_to_translate": "Эмне которуу керек?",
        "choose_target_language": "Которуу тилин тандаңыз:",
        "what_to_translate_placeholder": "Кайсыл тилге которуу керек?",
        "translator_disabled": "Котормочу өчүрүлгөн. Иштетүү үчүн /translate же баскычты колдонуңуз.",
        "choose_action": "Аракетти тандаңыз:",
        "history_empty": "Сиздин которуулар тарыхыңыз бош.",
        "your_translation_history": "Сиздин которуулар тарыхыңыз",
        "clear_history_button": "🧹 Тарыхты тазалоо",
        "history_cleared": "Которуулар тарыхы ийгиликтүү тазаланды.",
        "history_clear_error": "Которуулар тарыхын тазалоо ишке ашкан жок.",
        "language_set": "Которуу тили орнотулду: {language}\nКоторуу үчүн текст жөнөтүңүз же '🔙 Артка' баскычын басыңыз",
        "original_text": "Оригинал",
        "translated_text": "Котормосу",
        "translation_error": "⚠️ Которуу катасы: {error}",
        "select_language_first": "Алгач /translate аркылуу которуу тилин тандаңыз",

        # chat gpt 

          "chatgpt_intro": """
🇬🇧 <b>Салам! Мен Англис тил жардамчысымын</b> 🇺🇸
Сизге кандай жардам бере алам?
🎓 <b>Кеңеш</b>: Эң жакшы натыйжа үчүн ар күнү 15-20 мүнөт тажрыйбалаңыз!
""",
        "chatgpt_callback_intro": """
🇬🇧 <b>Англис тил жардамчысы chatgpt</b> 🇺🇸

✨ <b>Колдонуу чектөөлөрү</b>  
- Күнүнө 2000 токен (~2000 символ)  
- Чектөө ар 24 сааттан жаңыланат  
""",
        "stop_button": "stop⛔",
        "chat_stopped": "Чат токтотулду. Кайра баштоо үчүн /chatgpt териңиз",
        "token_limit_reached": "⚠️ Сиз күндүк токен лимитин колдонуп бүттүңүз (2000). Эртең кайра аракет кылыңыз.",
        "generating_answer": "Жооп иштеп чыгууда⌛",
        "describe_image": "Сүрөттү сүрөттөө",
        "unsupported_message": "Бул билдирүү түрү колдогон эмес",
        "token_limit_exceeded": "⚠️ Бул суроо үчүн токен лимити ашып кетти",
        "tokens_used": "ℹ️ Колдонулган токендер: {used} (Калган: {remaining})",
        "error_occurred": "⚠️ Ката кетти: {error}",  

                # Inline кнопки
        "translator_btn": "Котормоч",
        "chatgpt_btn": "ChatGPT",
        "learn_words_btn": "Сөздөрдү үйрөнүү",
        "word_meaning_btn": "Сөздөрдүн мааниси",
        "texts_btn": "Тексттер",
        "games_btn": "Оюндар",
        
        # Основное меню
        "menu_btn": "Меню",
        "profile_btn": "Профиль",

        
        # Переводчик
        "choose_target_language": "Которуу тилин тандаңыз:",
        "what_to_translate_placeholder": "Кайсыл тилге которуу керек?",
        "enable_translator": "🔁 Котормочу иштетүү",
        "disable_translator": "🚫 Котормочу өчүрүү",
        "translator_disabled": "Котормочу өчүрүлгөн. Иштетүү үчүн /translate же баскычты колдонуңуз.",
        "back_button": "🔙 Артка",
        "choose_action": "Аракетти тандаңыз:",
        "language_set": "Которуу тили орнотулду: {language}\nКоторуу үчүн текст жөнөтүңүз.",
        
        # ChatGPT
        "enable_gpt_btn": "🔵 ChatGPT иштетүү",
        "disable_gpt_btn": "🔴 ChatGPT өчүрүү",
        
        # Команды бота
        "start_cmd": "Ботту иштетүү",
        "menu_cmd": "Кызматтар менюсу",
        "chatgpt_cmd": "ИИ Жардамчы",
        "profile_cmd": "Сиздин профиль",
        "language_cmd": "Интерфейс тили",
        "translate_cmd": "Котормоч"  
    }
}

'''
def get_translation(key: str, lang: str = "ru", **kwargs) -> str:
    """Получает перевод по ключу для указанного языка"""
    try:
        text = translations[lang][key]
        return text.format(**kwargs) if kwargs else text
    except KeyError:
        # Если перевод не найден, возвращаем русскую версию или заглушку
        try:
            return translations["ru"][key]
        except KeyError:
            return f"[Translation missing for key: {key}]"  # Заглушка для отсутствующих переводов'''