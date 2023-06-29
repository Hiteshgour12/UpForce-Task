from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','role','created_at','last_update_at')
    list_filter = ("role",)
    search_fields = ['name']
admin.site.register(User,UserAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('id','title','author', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
admin.site.register(Post,PostAdmin)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('id','liked_by', 'post','created_at')
    list_filter = ("liked_by","post")
    search_fields = ['liked_by', 'post']

admin.site.register(Like,LikeAdmin)