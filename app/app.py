from flask import Flask, render_template, jsonify, request
import time
import src.services.YoutubeMethods
import nbformat
from nbconvert import HTMLExporter
from src.process import process_dataframe

app = Flask(__name__)

songs = []
def get_data():
    list = [{'name': 'Daniel', 'url': 'https://www.youtube.com/watch?v=bBB-VAHYi7c'}, {'name': 'Jorge', 'url': 'https://www.youtube.com/watch?v=gqmwtVey3Cs'}, {'name': 'Luis', 'url': 'https://www.youtube.com/watch?v=z7pVGZwghZE'}, {'name': 'Carlos', 'url': 'https://www.youtube.com/watch?v=-3vwrzqkMgU'}]
    time.sleep(2)
    if len(songs) > 0: songs.clear()
    for item in list:
        songs.append(item['url'])
    return jsonify(list)

@app.route('/data', methods=['POST'])
def data():
    value = request.args.get('value')
    list = get_data()
    return list

@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    #playlist_id = src.services.YoutubeMethods.init(songs)
    playlist_id = "PLmgnf_5CScgUAB0-8EsBXX-XkQ3T6suBh"
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

@app.route('/songs', methods=['POST'])
def songs():
    prefence_value = request.form.get('preference_value')
    df = process_dataframe(THRESHOLD=float(prefence_value))
    return render_template('songs.html', data=df.to_json(orient='records'))
if __name__ == '__main__':
    app.run(debug=True)