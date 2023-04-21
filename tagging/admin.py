from django.contrib import admin
from .models import Post,Image,UserReaction,Tag,PostTag


# admin.site.register(Post)
admin.site.register(Image)
admin.site.register(UserReaction)
admin.site.register(Tag)
admin.site.register(PostTag)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','like_count','dislikes')
    readonly_fields = ["like_count","dislikes"]

admin.site.register(Post,PostAdmin)