from django.db import models


class Session(models.Model):
    name = models.CharField(max_length=255)
    dataset = models.CharField(max_length=255)
    date = models.DateField()
    accuracy = models.FloatField(null=True)
    time_taken = models.IntegerField(null=True)


class SessionProgress(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    file = models.CharField(max_length=100)
    ground_truth = models.IntegerField()
    result = models.IntegerField(null=True)
    difficulty = models.IntegerField(null=True)
    time_taken = models.FloatField(null=True)
    audio_position = models.FloatField(null=True)
    play_count = models.IntegerField(null=True)
    audio_length = models.FloatField(null=True)


class MediaState(models.Model):
    current_dataset = models.CharField(max_length=255)
    current_sample = models.CharField(max_length=255)


class QueuedFiles(models.Model):
    state = models.ForeignKey(MediaState, on_delete=models.CASCADE)
    file = models.CharField(max_length=255)
    ground_truth = models.IntegerField()



