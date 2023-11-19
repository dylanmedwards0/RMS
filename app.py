from dotenv import load_dotenv


load_dotenv()

import json
import os
import supabase


from flask import Flask, render_template, request, session, jsonify
from supabase import Client, create_client

url = os.environ['SUPABASE_URL']
key = os.environ['SUPABASE_KEY']
supabase: Client = create_client(url, key)

app = Flask(__name__)
app.secret_key = 'super secret key'
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True



orgData = supabase.table("organization").select("subdomain").execute().json()
orgjson_data = json.loads(orgData)
orgList = []
for obj in orgjson_data["data"]:
  orgList.append(obj["subdomain"])
  
@app.route("/<subdomain>", methods=['GET', 'POST'])
def landingPage(subdomain):
    if subdomain in orgList:
      if request.method == 'POST':
         email: str = request.form.get('email')
         password: str = request.form.get('password')
         data = supabase.table("login").select("id").eq("email", email).execute().json()
         dataP = supabase.table("login").select("email").eq("password", password).execute().json()
         print(data)
         print(data)
         print(data)
         print(data)
         json_data = json.loads(data)
         json_dataP = json.loads(dataP)
         if len(json_data["data"].get(id)) == 0:
          print("Failed")
          return render_template("login.html", subdomain=subdomain, loginError="Email or password is incorrect")
         elif not json_dataP["data"]:
           print("Failed2")
           return render_template("login.html", subdomain=subdomain, loginError="Email or password is incorrect")
         emailIDs = []
         for obj in json_dataP["data"]:
          emailIDs.append([obj["email"]])
            
         tempEmail = ""
         for emails in emailIDs:
            if emails[0] == email:
              print(emails)
              print(email)
              tempEmail = email

         if tempEmail == "":
            print("Failed3")
            return render_template("login.html", subdomain=subdomain, loginError="Email or password is incorrect")
         else:
           loginID = json_data["data"][0].get('id')
           data2 = supabase.table("organization").select("subdomain").eq("id", loginID).execute().json()
           json_data2 = json.loads(data2)
           subdomain1 = json_data["data"][0].get('subdomain')
           return render_template('login.html', subdomain=subdomain)
      return render_template('login.html', subdomain=subdomain)
    else:
        # Handle cases where the subdomain is not found, e.g., return to home
        return render_template("home.html", subdomain=subdomain)
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

  data = supabase.table("rooms").select("roomName" ,"availability").eq("availability", "TRUE").execute().json()
  
  json_data = json.loads(data)

  roomList = []
  for obj in json_data["data"]:
    roomList.append([obj["roomName"], obj["availability"]])
  
  
  return render_template('signup.html', roomList = roomList)

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
     for char in email:
       if char == "@":
        break
       elif char != "@":
        username += char
        print(char)

     data = supabase.table("login").select("email").execute().json()
     json_data = json.loads(data)
     noDuplicates = true;
     for check in json_data["data"]:
      if check["email"] == email:
          noDuplicates = false 
        
      if noDuplicates == true:
        data, count = supabase.table("login").insert({"id": 1, "username": username, "email": email, "password": password}).execute()
        supabase.auth.sign_up({ "email": email, "password": password })
      
      
     return render_template('createAccount.html', email=email, password=password, username=username)
  return render_template('createAccount.html')


@app.route("/eventsCalendar", methods=['GET', 'POST'])
def eventsCal():
    # Get the URL parameters using request.args.get()
    currentDate = request.args.get('currentDate')
    nextDate = request.args.get('nextDate')

    data = supabase.table("reservations").select("startTime","endTime","fName").gte('startTime', currentDate).lt('startTime', nextDate).execute().json()
    json_data = json.loads(data)
    jsonify(json_data)
  
    return render_template('eventsCalendar.html',json_data=json_data)

# /fetchEvents is for testing, Pulled the data query into /eventsCalendar
@app.route("/fetchEvents", methods=['GET', 'POST'])
def fetchEvents():
   # Get the URL parameters using request.args.get()
   currentDate = request.args.get('currentDate')
   nextDate = request.args.get('nextDate')
  
   data = supabase.table("reservations").select("startTime","endTime","fName").gte('startTime', currentDate).lt('startTime', nextDate).execute().json()
   json_data = json.loads(data)
   return jsonify(json_data)

if __name__ == "__main__":
    app.jinja_env.auto_reload = False
    app.config['TEMPLATES_AUTO_RELOAD'] = False
    app.run(debug=True, host='0.0.0.0')
