# INTEGRANTES Green Hats
# Chatbot orientado a facturación, entrenado con NLP clásico y montado con Flask para hackatón
Santiago Potes 

Freddy Alejandro Aristizabal

Juan Franco


#  Chatbot - Green Hats (Flask + scikit-learn)

Este es el frontend de nuestro chatbot, construido con **Flask** y **scikit-learn**. Usa un modelo de NLP clásico (TF-IDF + Naive Bayes) entrenado con un dataset ligero, capaz de responder preguntas básicas sobre facturación, soporte técnico y otros.

---

##  Tecnologías Usadas

- Python 3.10+
- Flask (Interfaz web)
- scikit-learn (modelo NLP)
- joblib (persistencia)
- Tailwind CSS (UI rápida)
- Pandas (manejo de dataset)

---

##  Estructura

```
chatbot-hackathon/
├── app.py                  # Servidor Flask
├── chatbot_core.py         # Lógica del modelo
├── intents.csv             # Dataset de entrenamiento
├── model_training.py       # Script para entrenar el modelo
├── modelo.pkl              # Modelo entrenado
├── vectorizer.pkl          # Vectorizador TF-IDF
├── requirements.txt
└── templates/
    ├── index.html
    └── chat.html
```

---

##  ¿Cómo correrlo?

1. Crear entorno virtual (opcional):
```bash
python -m venv venv
source venv/bin/activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Entrenar el modelo (una vez):
```bash
python model_training.py
```

4. Ejecutar el servidor:
```bash
python app.py
```

Accede al bot en `http://localhost:5000`

---

##  Dataset

El archivo `intents.csv` y `FAQs.csv` contiene frases etiquetadas con sus respectivas intenciones. Estas son procesadas por `TfidfVectorizer` y clasificadas por `MultinomialNB`.

---

##  Posibles mejoras

- Entrenamiento dinámico con nuevos inputs
- Logs de conversación
- Interfaz más avanzada con WebSocket
- Integración con GPT vía API (ver backend PHP)

---

## Licencia

MIT — hecho con sudor por Green Hats ⚡

# pasos de uso
- entorno virtual
- pip install -r  requieriments.txt
- ponerle datos al intents.csv 
- python3 model-training.py
- python3 app.py
- probar parte grafica

# intents.csv 
`texto,intent`
`hola,saludo`
 
# app.py
- '/' index vista de funcionalidades general
- '/chat/' vista chat
- model-training.py debe ser modificado solo y exclusivamente si se sabe lo que se hace
- '/login'
- '/signup'
- '/logout'
  
