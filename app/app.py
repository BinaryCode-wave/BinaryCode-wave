from flask import Flask, render_template
import nbformat
from nbconvert import HTMLExporter

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
if __name__ == '__main__':
    app.run(debug=True)