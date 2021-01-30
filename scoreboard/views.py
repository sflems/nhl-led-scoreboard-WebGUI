from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import FieldError

from .forms import schema, SettingsDetailForm, SettingsJSONForm
from django_jsonforms.forms import JSONSchemaForm
from .models import *
from .services import *
import json

# Create your views here.
def index(request):
    games = todays_games()
    return render(request, "scoreboard/index.html", {"games":games,})

class SettingsList(ListView):
    model = Settings

@login_required
def settings_create(request):
    def schema():
        with open("./scoreboard/static/schema/config.schema.json", "r") as f:
            conf = json.load(f)
            return conf

    if request.method == "GET":
        # Settings Forms are instantiated in forms.py
        detailform = SettingsDetailForm()
        JSONform = SettingsJSONForm()
        return render(request, "scoreboard/settings_create.html", {
            "JSONform":JSONform, 
            "detailform":detailform,
        })
        
    if request.method == "POST":
        detailform = SettingsDetailForm(request.POST)
        # The request data for the config json must be encoded and then decoded again as below due to a BOM error. Without this the form submissions are saved as slash escaped strings... but why? Possibly due to jsonforms encoding methods.
        new_config = request.POST['json'].encode().decode('utf-8-sig')

        if detailform.is_valid():           
            
            name = detailform.cleaned_data['name']
            isActive = detailform.cleaned_data['isActive']

            active_profiles = Settings.objects.filter(isActive=True).exclude(name=name)
            new_settings = Settings.objects.create(name=name, isActive=isActive, config=json.loads(new_config))
            new_settings.save()

            notes = [
                " (Not Active)",
                " (Active)" 
            ]
            message = "Your profile has been saved." + notes[new_settings.isActive]
            messages.success(request, message)

            return HttpResponseRedirect(reverse(index), {"message": message,})

        elif FieldError:
            schema = schema()
            startval = json.loads(request.POST['json'])
            options = form_options(startval)

            # JSONResponse to refill form? This isnt working.
            return render(request, "scoreboard/settings_create.html", { 
                "error": "Profile with this name exists.", 
                "detailform": SettingsDetailForm(request.POST), 
                "JSONform": JSONSchemaForm(schema=schema, options=options, ajax=True)
                })
        else:      
            return render(request, "scoreboard/settings_create.html", { "error": "Invalid data.", })
            

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "scoreboard/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "scoreboard/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
    