from django.shortcuts import render
from django.template import loader
from django.core.validators import validate_ipv4_address
from django.core.exceptions import ValidationError
import subprocess

from .forms import RequestForm

# Create your views here.
def index(request):

    if request.method == "POST":
        form = RequestForm(request.POST)

        subnet = form.data["subnet"]
        ipaddr = form.data["ipaddr"]
        try:
            validate_ipv4_address(ipaddr)
        except ValidationError:
            return render(request, "frontend/help/help.html")

        ipv4 = f"{ipaddr}/{subnet}"
        rate = form.data["rate"]
        lowerboundport = form.data["lowerboundport"]
        upperboundport = form.data.get("upperboundport")
        portrange = lowerboundport

        if upperboundport:
            portrange = f"{lowerboundport}-{upperboundport}"


        subprocess.run(['masscan', ipv4, '--ports', portrange, "--rate", rate, "-oJ", "results.json"], stdout=subprocess.PIPE)

        subprocess.run(['mongoimport', '-u', 'admin', '-p', 'password', '--db', 'masscanresults', '--collection', 'masscan_results', '--file', 'results.json', '--jsonArray'])

        subprocess.run(['rm', 'results.json'])

    form = RequestForm()
    return render(request, "frontend/index.html", {"form": form})

def about(request):
    template = loader.get_template('frontend/about/about.html')

    return render(request, "frontend/about/about.html")