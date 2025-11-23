from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def principal():
    return render_template('index.html')  

@app.route('/formulario')
def formulario():
    return render_template('formulario.html', resultado=None, fondo=None)

@app.route('/procesar', methods=['POST'])
def procesar():
    nombre = request.form.get('nombre')
    apellidos = request.form.get('apellidos')
    salario = float(request.form.get('salario'))
    fondo = request.form.get('fondo')        # Esta línea ya la tenías
    semanas = int(request.form.get('semanas'))
    edad = int(request.form.get('edad'))
    arl = float(request.form.get('arl'))
    aporte_arl = salario * arl

    if fondo == "colpensiones":
        pension = salario * 0.65
        resultado = (
            f"Estimado/a {nombre} {apellidos}, tu pensión aproximada con Colpensiones es: "
            f"${pension:,.0f}. Aporte mensual ARL: ${aporte_arl:,.0f}."
        )
    else:
        base = semanas * 10
        rendimiento = salario * 0.10
        pension = base + rendimiento
        resultado = (
            f"Estimado/a {nombre} {apellidos}, tu pensión aproximada con fondos privados es: "
            f"${pension:,.0f}. Aporte mensual ARL: ${aporte_arl:,.0f}."
        )

    # Aquí pasamos ambas variables
    return render_template("formulario.html", resultado=resultado, fondo=fondo)

if __name__ == '__main__':
    app.run(debug=True)
