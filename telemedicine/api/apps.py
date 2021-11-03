from django.apps import AppConfig
from telemedicine import settings


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from django.contrib.sites.models import Site
        
        #site = Site.objects.get_current()
        #site.domain = 'telemedicine.prj'
        #site.name = 'Tele Team'
