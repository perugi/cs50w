from django.contrib import admin

from .models import User, Listing, Comment, Bid

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)