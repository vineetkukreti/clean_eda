import pandas as pd
from dtale.app import build_app
from dtale.views import startup
from flask import redirect

if __name__ == '__main__':
    app = build_app(reaper_on=False)


    @app.route("/create-df")
    def create_df():
        df = pd.read_csv('isisi\eda.csv')
        instance = startup(data=df, ignore_duplicate=True)
        return redirect(f"/dtale/main/{instance._data_id}", code=302)


    @app.route("/")
    def hello_world():
        return 'Hi there, load data using <a href="/create-df">create-df</a>'


    app.run(host="0.0.0.0", port=8080)
