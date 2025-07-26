# INTEGRANTES Green hats
Santiago Potes 
Freddy Alejandro Aristizabal
Juan Franco


n,cc,corr,cel


 minichatbot llm template flask

# pasos de uso
- entorno virtual
- pip install -r  requieriments.txt
- ponerle datos al intents.csv 
- python3 model-training.py
- python3 app.py
- probar parte grafica

# intents.csv
texto,intent
hola,saludo
 
# app.py
- '/' index vista de funcionalidades general
- '/chat/' vista chat
- model-training.py debe ser modificado solo y exclusivamente si se sabe lo que se hace

# referencias y documentacion util
https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.VotingClassifier.html?utm_source=chatgpt.com
https://stackoverflow.com/questions/67171946/how-to-make-naive-bayes-multinomial-with-tf-idf-from-scratch-in-python?utm_source=chatgpt.com
https://scikit-learn.org/stable/common_pitfalls.html?utm_source=chatgpt.com
https://ai.plainenglish.io/25-machine-learning-projects-for-all-levels-beginner-friendly-to-advance-61fbac30ab77

Flashcards de herramientas y técnicas
1. TF‑IDF + Naive Bayes con Scikit-Learn
Qué es: Clasificación de texto rápida y eficiente usando TF‑IDF para vectorizar y MultinomialNB para clasificar.

Por qué usarlo: Ligero, rápido, entendible y excelente con datasets medianos.

Práctica recomendada: sigue el paso a paso desde StackOverflow 



2. VotingClassifier en Scikit‑Learn
Qué es: Ensamble de modelos simples que hace hard o soft voting para mejorar precisión.

Doc oficial: Usando VotingClassifier(estimators=[...], voting='hard/soft') 


Ventajas: Puedes entrenar tres clasificadores por separado y combinarlos fácilmente; ideal para tu enfoque distribuido.

3. Evitar malas prácticas en Scikit‑Learn
Punto clave: Usa pipelines y aplica exactamente la misma limpieza durante entrenamiento y en producción.

Recurso: sección “Common pitfalls and recommended practices” 
scikit-learn.org
.

4. Guía de intent classification para chatbots (Quidget)
Contenido: Arquitectura básica, cómo definir intents, recolectar datos, tokenización, limpieza, métricas (accuracy, recall, precision, F1) 
Artificial Intelligence in Plain English
+1
scikit-learn.org
+1
.

Importante: Buen diseño de intents reduce errores y facilita el etiquetado colaborativo. 

5. Ensemble avanzado y análisis de rendimiento
Biblioteca: DESlib (dynamic ensemble selection) compatible con Scikit-learn 

Utilidad: Si un modelo está fallando en ciertos casos, DESlib puede seleccionar automáticamente cuál usar.

6. Herramienta de ensemble: Pycobra
Para qué sirve: Combina múltiples modelos y visualiza resultados. Compatible con scikit-learn 
arXiv


Uso: Ideal para analizar qué modelo aporta más y cómo varían votos.

7. Tutorial de ensemble con Python paso a paso
Contenido: Ejemplo práctico para montar VotingClassifier con LogisticRegression, SVM y SGD 


Beneficio: Base para armar tu propio train_all.py con múltiples clasificadores entrenados sobre distintos subsets.

8. Recursos de NLP y fine-tuning (NLPlanet)
Incluye: Guía general sobre clasificación de texto, modelos tradicionales (Naive Bayes, Word2vec, LSTM, BERT).

Para tí: Te ayuda a escalar si incluyes pre-entrenamiento o embeddings 
Medium


| Fase del trabajo                         | Flashcards útiles                      | Acción recomendada                                    |
| ---------------------------------------- | -------------------------------------- | ----------------------------------------------------- |
| **División y entrenamiento distribuido** | TF‑IDF + NB, VotingClassifier          | Carga subset, entrena, guarda modelos                 |
| **Ensamblado / fusión**                  | VotingClassifier docs, Pycobra, DESlib | Combinar modelos y usar votación o selección dinámica |
| **Prevención de errores**                | Common pitfalls                        | Usa pipelines y asegura consistencia de procesamiento |
| **Refinamiento de intents**              | Guía de intent classification          | Revisa estructura de intents, agrega ejemplos nuevos  |
| **Escalado futuro**                      | NLPlanet recursos, Quidget             | Considera embeddings, transfer learning si hay tiempo |

.
