from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
import openpyxl
from openpyxl import Workbook
from modules.db import Database


app = Flask(__name__)
app.config['SECRET_KEY'] = 'MiaLaPesadita'  # Asegúrate de cambiar esto a una clave segura en un entorno de producción
db = Database()


class LoginForm(FlaskForm):
    username = StringField('Usuario')
    password = PasswordField('Contraseña')
    submit = SubmitField('Iniciar sesión')

usuarios = {
    'Gonzalo': {'contraseña': 'Gonza1234', 'pagina': 'Gonzalo'},
    'Camila': {'contraseña': 'Cami1234', 'pagina': 'camila'},
}

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username in usuarios and usuarios[username]['contraseña'] == password:
            flash('Inicio de sesión exitoso', 'success')
            # Aquí podrías redirigir a la página principal o a donde sea necesario después del inicio de sesión
            return redirect(url_for(usuarios[username]['pagina']))
        else:
            flash('Inicio de sesión fallido. Verifica tu usuario y contraseña', 'danger')

    return render_template('login.html', form=form)

@app.route('/camila')
def camila():
    conteo_ds = db.conteo_diario()
    return render_template('camila.html', conteo_ds=conteo_ds)

@app.route('/calcular_imc', methods=['POST'])
def calcular_imc():
    if request.method == 'POST':
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        imc = calcular_imc_real(peso, altura)
        return jsonify({'imc': imc})

def calcular_imc_real(peso, altura):
    # Fórmula del IMC: IMC = peso / (altura * altura)
    imc = peso / (altura ** 2)
    return round(imc, 2)

@app.route('/agregar_ds', methods=["POST"])
def agregar_ds():
    if request.method == 'POST':
        db.agregarDs()
        conteo_ds = db.conteo_diario()
        return jsonify({'conteo_ds': conteo_ds})

@app.route('/borrar_registro_diario', methods=["POST"])
def borrar_registro_diario():
    if request.method == 'POST':
        db.Eliminar_registro_diario()
        conteo_ds = db.conteo_diario()
        return jsonify({'conteo_ds': conteo_ds})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
