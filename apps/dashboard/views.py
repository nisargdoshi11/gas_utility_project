from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')
    
@login_required
def customer_dashboard(request):
    # Get user's recent requests
    recent_requests = ServiceRequest.objects.filter(
        customer=request.user
    ).order_by('-created_at')[:5]
    
    # Get request statistics
    total_requests = ServiceRequest.objects.filter(customer=request.user).count()
    pending_requests = ServiceRequest.objects.filter(
        customer=request.user,
        status='pending'
    ).count()
    resolved_requests = ServiceRequest.objects.filter(
        customer=request.user,
        status='resolved'
    ).count()
    
    context = {
        'recent_requests': recent_requests,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'resolved_requests': resolved_requests,
    }
    return render(request, 'dashboard/customer_dashboard.html', context)


@login_required
def customer_statistics(request):
    # Get monthly request statistics
    last_6_months = timezone.now() - timedelta(days=180)
    monthly_stats = ServiceRequest.objects.filter(
        customer=request.user,
        created_at__gte=last_6_months
    ).extra(
        select={'month': 'EXTRACT(month FROM created_at)'}
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    context = {
        'monthly_stats': monthly_stats,
    }
    return render(request, 'dashboard/customer_statistics.html', context)


@login_required
def staff_dashboard(request):
    if not request.user.is_staff_member:
        return redirect('dashboard:customer_dashboard')
    
    # Handle filters
    filter_form = ServiceRequestFilterForm(request.GET)
    requests = ServiceRequest.objects.all()
    
    if filter_form.is_valid():
        status = filter_form.cleaned_data.get('status')
        priority = filter_form.cleaned_data.get('priority')
        date_from = filter_form.cleaned_data.get('date_from')
        date_to = filter_form.cleaned_data.get('date_to')
        
        if status:
            requests = requests.filter(status=status)
        if priority:
            requests = requests.filter(priority=priority)
        if date_from:
            requests = requests.filter(created_at__gte=date_from)
        if date_to:
            requests = requests.filter(created_at__lte=date_to)
    
    # Get summary statistics
    urgent_requests = requests.filter(priority='urgent').count()
    pending_requests = requests.filter(status='pending').count()
    unassigned_requests = requests.filter(assigned_to=None).count()
    
    context = {
        'filter_form': filter_form,
        'requests': requests[:10],  # Latest 10 requests
        'urgent_requests': urgent_requests,
        'pending_requests': pending_requests,
        'unassigned_requests': unassigned_requests,
    }
    return render(request, 'dashboard/staff_dashboard.html', context)


@login_required
def staff_statistics(request):
    if not request.user.is_staff_member:
        return redirect('dashboard:customer_dashboard')
    
    # Get various statistics for staff view
    last_30_days = timezone.now() - timedelta(days=30)
    
    daily_stats = ServiceRequest.objects.filter(
        created_at__gte=last_30_days
    ).extra(
        select={'day': 'DATE(created_at)'}
    ).values('day').annotate(
        total=Count('id'),
        resolved=Count('id', filter=Q(status='resolved')),
        pending=Count('id', filter=Q(status='pending'))
    ).order_by('day')
    
    context = {
        'daily_stats': daily_stats,
    }
    return render(request, 'dashboard/staff_statistics.html', context)


@login_required
def staff_reports(request):
    if not request.user.is_staff_member:
        return redirect('dashboard:customer_dashboard')
    
    # Generate summary reports for staff
    total_requests = ServiceRequest.objects.count()
    
    # Calculate average resolution time for resolved requests
    resolution_time_avg = ServiceRequest.objects.filter(
        status='resolved'
    ).extra(
        select={'resolution_time': 'EXTRACT(epoch FROM (updated_at - created_at))/3600'}
    ).values('resolution_time').aggregate(avg_time=models.Avg('resolution_time'))
    
    context = {
        'total_requests': total_requests,
        'resolution_time_avg': resolution_time_avg['avg_time'],
    }
    return render(request, 'dashboard/staff_reports.html', context)



@login_required
def request_summary(request):
    """API endpoint for dashboard summary data"""
    if request.user.is_staff_member:
        data = {
            'total': ServiceRequest.objects.count(),
            'pending': ServiceRequest.objects.filter(status='pending').count(),
            'urgent': ServiceRequest.objects.filter(priority='urgent').count(),
        }
    else:
        data = {
            'total': ServiceRequest.objects.filter(customer=request.user).count(),
            'pending': ServiceRequest.objects.filter(
                customer=request.user,
                status='pending'
            ).count(),
        }
    return JsonResponse(data)


@login_required
def monthly_stats(request):
    """API endpoint for monthly statistics"""
    last_6_months = timezone.now() - timedelta(days=180)
    query = ServiceRequest.objects.filter(created_at__gte=last_6_months)
    
    if not request.user.is_staff_member:
        query = query.filter(customer=request.user)
    
    stats = query.extra(
        select={'month': 'EXTRACT(month FROM created_at)'}
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    return JsonResponse(list(stats), safe=False)

