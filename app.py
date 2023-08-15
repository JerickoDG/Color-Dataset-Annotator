from flask import Flask, render_template, request
import pandas as pd
import os
import datetime

MAIN_PATH = os.path.join(os.getcwd())
ORIG_FILE_NAME = 'final_data_colors - Copy.csv' # If you have progress, change this to the filename of CSV file where you had your progress.

app = Flask(__name__)

@app.route('/')
def index():
    colors_data = []

    df = pd.read_csv(os.path.join(MAIN_PATH, ORIG_FILE_NAME))
    df['HexCode'] = df.apply(lambda row: f'#{row["red"]:02X}{row["green"]:02X}{row["blue"]:02X}', axis=1)
    colors_data = df.to_dict(orient='records')
        
    colors_data = sorted(colors_data, key=lambda x: x['label'])
    
    return render_template('index.html', colors_data=colors_data, update_success=False)

@app.route('/update_colors', methods=['POST'])
def update_colors():
    red_values = request.form.getlist('red[]')
    green_values = request.form.getlist('green[]')
    blue_values = request.form.getlist('blue[]')
    label_values = request.form.getlist('label[]')
    hex_codes = request.form.getlist('hexCode[]')

    colors_data = {
        'red': red_values,
        'green': green_values,
        'blue': blue_values,
        'label': label_values,
        'HexCode': hex_codes
    }

    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f'modified_colors_{formatted_datetime}.csv'
    pd.DataFrame(colors_data).drop(['HexCode'], axis=1).to_csv(os.path.join(MAIN_PATH, filename), index=False)

    return render_template('index.html', colors_data=pd.DataFrame(colors_data).to_dict('records'), update_success=True)

def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'. format(r, g, b)

if __name__ == '__main__':
    app.run(debug=True)
