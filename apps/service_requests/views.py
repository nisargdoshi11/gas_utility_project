# apps/service_requests/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import ServiceRequest
from .forms import ServiceRequestForm, RequestCommentForm, RequestUpdateForm

@login_required
def request_list(request):
    requests = ServiceRequest.objects.filter(customer=request.user)
    paginator = Paginator(requests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'service_requests/request_list.html', {'page_obj': page_obj})

@login_required
def create_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = request.user
            service_request.save()
            messages.success(request, 'Service request created successfully!')
            return redirect('service_requests:request_detail', pk=service_request.pk)
    else:
        form = ServiceRequestForm()
    return render(request, 'service_requests/create_request.html', {'form': form})

@login_required
def request_detail(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    if request.method == 'POST':
        comment_form = RequestCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.request = service_request
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('service_requests:request_detail', pk=pk)
    else:
        comment_form = RequestCommentForm()
    
    return render(request, 'service_requests/request_detail.html', {
        'service_request': service_request,
        'comment_form': comment_form
    })

@login_required
def request_update(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    if not request.user.is_staff_member:
        messages.error(request, 'You do not have permission to update requests.')
        return redirect('service_requests:request_detail', pk=pk)
    
    if request.method == 'POST':
        form = RequestUpdateForm(request.POST, instance=service_request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Request updated successfully!')
            return redirect('service_requests:request_detail', pk=pk)
    else:
        form = RequestUpdateForm(instance=service_request)
    
    return render(request, 'service_requests/request_update.html', {
        'form': form,
        'service_request': service_request
    })

@login_required
def staff_dashboard(request):
    if not request.user.is_staff_member:
        messages.error(request, 'Access denied. Staff only area.')
        return redirect('dashboard:customer_dashboard')
    
    requests = ServiceRequest.objects.all()
    paginator = Paginator(requests, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'service_requests/staff_dashboard.html', {
        'page_obj': page_obj
    })