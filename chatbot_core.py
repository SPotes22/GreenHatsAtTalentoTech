import joblib

# Cargar modelos
vectorizer = joblib.load('vectorizer.pkl')
modelo = joblib.load('modelo.pkl')

respuestas = {
    "saludo": "¡Hola! ¿Cómo puedo ayudarte?",
    "problema_tecnico": "¿Puedes decirme qué error tienes exactamente?",
    "soporte_factura": "Te ayudaré con tu factura, ¿qué parte no entiendes?",
    "despedida": "Gracias por usar el chatbot. ¡Hasta luego!",
    "fallback": "No entendí bien, ¿puedes reformular tu pregunta?"
}

def predecir_intencion(texto, temp=0.7, verbose=0.3):
    texto = texto.lower().strip()
    vector = vectorizer.transform([texto])
    pred = modelo.predict(vector)[0]
    return respuestas.get(pred, respuestas["fallback"])
