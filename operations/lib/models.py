from django.db import models

class BaseManager(models.Manager):
    def get_queryset(self):
        return super(BaseManager, self).get_queryset().filter(deleted=False)

class BaseModel(models.Model):
    class Meta:
        abstract=True
        default_permissions = []
        
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    changed_at = models.DateTimeField(null=True, auto_now=True)
    deleted = models.BooleanField(default=False, db_index=True)
    
    objects = BaseManager()
    objects_original = models.Manager()

