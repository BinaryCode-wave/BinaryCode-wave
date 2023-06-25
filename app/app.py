from flask import Flask, render_template, jsonify, request
import src.services.YoutubeMethods
import nbformat
from nbconvert import HTMLExporter
from src.process import process_dataframe

app = Flask(__name__)

@app.route('/songs', methods=['POST'])
def songsList():
    datos = request.get_json()

    song = datos.get('favorite_track')
    intensity = datos.get('intensity')
    filter = datos.get('filter')
    algorithm = datos.get('algorithm')

    df = process_dataframe(THRESHOLD=float(intensity), algorithm=algorithm, song=song, filter_artists=filter)
    return df.to_json(orient='records')

@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    datos = request.get_json()
    songs = datos.get('urls')
    playlist_id = src.services.YoutubeMethods.init(songs)
    #playlist_id = "PLmgnf_5CScgUAB0-8EsBXX-XkQ3T6suBh" 
    print('Creating playlist...')
    return jsonify(playlist_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/doc')
def docs():
    return render_template('doc.html')

@app.route('/notebook')
def notebook():
    # Lee el archivo del notebook
    with open('./app/src/Program_Huaman_Mendoza_Ramirez.ipynb') as f:
        notebook_content = f.read()
        notebook = nbformat.reads(notebook_content, as_version=4)
    
    # Convierte el notebook a HTML
    html_exporter = HTMLExporter()
    (body, _) = html_exporter.from_notebook_node(notebook)

    return render_template('notebook.html', body=body)

if __name__ == '__main__':
    app.run(debug=True)