from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

# see https://docs.djangoproject.com/en/dev/topics/db/models/#extra-fields-on-many-to-many-relationships

# from https://stackoverflow.com/questions/29534257/set-imagefield-default-value-to-random-image-out-of-a-list-of-images-in-django
from pathlib import Path
from random import randint
import time
from django.core.files import File
from django.db import models
allowed_image_extensions = ['.jpg', '.png', '.jpeg']


class Hashtag(models.Model):
#    statement = models.ForeignKey(Statement, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    url = models.TextField()
    icon = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.text

    
class Statement(models.Model):
    statement_text = models.CharField(max_length=200)
#    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField()
    # body = models.TextField()
    # url = models.TextField()
    #blank=True, null=True, 
    image = models.ImageField(default='static/statements/opinion_choice.png', upload_to="images/")
    icon = models.ImageField(default='static/statements/opinion_choice.png',upload_to='images/')
    iconAgree = models.ImageField(default='static/statements/agree.png', upload_to='images/')
    iconDisagree = models.ImageField(default='static/statements/disagree.png', upload_to='images/')
    # votes_total = models.IntegerField(default = 1)    
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    agreeUsers = models.ManyToManyField(User, related_name="agreeUsers")
    disagreeUsers = models.ManyToManyField(User, related_name="disagreeUsers")
    dontcareUsers = models.ManyToManyField(User, related_name="dontcareUsers")
    dontknowUsers = models.ManyToManyField(User, related_name="dontknowUsers")
    hashtags = models.ManyToManyField(Hashtag, related_name="hashtags")

    def __str__(self):
        return self.statement_text[:100]

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')  

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    statement = models.ForeignKey(Statement, on_delete=models.CASCADE)
    response_date = models.DateTimeField()
    agree = models.IntegerField(default = 0)
    disagree = models.IntegerField(default = 0)
    latitude = models.FloatField(default=0, blank=False, null=False)
    longitude = models.FloatField(default=0, blank=False, null=False)

    def __str__(self):
        return self.statement.statement_text

    def __num0__(self):
        return Response.objects.filter(answer=0).count()

class UserGeoLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField(blank=False, null=False)
    longitude = models.FloatField(blank=False, null=False)



################################################################################

def get_file_extension(file_path):
    return Path(file_path).suffix


def get_files_in_directory(directory, absolute_path=False):
    from os import listdir
    from os.path import isfile
    only_files = [f for f in listdir(directory) if isfile("{}/{}".format(directory, f))]

    if not absolute_path:
        return only_files

    else:
        return ["{}/{}".format(directory, file_) for file_ in only_files]


def get_post_image_path(instance, filename):
    path_first_component = 'posts'
    ext = get_file_extension(filename)
    current_time_stamp = int(time.time())
    file_name = '{}/posts_{}_{}{}'.format(path_first_component, instance.id, current_time_stamp, ext)
    full_path = path_first_component + file_name
    return full_path