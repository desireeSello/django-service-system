# reporting/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from .models import Report, IssueCategory, Province, Municipality
import json

def homepage(request):
    """
    Assignment Homepage - Matches layout.docx exactly
    """
    
    if request.method == 'POST':
        return submit_report(request)
    
    total_reported = Report.objects.count()
    
    resolved_count = Report.objects.filter(status='resolved').count()
    
    acknowledged_count = Report.objects.filter(status='acknowledged').count()
    
    pending_count = Report.objects.filter(
        Q(status='reported') | Q(status='in_progress')
    ).count()
    
    recent_reports = Report.objects.all().order_by('-created_at')[:10]
    
    provinces = Province.objects.all().order_by('name')
    
    categories = IssueCategory.objects.all()
    
    context = {
        'total_reported': total_reported,
        'resolved_count': resolved_count,
        'pending_count': pending_count,
        'acknowledged_count': acknowledged_count,
        'recent_reports': recent_reports,
        'provinces': provinces,
        'categories': categories,
        'page_title': 'Welcome to CityMenderSA'
    }
    
    return render(request, 'reporting/home.html', context)


def submit_report(request):
    """Handle report submission"""
    if request.method == 'POST':
        category_id = request.POST.get('category')  
        province_code = request.POST.get('province')
        municipality_code = request.POST.get('municipality')
        address = request.POST.get('address_description')
        description = request.POST.get('description')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        language = request.POST.get('reported_language', 'en')
        
        category = IssueCategory.objects.get(id=category_id)
        province = Province.objects.get(code=province_code)
        municipality = Municipality.objects.get(code=municipality_code)
        
        report = Report.objects.create(
            category=category,
            province=province,
            municipality=municipality,
            address_description=address,
            description=description,
            phone_number=phone,
            email=email,
            reported_language=language
        )
        
        return redirect('reporting:success', ref=report.reference_number)
    
    return redirect('reporting:homepage')


def get_municipalities(request):
    """AJAX endpoint for municipality dropdown"""
    province_code = request.GET.get('province_code')
    
    if province_code:
        municipalities = Municipality.objects.filter(
            province__code=province_code
        ).values('code', 'name').order_by('name')
        
        return JsonResponse(list(municipalities), safe=False)
    
    return JsonResponse([], safe=False)


def success(request, ref):
    """Success page after report submission"""
    report = Report.objects.get(reference_number=ref)
    return render(request, 'reporting/success.html', {'report': report})