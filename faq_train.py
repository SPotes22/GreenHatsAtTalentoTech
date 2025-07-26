import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# 📥 Cargar dataset
df = pd.read_csv('FAQs.csv')

# 🧼 Normalizar nombres de columnas
df.columns = df.columns.str.strip().str.lower()

# 🧹 Preprocesamiento simple
def limpiar_texto(texto):
    return texto.lower().strip()

df['question'] = df['question'].apply(limpiar_texto)

# 🧠 Vectorización
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['question'])
y = df['category']

# 🔀 Dividir datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🤖 Entrenar modelo
modelo = MultinomialNB()
modelo.fit(X_train, y_train)

# 📊 Evaluar modelo
y_pred = modelo.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f'📈 Accuracy: {acc:.2f}')

# 💾 Guardar modelo y vectorizador
joblib.dump(modelo, 'modelo.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

print("✅ Modelo y vectorizador guardados como 'modelo.pkl' y 'vectorizer.pkl'")
