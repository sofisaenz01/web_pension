from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/formulario')
def contacto():
    return render_template('formulario.html')

@app.route('/calcular', methods=['POST'])
def calcular_pension():
    # Obtener datos del formulario
    nombre = request.form.get('nombre')
    apellidos = request.form.get('apellidos')
    genero = request.form.get('genero')
    dia = int(request.form.get('dia'))
    mes = int(request.form.get('mes'))
    anio = int(request.form.get('anio'))
    edad_inicio = int(request.form.get('edad_inicio'))
    semanas_colpensiones = int(request.form.get('semanas_colpensiones') or 0)
    semanas_privados = int(request.form.get('semanas_privados') or 0)
    regimen = request.form.get('regimen')
    salario = float(request.form.get('salario'))

    # Calcular edad actual (aproximada)
    from datetime import datetime
    hoy = datetime.now()
    edad = hoy.year - anio - ((hoy.month, hoy.day) < (mes, dia))

    # Total de semanas cotizadas
    semanas_totales = semanas_colpensiones + semanas_privados

    # Lógica de cálculo aproximado
    if regimen == 'colpensiones':
        if edad >= 62 and semanas_totales >= 1300:  # 62 años para hombres, 57 para mujeres
            porcentaje = min(1.0, (semanas_totales // 50) * 0.012)  # Máximo 100%
            pension = salario * porcentaje
            resultado = f"Estimado/a {nombre} {apellidos}, tu pensión aproximada con Colpensiones es: ${pension:,.0f}."
        else:
            resultado = "No cumples con la edad mínima (62 años) o 1,300 semanas cotizadas para Colpensiones."
    elif regimen == 'privados':
        # Aproximación: saldo acumulado = aportes + rendimientos simples
        anos_cotizados = edad - edad_inicio
        aportes_totales = salario * 0.12 * anos_cotizados  # 12% de aporte aproximado
        rendimientos = aportes_totales * 0.03 * anos_cotizados  # 3% anual aproximado
        saldo = aportes_totales + rendimientos
        pension = saldo / (20 * 12)  # Dividir entre 20 años en meses
        resultado = f"Estimado/a {nombre} {apellidos}, tu pensión aproximada con fondos privados es: ${pension:,.0f}."
    else:
        resultado = "Por favor, selecciona un régimen válido."

    return render_template('formulario.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)