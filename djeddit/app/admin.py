from django.contrib import admin
from .models import UserProfile,Sub,Post,Comment, Vote
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Sub)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Vote)