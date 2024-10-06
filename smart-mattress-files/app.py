from flask import Flask, render_template, jsonify, send_file
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from fpdf import FPDF

import main


"""
The main App, contains the backend of the web app, interact with index.html
"""
# Use the Agg backend for Matplotlib
plt.switch_backend('Agg')

app = Flask(__name__)

# Dummy data for percentages
percentages = {
    'BACK': 0,
    'LEFT SIDE': 0,
    'RIGHT SIDE': 0,
    'STOMACH': 0,
    'EMPTY': 0,
}

positions = {
    0: "BACK",
    1: "LEFT SIDE",
    2: "RIGHT SIDE",
    3: "STOMACH",
    5: "EMPTY"}

@app.route('/')
def index():
    return render_template('index.html')

"""
Activate the mattress prediction functionality 
(main.record_one_sample_and_calculate)
"""
@app.route('/generate', methods=['POST'])
def generate():
    matrix, prediction = main.record_one_sample_and_calculate()
    plt.imshow(matrix, cmap='viridis')
    plt.axis('off')
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    heatmap_base64 = base64.b64encode(buf.read()).decode('utf-8')
    text = get_position_caption(prediction)
    percentages[positions[prediction]] += 1

    return jsonify({
        'heatmap': heatmap_base64,
        'text': text
    })

def get_position_caption(value):
    positions = { 0: "BACK", 1: "LEFT SIDE", 2: "RIGHT SIDE", 3: "STOMACH", 5: "EMPTY" }
    return positions.get(value)

"""
calculating the position time percentage
"""
@app.route('/percentage', methods=['GET'])
def percentage():
    total = percentages['BACK'] + percentages['LEFT SIDE'] + percentages['RIGHT SIDE'] + percentages['STOMACH'] + percentages['EMPTY']
    return jsonify({
        'back': (percentages['BACK'] / total) * 100 if total > 0 else 0,
        'left_side': (percentages['LEFT SIDE'] / total) * 100 if total > 0 else 0,
        'right_side': (percentages['RIGHT SIDE'] / total) * 100 if total > 0 else 0,
        'stomach': (percentages['STOMACH'] / total) * 100 if total > 0 else 0,
        'empty': (percentages['EMPTY'] / total) * 100 if total > 0 else 0
    })

"""
Creates a PDF report from the positions recorded information (duration in each 
position, and the screenshot of the heatmap during the recording)
"""
@app.route('/create_report', methods=['POST'])
def create_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Sleep Report", ln=True)
    total = percentages['BACK'] + percentages['LEFT SIDE'] + percentages['RIGHT SIDE'] + percentages['STOMACH'] + percentages['EMPTY']
    pdf.cell(200, 10, txt=f"Back: {(percentages['BACK'] / total) * 100 if total > 0 else 0:.2f}%", ln=True)
    pdf.cell(200, 10, txt=f"Left side: {(percentages['LEFT SIDE'] / total) * 100 if total > 0 else 0:.2f}%", ln=True)
    pdf.cell(200, 10, txt=f"Right side: {(percentages['RIGHT SIDE'] / total) * 100 if total > 0 else 0:.2f}%", ln=True)
    pdf.cell(200, 10, txt=f"Stomach: {(percentages['STOMACH'] / total) * 100 if total > 0 else 0:.2f}%", ln=True)
    pdf.cell(200, 10, txt=f"Empty: {(percentages['EMPTY'] / total) * 100 if total > 0 else 0:.2f}%", ln=True)

    buf = BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name='report.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Replace 5001 with your desired port
