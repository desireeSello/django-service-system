# reporting/models.py
from django.db import models
from django.utils import timezone
import uuid

class Province(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Provinces"
    
    def __str__(self):
        return self.name

class Municipality(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='municipalities')
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name}"

class IssueCategory(models.Model):
    """Supports translation for all 11 SA languages"""
    name_en = models.CharField(max_length=100)  
    name_zu = models.CharField(max_length=100, blank=True)
    name_xh = models.CharField(max_length=100, blank=True)
    name_af = models.CharField(max_length=100, blank=True)
    name_ses = models.CharField(max_length=100, blank=True)
    name_ts = models.CharField(max_length=100, blank=True)
    name_sep = models.CharField(max_length=100, blank=True)
    name_ven = models.CharField(max_length=100, blank=True)
    name_nde = models.CharField(max_length=100, blank=True)
    name_ss = models.CharField(max_length=100, blank=True)
    
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class", default="fa-solid fa-circle-exclamation")
    
    def __str__(self):
        return self.name_en
    
    def get_name_by_language(self, lang_code):
        """Get category name in requested language"""
        lang_map = {
            'en': self.name_en, 'zu': self.name_zu, 'xh': self.name_xh,
            'af': self.name_af, 'ses': self.name_ses, 'set': self.name_ts,
            'sep': self.name_sep, 'ven': self.name_ven, 'nde': self.name_nde,
            'ss': self.name_ss, 'ts': self.name_ts
        }
        name = lang_map.get(lang_code) or self.name_en
        return name if name else self.name_en


class Report(models.Model):
    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('acknowledged', 'Acknowledged by Municipality'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    
    reference_number = models.CharField(max_length=20, unique=True, editable=False)
    
    category = models.ForeignKey(IssueCategory, on_delete=models.PROTECT, related_name='reports')
    
    province = models.ForeignKey(Province, on_delete=models.PROTECT, related_name='reports')
    municipality = models.ForeignKey(Municipality, on_delete=models.PROTECT, related_name='reports')
    ward = models.CharField(max_length=20, blank=True, help_text="Optional ward number")
    
    gps_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    gps_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    address_description = models.TextField(help_text="Describe the exact location (building, landmark, etc.)")
    
    description = models.TextField()
    photo = models.ImageField(upload_to='reports/photos/', blank=True, null=True)
    
    reported_language = models.CharField(
        max_length=10,
        choices=[
            ('en', 'English'), ('zu', 'isiZulu'), ('xh', 'isiXhosa'), ('af', 'Afrikaans'),
            ('ses', 'Sesotho'), ('set', 'Setswana'), ('ss', 'siSwati'), ('ve', 'Tshivenda'),
            ('ts', 'Xitsonga'), ('nde', 'isiNdebele'), ('sep', 'Sepedi')
        ],
        default='en'
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    
    municipal_reference = models.CharField(max_length=100, blank=True, help_text="Official municipality reference")
    tracking_link = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    
    session_key = models.CharField(max_length=40, blank=True, db_index=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reference_number} - {self.category.name_en}"
    
    def save(self, *args, **kwargs):
        if not self.reference_number:
            date_str = timezone.now().strftime('%Y%m%d')
            random_suffix = uuid.uuid4().hex[:4].upper()
            self.reference_number = f"CM-{date_str}-{random_suffix}"
        super().save(*args, **kwargs)
    
    @property
    def is_resolved(self):
        return self.status == 'resolved'

class ReportUpdate(models.Model):
    """For status updates and municipality communication"""
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='updates')
    updated_by = models.CharField(max_length=100, help_text="Resident, Municipality, or System")
    message = models.TextField()
    status_change = models.CharField(max_length=20, choices=Report.STATUS_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True, help_text="Show on public dashboard")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.report.reference_number} - {self.status_change or 'Update'}"