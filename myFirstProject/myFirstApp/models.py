from django.db import models
from django.utils import timezone


class Base(models.Model):
    title = models.CharField(max_length=150)

    class Meta:
        abstract = True


class BaseNews(Base):
    description = models.CharField(max_length=4000)


class NewsItem(BaseNews):
    publish_date = models.DateField(default=timezone.now)

    def __str__(self):
        return '{0}'.format(self.title)


class Event (BaseNews):
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return '{0} : {1} - {2}'.format(self.title, self.start_date, self.end_date)