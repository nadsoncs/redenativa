from django.db import models

class OrgManager(models.Manager):
    def update(self, **kwargs):
        allowed_attributes = {'name', 'email', 'tipo', 'tel', 'localidade', 'logo'}
        for name, value in kwargs.items():
            assert name in allowed_attributes
            setattr(self, name, value)
        self.save()