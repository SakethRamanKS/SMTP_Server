from django.shortcuts import render,redirect
from signup.forms import signupForm
from django.http import HttpResponse
# import environ
#load_dotenv()
from django.views.generic import TemplateView
from django.contrib.auth import authenticate
import pymongo
import bcrypt
import os
def signup(request):
   request.POST.get("Username")
   if request.method == "POST":
      # mongo_user=os.environ.get('mongo_USERNAME')
      # mongo_pass=os.environ.get('mongo_PASSWORD')
      # dbname=os.environ.get('DATABASE')
      # collection=os.environ.get('COLLECTION')
      salt=bcrypt.gensalt()
      username=request.POST.get("Username")
      password = bcrypt.hashpw(request.POST.get("password").encode('utf-8'),salt)
      #myclient = pymongo.MongoClient(f"mongodb+srv://{mongo_user}:{mongo_pass}@cluster0.cew55.mongodb.net/{dbname}?retryWrites=true&w=majority")
      #mydb = myclient[dbname]
      #mycol = mydb[collection]
      myclient = pymongo.MongoClient("mongodb+srv://sanjay:1234@cluster0.cew55.mongodb.net/MailDB?retryWrites=true&w=majority")
      mydb = myclient["MailDB"]
      mycol = mydb["Users"]
      mydict = { "username": username, "password": password,"salt": salt}
      user=mycol.find_one({ "username": username })
      if not user:
         x = mycol.insert_one(mydict)
         print(x)
         return render(request, "success.html")
      else:
          return render(request, "failure.html")
   else:
       return redirect('/')
      #Form = signupForm()

    