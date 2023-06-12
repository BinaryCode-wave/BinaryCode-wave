from flask import Flask, render_template
import nbformat
from nbconvert import HTMLExporter
from src.process import process_dataframe

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notebook')
def notebook():
    # Lee el archivo del notebook
    with open('./app/src/Program_Huaman_Mendoza_Ramirez.ipynb') as f:
        notebook_content = f.read()
        notebook = nbformat.reads(notebook_content, as_version=4)
    
    # Convierte el notebook a HTML
    html_exporter = HTMLExporter()
    #html_exporter.template_file = 'basic'  # Puedes usar otro template si lo deseas
    #html_exporter.template_path.append('./app/templates')
    (body, _) = html_exporter.from_notebook_node(notebook)

    return render_template('notebook.html', body=body)

@app.route('/songs')
def songs():
    df = process_dataframe(NROWS=80, THRESHOLD=1.5, PATH="app/data/Dataset_Huaman_Mendoza_Ramirez_500.csv", print_df=False, print_processed_df=False)
    return render_template('songs.html', data=df.to_json(orient='records'))
if __name__ == '__main__':
    app.run(debug=True)