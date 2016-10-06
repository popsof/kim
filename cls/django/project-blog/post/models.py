from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField( max_length=40 )
    description = models.CharField( max_length=100 )
    # img_cover = models.ImageField(blank=True)
    content = models.TextField()
    view_count = models.IntegerField( default = 0 )
    like_count = models.IntegerField( default = 0)
    # ip_address = models.IPAddressField( blank = True )
    created = models.DateTimeField( auto_now_add = True )

    def __str__(self):
        return "{}:{}".format( self.id, self.title )
