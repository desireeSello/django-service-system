from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from django.utils import timezone
from reporting.models import Report
from datetime import timedelta

def dashboard_view(request):
    """Dashboard - Track all reports"""
    
    
    all_reports = Report.objects.all()
    
   
    total_reports = all_reports.count()
    resolved_reports = all_reports.filter(status='resolved').count()
    acknowledged_reports = all_reports.filter(status='acknowledged').count()
    pending_reports = all_reports.filter(
        Q(status='reported') | Q(status='in_progress')
    ).count()
    
    
    active_list = all_reports.order_by('-created_at')[:10]
    
    context = {
        'total_reports': total_reports,
        'resolved_reports': resolved_reports,
        'acknowledged_reports': acknowledged_reports,
        'pending_reports': pending_reports,
        'active_list': active_list,
    }
    
    return render(request, 'tracking/dashboard.html', context)


def report_detail_view(request, ref_number):
    """Detailed report tracking"""
    report = get_object_or_404(Report, reference_number=ref_number)
    status_updates = report.updates.all().order_by('created_at') if hasattr(report, 'updates') else []
    
    status_progress = {
        'reported': 10,
        'acknowledged': 40,
        'in_progress': 75,
        'resolved': 100,
    }
    progress = status_progress.get(report.status, 0)
    
    context = {
        'report': report,
        'status_updates': status_updates,
        'progress': progress,
    }
    
    return render(request, 'tracking/report_detail.html', context)


def community_dashboard_view(request):
    """Public community view"""
    category_stats = Report.objects.values('category__name_en').annotate(
        total=Count('id'),
        resolved=Count('id', filter=Q(status='resolved'))
    )
    
    context = {
        'category_stats': category_stats,
    }
    
    return render(request, 'tracking/community_dashboard.html', context)