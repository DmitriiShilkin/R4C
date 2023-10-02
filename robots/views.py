# импорт библиотеки для работы датой и временем
import datetime
# импорт библиотеки для работы с файлами формата MS-Excel
import xlwt
# импорт рендера
from django.shortcuts import render
# импорт инструментов для работы с запросами
from django.http import HttpResponse
# импорт инструментов для множественной фильтрации и подсчета количества записей
from django.db.models import Q, Count

# импорт модели робот
from .models import Robot
# импорт списка моделей робота
from .validators import MODELS


# поиск роботов за указанное количество дней и требуемой модели
def get_new_robots(days, model):
    # определяем текущий день
    today = datetime.datetime.today()
    # определяем интервал времени от прошедшего до текущего дня
    time_ago = today - datetime.timedelta(days=days)
    # ищем роботов требуемой модели, созданных в указанный временной интервал
    robots = Robot.objects.filter(Q(created__gte=time_ago) & Q(model=model)).values('model', 'version').\
        annotate(count=Count('id'))

    return robots


# представление-заглушка для стартовой страницы
def index_view(request):

    return render(request, "index.html")


# представление для сохранения данных по роботам в файл xls
def stats_view(request):
    # формат данных
    response = HttpResponse(content_type='application/ms-excel')
    # формируем текущую дату для добавления к имени файла
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    # задаем имя файла
    response['Content-Disposition'] = 'attachment; filename="weekly_stats_{}.xls"'.format(date)
    # кодировка в книге эксель
    wb = xlwt.Workbook(encoding='utf-8')
    # список ячеек шапки таблицы
    columns = ['Модель', 'Версия', 'Количество за неделю', ]
    # список ключей словаря, по которым будем брать данным для строк таблицы
    dict_keys = ['model', 'version', 'count']

    # добавляем лист в книгу
    for model_num in range(len(MODELS)):
        # название листа книги
        model = MODELS[model_num]
        ws = wb.add_sheet(model)

        # добавляем таблицу
        # шапка таблицы
        row_num = 0
        # параметры шрифта
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        # записываем шапку таблицы
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # остальные строки
        # параметры шрифта
        font_style = xlwt.XFStyle()
        # получаем данные о роботах требуемой модели за последние 7 дней
        rows = get_new_robots(7, model)

        # записываем строки таблицы
        for row in rows:
            row_num += 1
            # записываем столбцы текущей строки
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, row[dict_keys[col_num]], font_style)

    # сохраняем книгу
    wb.save(response)
    return response
