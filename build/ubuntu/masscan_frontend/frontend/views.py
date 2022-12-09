from django.shortcuts import render
from django.template import loader
import subprocess
import os

from .forms import RequestForm

# Create your views here.
def index(request):

    template = loader.get_template('frontend/index.html')
    if request.method == "POST":
        form = RequestForm(request.POST)

        subnet = form.data["subnet"]
        ipaddr = form.data["ipaddr"]
        ipv4 = f"{ipaddr}/{subnet}"
        rate = form.data["rate"]
        lowerboundport = form.data["lowerboundport"]
        upperboundport = form.data.get("upperboundport")
        portrange = lowerboundport
        mongodbusername = os.environ.get('MS_MONGODB_USERNAME')
        mongodbpassword = os.environ.get('MS_MONGODB_PASSWORD')

        if upperboundport:
            portrange = f"{lowerboundport}-{upperboundport}"


        subprocess.run(['masscan', ipv4, '--ports', portrange, "--rate", rate, "-oJ", "results.json"], stdout=subprocess.PIPE)

        subprocess.run(['mongoimport', '-u', mongodbusername, '-p', mongodbpassword, '--db', 'masscanresults', '--collection', 'masscan_results', '--file', 'results.json', '--jsonArray'])

        subprocess.run(['rm', 'results.json'])

    form = RequestForm()
    return render(request, "frontend/index.html", {"form": form})

def about(request):
    template = loader.get_template('frontend/about/about.html')

    return render(request, "frontend/about/about.html")