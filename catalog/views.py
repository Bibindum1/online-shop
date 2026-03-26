from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic import DetailView
from django.views.decorators.http import require_POST
from django.db import transaction
import json
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Product
from .forms import CategoryForm, ProductForm



@csrf_exempt
@login_required
def user_logout(request):
    logout(request)
    return redirect('catalog:index')
def category_list(request):
    query = request.GET.get('q', '')
    categories = Category.objects.all()

    if query:
        categories = categories.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    paginator = Paginator(categories, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': page_obj,
        'query': query,
        'show_dragdrop': request.user.is_authenticated
    }
    return render(request, 'catalog/categories/list.html', context)


def product_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    sort = request.GET.get('sort', 'name')

    products = Product.objects.select_related('category').all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    if category_id:
        products = products.filter(category_id=category_id)

    sort_options = {
        'name': 'name',
        'price': 'price',
        'price_desc': '-price',
        'created_at': '-created_at',
        'stock': 'stock'
    }
    products = products.order_by(sort_options.get(sort, 'name'))

    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.filter(is_active=True)

    context = {
        'products': page_obj,
        'categories': categories,
        'query': query,
        'category_id': category_id,
        'sort': sort,
        'total_count': products.count(),
        'show_dragdrop': request.user.is_authenticated
    }
    return render(request, 'catalog/products/list.html', context)


def public_page(request):
    products = Product.objects.all()

    return render(request, 'catalog/public.html', {
        'title': 'Публичная страница',
        'products': products,
    })


@login_required
def client_page(request):
    return render(request, 'catalog/client.html', {
        'title': 'Страница клиента'
    })


@staff_member_required
def manager_page(request):
    return render(request, 'catalog/manager.html', {
        'title': 'Страница менеджера'
    })


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно создана')
            return redirect('catalog:category_list')
        else:
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = CategoryForm()

    context = {
        'form': form,
        'title': 'Добавить категорию'
    }
    return render(request, 'catalog/categories/form.html', context)


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно обновлена')
            return redirect('catalog:category_list')
        else:
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category': category,
        'title': f'Редактировать: {category.name}'
    }
    return render(request, 'catalog/categories/form.html', context)


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        if category.products.exists():
            messages.error(request,
                           f'Нельзя удалить категорию "{category.name}". '
                           f'В ней {category.products.count()} товаров')
        else:
            category.delete()
            messages.success(request, 'Категория успешно удалена')
        return redirect('catalog:category_list')

    context = {
        'category': category,
        'products_count': category.products.count()
    }
    return render(request, 'catalog/categories/confirm_delete.html', context)


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успешно создан')
            return redirect('catalog:product_list')
        else:
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = ProductForm()

    context = {
        'form': form,
        'title': 'Добавить товар'
    }
    return render(request, 'catalog/products/form.html', context)


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успешно обновлен')
            return redirect('catalog:product_list')
        else:
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
        'title': f'Редактировать: {product.name}'
    }
    return render(request, 'catalog/products/form.html', context)


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Товар "{product_name}" удален')
        return redirect('catalog:product_list')

    context = {
        'product': product
    }
    return render(request, 'catalog/products/confirm_delete.html', context)


class ProductDetailAdminView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Product
    template_name = 'catalog/products/product_detail_admin.html'
    context_object_name = 'product'

    def test_func(self):
        return (self.request.user.is_superuser or
                self.request.user.is_staff or
                self.request.user.groups.filter(name='admin').exists())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery'] = self.object.gallery.all()
        context['main_image'] = self.object.gallery.filter(is_main=True).first()
        context['is_admin'] = True
        return context


# AJAX проверки
def category_check_slug(request):
    slug = request.GET.get('slug', '')
    exists = Category.objects.filter(slug=slug).exists()
    return JsonResponse({'exists': exists})


def product_check_slug(request):
    slug = request.GET.get('slug', '')
    exists = Product.objects.filter(slug=slug).exists()
    return JsonResponse({'exists': exists})


@login_required
@require_POST
@csrf_exempt
def reorder_categories(request):
    try:
        data = json.loads(request.body)
        order = data.get('order', [])

        if not order:
            return JsonResponse({'success': False, 'error': 'Пустой список'})

        with transaction.atomic():
            for i, category_id in enumerate(order):
                Category.objects.filter(id=category_id).update(position=i)

        return JsonResponse({'success': True, 'message': f'Переупорядочено {len(order)} категорий'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@require_POST
@csrf_exempt
def reorder_products(request):
    try:
        data = json.loads(request.body)
        order = data.get('order', [])

        if not order:
            return JsonResponse({'success': False, 'error': 'Пустой список'})

        with transaction.atomic():
            for i, product_id in enumerate(order):
                Product.objects.filter(id=product_id).update(position=i)

        return JsonResponse({'success': True, 'message': f'Переупорядочено {len(order)} товаров'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
