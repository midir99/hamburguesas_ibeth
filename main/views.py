from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import Dish
from django.urls import reverse, reverse_lazy
from django.views import generic
from datetime import datetime


def menu_view(request):
    desserts = Dish.objects.filter(category='Postre', is_enabled=True)
    desserts_half = desserts.count() // 2
    desserts1 = desserts[:desserts_half]
    desserts2 = desserts[desserts_half:]
    drinks = Dish.objects.filter(category='Bebida', is_enabled=True)
    drinks_half = drinks.count() // 2
    drinks1 = drinks[:drinks_half]
    drinks2 = drinks[drinks_half:]
    now = datetime.now()
    months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
              'Noviembre', 'Diciembre']
    if now.weekday() < 5:
        str_now = 'Lo sentimos, solo abrimos en fines de semana'
    else:
        str_now = f'{now.day} de {months[now.month - 1]}, {now.year}'

    context = {
        'nbar': 'menu',
        'hamburgers': Dish.objects.filter(category='Hamburguesa', is_enabled=True),
        'tortas': Dish.objects.filter(category='Torta', is_enabled=True),
        'drinks1': drinks1,
        'drinks2': drinks2,
        'desserts1': desserts1,
        'desserts2': desserts2,
        'todays_date': str_now,
    }
    return render(request, 'main/index.html', context)


def cart_view(request):
    return render(request, 'main/cart.html', {})


class MenuAdminView(LoginRequiredMixin, generic.ListView):
    model = Dish
    context_object_name = 'menu'
    paginate_by = 4
    template_name = 'main/menu_admin.html'

    def get_queryset(self):
        return Dish.objects.order_by('-units_sold')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Dish.category_choices
        context['categories'] = categories
        return context

@login_required
def menu_admin(request):
    category = request.GET.get('category', '')
    name = request.GET.get('name', '')
    page = request.GET.get('page', 1)

    objs = Dish.objects.filter(category__icontains=category, name__icontains=name)
    categories = Dish.category_choices

    p = Paginator(objs, 5)
    try:
        page_obj = p.page(page)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    menu = page_obj
    query_params = f'&name={name}&category={category}'
    context = {
        'menu': menu,
        'page_obj': page_obj,
        'categories': categories,
        'paginator': p,
        'category': category,
        'name': name,
        'query_params': query_params,
    }
    return render(request, 'main/menu_admin.html', context)


def search_dish(request):
    category = request.GET.get('category', '')
    name = request.GET.get('name', '')
    objs = Dish.objects.filter(category__icontains=category, name__icontains=name)

    def to_dict(e: Dish):
        if e.img:
            img_url = e.img.url
        else:
            img_url = ''

        return {'name': e.name, 'price': e.price, 'id': e.id, 'units_sold': e.units_sold, 'is_enabled': e.is_enabled,
                'img_url': img_url }

    objs = list(map(to_dict, objs))
    return JsonResponse({ 'dishes': objs })


class DishCreate(LoginRequiredMixin, generic.edit.CreateView):
    model = Dish
    success_url = '/menu_admin/'
    template_name = 'main/create_dish_form.html'
    fields = [
        'name',
        'description',
        'price',
        'is_enabled',
        'category',
        'units_sold',
        'img'
    ]


def dish_delete(request, question_id):
    page = request.GET.get('page', '')
    category = request.GET.get('category', '')
    name = request.GET.get('name', '')
    try:
        dish = Dish.objects.get(pk=question_id)
        dish.delete()
    except:
        pass

    redirect_url = f'{reverse("main:menu_admin")}?page={page}&name={name}&category={category}'
    return HttpResponseRedirect(redirect_url)


class DishDetailView(generic.DetailView):
    model = Dish
    template_name = 'main/dish_detail.html'


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    fields = ['name', 'description', 'price', 'category', 'is_enabled', 'img']
    template_name = 'main/update_dish_form.html'
    success_url = '/menu_admin/'