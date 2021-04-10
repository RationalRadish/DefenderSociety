from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class Ouser(AbstractUser):
     link = models.URLField('Personal URL',blank=True,help_text='Reminder: URL must fill in the complete form starting with http')
     avatar = ProcessedImageField(upload_to='avatar/%Y/%m/%d',
                                  default='avatar/default.png',
                                  verbose_name='Portrait',
                                  processors=[ResizeToFill(80, 80)]
                                  )

     class Meta:
         verbose_name ='User'
         verbose_name_plural = verbose_name
         ordering = ['-id']

     def __str__(self):
         return self.username