from django.apps import AppConfig


class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'

    def ready(self):
        # Cloudinary Settings
        import cloudinary
        import cloudinary.uploader
        import cloudinary.api

        cloudinary.config(
            cloud_name='dmji6uxrt',
            api_key='745654639178649',
            api_secret='p3fN0OREEpKdihPeGkp6-viVbEs'
        )
