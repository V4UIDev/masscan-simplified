from django.shortcuts import render
from django.template import loader
import subprocess

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

        if upperboundport:
            portrange = f"{lowerboundport}-{upperboundport}"


        result = subprocess.run(['masscan', ipv4, '--ports', portrange, "--rate", rate, "-oJ", "results.json"], stdout=subprocess.PIPE)

        print(result.stdout) 

    form = RequestForm()
    return render(request, "frontend/index.html", {"form": form})