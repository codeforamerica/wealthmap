from django.shortcuts import render

def about(request):
    return render(request, "primerpeso/about.jade", { 'title': 'About' })
