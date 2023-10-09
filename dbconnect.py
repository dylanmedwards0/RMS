from dotenv import load_dotenv
load_dotenv()

import os
import json
import supabase
#import psycopg2


from flask import Flask, render_template, Blueprint, request, flash
from supabase import create_client, Client

url = os.environ['SUPABASE_URL']
key = os.environ['SUPABASE_KEY']
supabase: Client = create_client(url, key)

app = Flask(__name__)
app.secret_key = 'super secret key'



@app.route("/createReservation")
def createRes():

  # Connect to the database
conn = psycopg2.connect(
    host=url,
    database="rooms",
    user="supabase_admin",
    password=key
)
  #dbconnection

  
   return 'User created successfully!'


print(__name__)
if __name__ == "__main__":
  app.jinja_env.auto_reload = True
  app.run(host='0.0.0.0', debug=True)