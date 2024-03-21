from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def login(request):
    if request.method == "GET":
        return render(request, "exemplo.html", {})
    else:
        return JsonResponse({'status':True})