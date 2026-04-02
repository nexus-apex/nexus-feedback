import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import FeedbackItem, FeedbackCategory, FBResponse


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['feedbackitem_count'] = FeedbackItem.objects.count()
    ctx['feedbackitem_bug'] = FeedbackItem.objects.filter(category='bug').count()
    ctx['feedbackitem_feature'] = FeedbackItem.objects.filter(category='feature').count()
    ctx['feedbackitem_complaint'] = FeedbackItem.objects.filter(category='complaint').count()
    ctx['feedbackcategory_count'] = FeedbackCategory.objects.count()
    ctx['feedbackcategory_total_avg_rating'] = FeedbackCategory.objects.aggregate(t=Sum('avg_rating'))['t'] or 0
    ctx['fbresponse_count'] = FBResponse.objects.count()
    ctx['fbresponse_draft'] = FBResponse.objects.filter(status='draft').count()
    ctx['fbresponse_sent'] = FBResponse.objects.filter(status='sent').count()
    ctx['recent'] = FeedbackItem.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def feedbackitem_list(request):
    qs = FeedbackItem.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(category=status_filter)
    return render(request, 'feedbackitem_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def feedbackitem_create(request):
    if request.method == 'POST':
        obj = FeedbackItem()
        obj.title = request.POST.get('title', '')
        obj.customer_name = request.POST.get('customer_name', '')
        obj.customer_email = request.POST.get('customer_email', '')
        obj.category = request.POST.get('category', '')
        obj.rating = request.POST.get('rating') or 0
        obj.status = request.POST.get('status', '')
        obj.priority = request.POST.get('priority', '')
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/feedbackitems/')
    return render(request, 'feedbackitem_form.html', {'editing': False})


@login_required
def feedbackitem_edit(request, pk):
    obj = get_object_or_404(FeedbackItem, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '')
        obj.customer_name = request.POST.get('customer_name', '')
        obj.customer_email = request.POST.get('customer_email', '')
        obj.category = request.POST.get('category', '')
        obj.rating = request.POST.get('rating') or 0
        obj.status = request.POST.get('status', '')
        obj.priority = request.POST.get('priority', '')
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/feedbackitems/')
    return render(request, 'feedbackitem_form.html', {'record': obj, 'editing': True})


@login_required
def feedbackitem_delete(request, pk):
    obj = get_object_or_404(FeedbackItem, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/feedbackitems/')


@login_required
def feedbackcategory_list(request):
    qs = FeedbackCategory.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = ''
    return render(request, 'feedbackcategory_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def feedbackcategory_create(request):
    if request.method == 'POST':
        obj = FeedbackCategory()
        obj.name = request.POST.get('name', '')
        obj.items_count = request.POST.get('items_count') or 0
        obj.avg_rating = request.POST.get('avg_rating') or 0
        obj.response_time_hrs = request.POST.get('response_time_hrs') or 0
        obj.owner = request.POST.get('owner', '')
        obj.active = request.POST.get('active') == 'on'
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/feedbackcategories/')
    return render(request, 'feedbackcategory_form.html', {'editing': False})


@login_required
def feedbackcategory_edit(request, pk):
    obj = get_object_or_404(FeedbackCategory, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.items_count = request.POST.get('items_count') or 0
        obj.avg_rating = request.POST.get('avg_rating') or 0
        obj.response_time_hrs = request.POST.get('response_time_hrs') or 0
        obj.owner = request.POST.get('owner', '')
        obj.active = request.POST.get('active') == 'on'
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/feedbackcategories/')
    return render(request, 'feedbackcategory_form.html', {'record': obj, 'editing': True})


@login_required
def feedbackcategory_delete(request, pk):
    obj = get_object_or_404(FeedbackCategory, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/feedbackcategories/')


@login_required
def fbresponse_list(request):
    qs = FBResponse.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(feedback_title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'fbresponse_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def fbresponse_create(request):
    if request.method == 'POST':
        obj = FBResponse()
        obj.feedback_title = request.POST.get('feedback_title', '')
        obj.responder = request.POST.get('responder', '')
        obj.response = request.POST.get('response', '')
        obj.date = request.POST.get('date') or None
        obj.internal_note = request.POST.get('internal_note', '')
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/fbresponses/')
    return render(request, 'fbresponse_form.html', {'editing': False})


@login_required
def fbresponse_edit(request, pk):
    obj = get_object_or_404(FBResponse, pk=pk)
    if request.method == 'POST':
        obj.feedback_title = request.POST.get('feedback_title', '')
        obj.responder = request.POST.get('responder', '')
        obj.response = request.POST.get('response', '')
        obj.date = request.POST.get('date') or None
        obj.internal_note = request.POST.get('internal_note', '')
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/fbresponses/')
    return render(request, 'fbresponse_form.html', {'record': obj, 'editing': True})


@login_required
def fbresponse_delete(request, pk):
    obj = get_object_or_404(FBResponse, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/fbresponses/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['feedbackitem_count'] = FeedbackItem.objects.count()
    data['feedbackcategory_count'] = FeedbackCategory.objects.count()
    data['fbresponse_count'] = FBResponse.objects.count()
    return JsonResponse(data)
