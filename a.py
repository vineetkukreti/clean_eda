from flask import Flask, render_template, request, send_file, redirect
import pandas as pd
import dtale
from try_main import Data_Preprocess
from dtale.app import build_app
from dtale.views import startup
import os

app = Flask(__name__)
app1 = build_app(reaper_on=False)
name = ''

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/preprocess', methods=['POST'])
def preprocess():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            return "No selected file"
        df = pd.read_csv(uploaded_file)
        excel_file_name = request.form['excel_file_name']
        if not excel_file_name:
            return "Excel file name not provided"
        global name
        name = excel_file_name
        change_datatype = request.form.get('change_datatype')
        column_name = request.form.get('column_name')
        new_datatype = request.form.get('new_datatype')
        target_column = request.form['target_column']
        data_processor = Data_Preprocess(df, excel_file_name)
        data_processor.run(change_datatype=change_datatype == 'Yes',
                           column_name=column_name,
                           new_datatype=new_datatype,
                           target_column=target_column)
        return render_template('preprocessed.html')
    return "Something went wrong"

# Utility function to read log file
def read_log_file(log_file_path):
    try:
        if not os.path.exists(log_file_path):
            return "Log file not found!"
        with open(log_file_path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        return f"Error reading log file: {str(e)}"

# @app.route('/logs')
# def show_logs():
#     global name
#     if not name:
#         return "Name parameter not provided"
#     log_content = read_log_file(f"{name}_logfile.log")
#     return render_template('log.html', content=log_content)

@app.route('/logs')  # Remove the question mark from here
def show_logs():
    global name
    if not name:
        return "Name parameter not provided"
    log_content = read_log_file(f"{name}_logfile.log")
    return render_template('log.html', content=log_content)


@app.route('/download/<filename>')
def download(filename):
    file_path = filename  # Assuming the file path is correct
    return send_file(file_path, as_attachment=True)

@app.route("/show_eda")
def create_df():
    current_directory = os.getcwd()
    print("**************eda****************")
    print(current_directory)
    df = pd.read_csv('eda.csv')
    d = dtale.show(df)
    d.open_browser()
    # d.kill()
    return "dfd"
    

if __name__ == "__main__":
    app.run(debug=True)
