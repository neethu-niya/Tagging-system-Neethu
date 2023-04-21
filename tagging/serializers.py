from rest_framework import serializers

class PostListSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200)
    created_at = serializers.DateTimeField()
    images = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()
    dislike = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    
    def get_images(self, obj):
        return [img.image.url for img in obj.image_set.all()]
        
    def get_like(self, obj):
        user = self.context.get('user')
        return obj.is_user_liked(user)

    def get_dislike(self, obj):
        user = self.context.get('user')
        return obj.is_user_disliked(user)

    def get_likes(self,obj):
        return obj.likes()
    
    def get_dislikes(self,obj):
        return obj.likes()

    def get_id(self,obj):
        return obj.pk

class UserReactionSerializer(serializers.Serializer):
    post = serializers.CharField(max_length=200)
    liked_user = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    
    def get_liked_user(self, obj):
        return obj.user.username
    def get_user_id(self, obj):
        return obj.user_id       