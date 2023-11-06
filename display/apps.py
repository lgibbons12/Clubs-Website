from django.apps import AppConfig


class DisplayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'display'
    #add this in when the site is ready to go
    '''
    def ready(self):
        from email_schedule import scheduling
        scheduling.start()
    '''
