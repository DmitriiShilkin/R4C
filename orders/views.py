# импортируем рендер для функциональных вью
from django.shortcuts import render
# импортируем стандартный дженерик для вью, создающего новые записи
from django.views.generic import CreateView
# импортируем инструмент, который позволяет обращаться к url их name
from django.urls import reverse_lazy

# импортируем модели робота и заказа, а также форму для отправки заказа
from robots.models import Robot
from .forms import OrderForm
from .models import Order


# преставление для создания нового заказа
class OrderView(CreateView):
    # используемая форма
    form_class = OrderForm
    # используемая модель
    model = Order
    # имя шаблона, в соответствии с которым информация будет отображаться на странице
    template_name = 'order_create.html'
    # контекстное имя объекта для использования в шаблоне
    context_object_name = 'order'
    # куда переходим при успешном создании заказа
    success_url = reverse_lazy('order_success')

    # для того, чтобы передать серийный номер из одного вью в другой, его нужно сохранить в текущей сессии
    def form_valid(self, form):
        if self.request.method == 'POST':
            # сохраняем введенную в форму данные без сохранения в БД
            order = form.save(commit=False)
            # сохраняем серийный номер для текущей сессии
            self.request.session['robot_serial'] = order.robot_serial
        # сохраняем данные формы в БД
        return super().form_valid(form)


# представление для вывода сообщения о созданном заказе
def order_success_view(request):
    # забираем серийный номер из текущей сессии
    robot_serial = request.session.get('robot_serial')

    # формируем переменные для контекста шаблона
    context = {
        'exists': Robot.objects.filter(serial=robot_serial).exists(),
        'model': robot_serial[:2],
        'version': robot_serial[-2:]
    }
    # передаем контекст в шаблон и рендерим
    return render(request, "order_success.html", context)
