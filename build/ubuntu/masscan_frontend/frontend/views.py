from django.shortcuts import render
from django.template import loader

from .forms import RequestForm

# Create your views here.
def index(request):

    template = loader.get_template('frontend/index.html')
    if request.method == "POST":
        form = RequestForm(request.POST)
        print(form.data)
    form = RequestForm()
    return render(request, "frontend/index.html", {"form": form})