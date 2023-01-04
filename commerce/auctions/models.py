from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import CATEGORY_CHOICES


class User(AbstractUser):
    pass


class Listing(models.Model):
    creator = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="listings"
    )
    title = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    bid = models.FloatField(default=0)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, blank=True)
    watchlist = models.ManyToManyField("User", blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} : {self.title} [{self.creator}]"


class Comment(models.Model):
    listing = models.ForeignKey(
        "Listing", on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey("User", on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.listing}, comment by {self.author} at {self.created}: {self.text}"
        )


class Bid(models.Model):
    listing = models.ForeignKey(
        "Listing", on_delete=models.CASCADE, related_name="bids"
    )
    bidder = models.ForeignKey("User", on_delete=models.CASCADE)
    bid = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing}, bid by {self.bidder} at {self.time}: {self.bid}"
