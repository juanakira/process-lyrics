from flask import Flask, render_template, request
import numpy as np
from sklearn.cluster import KMeans

app = Flask(__name__)

# Definimos la ruta de la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Definimos la ruta para procesar el formulario
@app.route('/process', methods=['POST'])
def process():
    # Obtenemos la letra de la canción del formulario
    lyrics = request.form['lyrics']

    # Segmentamos la letra de la canción en diferentes secciones utilizando el algoritmo de segmentación de punto de cambio
    sections = segment_lyrics(lyrics)

    # Asignamos un código de color a cada sección
    colors = get_colors(len(sections))

    # Renderizamos la plantilla de la página de resultados y pasamos la letra de la canción, las secciones y los colores a la plantilla
    return render_template('results.html', lyrics=lyrics, sections=sections, colors=colors)

# Definimos una función para segmentar la letra de la canción en secciones utilizando el algoritmo de segmentación de punto de cambio
def segment_lyrics(lyrics):
    # Preprocesamos la letra de la canción y la convertimos en una matriz de características
    features = preprocess_lyrics(lyrics)

    # Utilizamos el algoritmo de KMeans para segmentar la letra de la canción en diferentes secciones
    kmeans = KMeans(n_clusters=2).fit(features)
    labels = kmeans.labels_

    # Separamos las secciones de la letra de la canción basados en los cambios en los patrones
    sections = []
    section_start = 0
    for i in range(1, len(labels)):
        if labels[i] != labels[i-1]:
            sections.append(lyrics[section_start:i])
            section_start = i
    sections.append(lyrics[section_start:])

    # Devolvemos una lista con las secciones de la letra de la canción
    return sections

# Definimos una función para preprocesar la letra de la canción y convertirla en una matriz de características
def preprocess_lyrics(lyrics):
    # Tokenizamos la letra de la canción en palabras
    words = lyrics.split()

    # Creamos una matriz de características que representa la frecuencia de cada palabra en la letra
    features = np.zeros((len(words), 1))
    for i, word in enumerate(words):
        features[i] = words.count(word)
    return features

# Definimos una función para asignar un código de color a cada sección
def get_colors(num_sections):
    colors = []
    for i in range(num_sections):
        if i % 2 == 0:
            colors.append('lightgray')
        else:
            colors.append('white')
    return colors
