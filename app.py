from dotenv import load_dotenv
load_dotenv()

import os
import json

from flask import Flask, render_template
from supabase import create_client

url = os.environ['SUPABASE_URL']
key = os.environ['SUPABASE_KEY']
supabase = create_client(url, key)


app = Flask(__name__)




@app.route("/")
def home():
  data = supabase.table("rooms").select("roomName").eq("roomType->events", "true").execute().json()
  json_data = json.loads(data)
  roomName = json_data["data"][0].get('roomName')
  
  roomList = []
  for obj in json_data["data"]:
    roomNameNew = obj["roomName"]
    roomList.append(roomNameNew)
  print(roomList)
  
  return render_template('home.html', roomName=roomName, roomList=roomList)

print(__name__)
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)