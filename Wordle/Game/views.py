from django.http import HttpResponse
from django.shortcuts import render
import json

# Create your views here.

def draw_game(request):
    with open("./words.json", 'r') as f:
        x = json.loads(f.read())
    print(x['words'])
    return render(request, template_name="game/index.html")