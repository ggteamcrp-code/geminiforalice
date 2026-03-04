import os
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Настройка Gemini
genai.configure(api_key="AIzaSyBJwvwwZYWySPdneIAhG0jSN_0fLdbtm5k")
model = genai.GenerativeModel('gemini-2.5-flash')

@app.route('/post', methods=['POST'])
def main():
    req = request.json
    user_text = req['request']['command'] # То, что ты сказал голосом
    
    if not user_text:
        response_text = "Привет! Я Gemini. О чем хочешь поговорить?"
    else:
        # Отправляем запрос в нейросеть
        chat_response = model.generate_content(user_text)
        response_text = chat_response.text

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
    # Railway сам скажет приложению, на каком порту работать
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

