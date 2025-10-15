from django.apps import AppConfig


class PollsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "polls"
    
    def ready(self):
        """Initialize sample data when the app is ready."""
        import os
        from django.core.management import call_command
        
        # Only run in production (not during tests)
        if not os.environ.get('RUN_MAIN') and not os.environ.get('TESTING'):
            try:
                from .models import Question
                # Only create data if no questions exist
                if Question.objects.count() == 0:
                    call_command('create_sample_data')
            except Exception:
                # Ignore errors during startup
                pass
