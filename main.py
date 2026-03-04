import os
import google.generativeai as genai # <-- Вот правильный импорт для новой библиотеки
from flask import Flask, request, jsonify

app = Flask(__name__)

# Эта обертка нужна, чтобы сервер не падал, если что-то не так с ключом
try:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY не найден в переменных окружения.")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Критическая ошибка при инициализации Gemini: {e}")
    model = None # Помечаем, что модель не работает

@app.route('/post', methods=['POST'])
def main():
    req = request.json
    user_text = req.get('request', {}).get('command', '')
    
    if model is None:
        response_text = "Проблема с настройкой нейросети. Проверьте переменные окружения и ключ API на Railway."
    elif not user_text:
        response_text = "Привет! Я Gemini. Чем могу помочь?"
    else:
        try:
            chat_response = model.generate_content(user_text)
            # Добавим проверку на случай, если ответ пустой
            if chat_response.text:
                response_text = chat_response.text
            else:
                response_text = "Я получил пустой ответ. Возможно, сработал фильтр безопасности. Попробуй переформулировать."
        except Exception as e:
            response_text = f"Произошла ошибка при обращении к нейросети. Попробуйте позже."

    # Формируем ответ для Алисы
    res = {
        'version': req['version'],
        'session': req['session'],
        'response': {
            'text': response_text,
            'end_session': False
        }
    }
    return jsonify(res)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
