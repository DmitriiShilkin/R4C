# импорт рендера
from django.shortcuts import render


# представление-заглушка для стартовой страницы
def index_view(request):

    return render(request, "index.html")
