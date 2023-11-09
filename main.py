from flask import Flask, render_template, request, send_file
import openpyxl
from openpyxl import Workbook

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/capitalizar_texto')
def capitalizar_texto():
    return render_template('capitalize_post.html')

@app.route('/capitalize', methods=['POST'])
def capitalize():
    text = request.form['text']
    text = text.replace('\\n', '\n')
    lineas = [line.strip() for line in text.split('\n')]
    lineas_capitalizadas = []

    for palabras in lineas:
        palabras_capitalizadas = [palabra.capitalize() for palabra in palabras.split()]
        linea_capitalizada = " ".join(palabras_capitalizadas)
        lineas_capitalizadas.append(linea_capitalizada)

    capitalize_text = "\n".join(lineas_capitalizadas)

    # Crear un archivo Excel
    wb = Workbook()
    ws = wb.active
    ws.append(['Texto capitalizado'])

    for linea in lineas_capitalizadas:
        ws.append([linea])

    excel_file = 'capitalized_text.xlsx'
    wb.save(excel_file)

    # Devolver un enlace para descargar el archivo Excel
    return render_template('capitalized_text.html', capitalize_text=capitalize_text, excel_file=excel_file)

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
