from dotenv import load_dotenv
load_dotenv()

import os

from flask import Flask, render_template
from supabase import create_client

url = os.environ['SUPABASE_URL']
key = os.environ['SUPABASE_KEY']
supabase = create_client(url, key)

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('home.html')

print(__name__)
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)