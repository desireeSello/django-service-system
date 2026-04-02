from django.core.management.base import BaseCommand
from reporting.models import Province, Municipality, IssueCategory

class Command(BaseCommand):
    help = 'Load initial data for provinces, municipalities, and categories'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('\n Loading provinces...'))
        
        provinces_data = [
            ('EC', 'Eastern Cape'),
            ('FS', 'Free State'),
            ('GP', 'Gauteng'),
            ('KZN', 'KwaZulu-Natal'),
            ('LP', 'Limpopo'),
            ('MP', 'Mpumalanga'),
            ('NC', 'Northern Cape'),
            ('NW', 'North West'),
            ('WC', 'Western Cape'),
        ]
        
        provinces = {}
        for code, name in provinces_data:
            province, created = Province.objects.get_or_create(code=code, name=name)
            provinces[code] = province
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ {name}'))
        
        self.stdout.write(self.style.SUCCESS('\n Loading municipalities...'))
        
        municipalities_data = [
            ('JHB', 'City of Johannesburg', 'GP'),
            ('TSH', 'City of Tshwane', 'GP'),
            ('EKU', 'Ekurhuleni', 'GP'),
            ('ETH', 'eThekwini', 'KZN'),
            ('CPT', 'City of Cape Town', 'WC'),
            ('NMA', 'Nelson Mandela Bay', 'EC'),
            ('MNG', 'Mangaung', 'FS'),
            ('RUS', 'Rustenburg', 'NW'),
            ('MBO', 'City of Mbombela', 'MP'),
        ]
        
        for code, name, province_code in municipalities_data:
            mun, created = Municipality.objects.get_or_create(
                code=code,
                name=name,
                province=provinces[province_code]
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ {name}'))
        
        self.stdout.write(self.style.SUCCESS('\n Loading issue categories...'))
        
        categories_data = [
            ('Electricity Faults', ''),
            ('Potholes', ''),
            ('Water Leaks', ''),
            ('Waste Collection', ''),
        ]
        
        for name, icon in categories_data:
            cat, created = IssueCategory.objects.get_or_create(
                name_en=name,
                defaults={'icon': icon}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ {name}'))
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS(' ALL DATA LOADED SUCCESSFULLY!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'\n Summary:')
        self.stdout.write(f'   Provinces: {Province.objects.count()}')
        self.stdout.write(f'   Municipalities: {Municipality.objects.count()}')
        self.stdout.write(f'   Categories: {IssueCategory.objects.count()}')
        self.stdout.write(self.style.SUCCESS('\n Refresh your homepage to see the dropdowns!'))