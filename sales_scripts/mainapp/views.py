from django.shortcuts import render

# Create your views here.

def main(request):
    title = 'главная'

    content = {
        'title': title
    }

    return render(request, 'mainapp/index.html', content)