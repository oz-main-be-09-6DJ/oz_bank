from django.http import HttpResponse

def test_home(request):
    return HttpResponse("This is a test home page!!")