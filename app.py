from flask import Flask, request, render_template
import chatbot_core as chat_core

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat/', methods=['GET', 'POST'])
def chat():
    response = ''
    if request.method == 'POST':
        question = request.form.get('question')
        if question:
            response = chat_core.predecir_intencion(question, temp=0.7, verbose=0.34)
    return render_template('chat.html', response=response)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

