from django.db import models


class FaceRanking(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    comment = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.created_date.strftime('%Y-%m-%d %H:%M:%S')


class FaceFriend(models.Model):
    face_ranking = models.ForeignKey(FaceRanking, on_delete=models.CASCADE)
    face_id = models.CharField(max_length=32)
    face_name = models.CharField(max_length=100)
    score = models.IntegerField()

