from dotenv import load_dotenv

load_dotenv()

import json
import os

import supabase

# import psycopg2
from flask import Flask, render_template, request, session
from supabase import Client, create_client

url = os.environ['SUPABASE_URL']
key = os.environ['SUPABASE_KEY']
supabase: Client = create_client(url, key)

app = Flask(__name__)
app.secret_key = 'super secret key'
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def home():

  #Query the Database for relevant data per route. Returns APIRequest, translate that to json with .json(), which creates a Dict with a nested List, and a nested Dict in that list. The format to access is: Variable["Dict"][indexOfList].get('Dict')
  
  data = supabase.table("rooms").select("roomName" ,"availability").eq("availability", "TRUE").execute().json()
  
  json_data = json.loads(data)

  roomList = []
  for obj in json_data["data"]:
    roomList.append([obj["roomName"], obj["availability"]])
  print(roomList)
  
  return render_template('home.html', roomList=roomList, supabase=supabase, url = url, key = key)
  
@app.route("/book-a-room", methods=['GET', 'POST'])
def bookroom():
  
  data = supabase.table("rooms").select("roomName" ,"availability").eq("availability", "TRUE").execute().json()
  
  json_data = json.loads(data)
  #  roomName = json_data["data"][0].get('roomName')

  
  roomList = []
  for obj in json_data["data"]:
    roomList.append([obj["roomName"], obj["availability"]])

  if request.method == 'POST':
        # Updated json method to "model_dump_json" from error messaging
        #data = supabase.table("rooms").select("roomName" ,"availability").eq("availability", "TRUE").execute().json()
        data = supabase.table("rooms").select("roomName" ,"availability").eq("availability", "TRUE").execute().model_dump_json()
        for obj in json_data["data"]:
         roomList.append([obj["roomName"], obj["availability"]])
        json_data = json.loads(data)
        session['roomList'] = roomList
        return render_template('bookRoom.html', supabase=supabase, roomList=roomList, test="THIS IS WORKING")
       
  return render_template('bookRoom.html', supabase=supabase, roomList=roomList, test="default")
        
@app.route("/signup", methods=['GET', 'POST'])
def signup():
  # This block is if we want to run the confirmation to run on the signup page. Currently handled with signupConfirmation
  #if request.method == 'POST':
    # Retrieve form data
  #  firstName = request.form.get['fName']
  #  lastName = request.form.get['lName']
    # Render a new page (signupConfirmation.html) with the submitted data
  #  return render_template('signupConfirmation.html', firstName=firstName, lastName=lastName)

  return render_template('signup.html')


@app.route("/signupConfirmation", methods=['GET', 'POST'])
def signupConfirmation():

  return render_template('signupConfirmation.html', firstName=request.form['fName'], lastName=request.form['lName'], email=request.form['email'], startTime=request.form['startTime'], endTime=request.form['endTime'])

@app.route("/createAccount", methods=['GET', 'POST'])
def createAccount():
  
    # Authentication - Sign up module
  if request.method == 'POST':
     email: str = request.form.get('email')
     password: str = request.form.get('password')
     username: str = ""
     print("made it")
     for char in email:
       if char == "@":
        break
       elif char != "@":
            username += char
            print(char)
        
     print('username is', username)
     data, count = supabase.table("login").insert({"id": 1, "username": username, "email": email, "password": password}).execute()
     supabase.auth.sign_up({ "email": email, "password": password })
      
      
     return render_template('createAccount.html', email=email, password=password, username=username)
  return render_template('createAccount.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
     email: str = request.form.get['email']
     password: str = request.form.get['password']
     data = supabase.table("login").select("id").eq("email", email).execute().json()
     json_data = json.loads(data)
     loginID = json_data["data"][0].get('id')
     data2 = supabase.table("organization").select("subdomain").eq("id", loginID).execute().json()
     json_data2 = json.loads(data2)
     subdomain = json_data["data2"][0].get('subdomain')
     #if subdomain :
     #  
     # supabase.auth.sign_in({ "email": email, "password": password })
     # 
     # return render_template('login.html')
     return render_template('login.html')

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=False, host='0.0.0.0')
