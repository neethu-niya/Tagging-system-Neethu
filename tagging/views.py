from tagging.serializers import PostListSerializer,UserReactionSerializer
from rest_framework import viewsets
from .models import Post,UserReaction, PostTag
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Prefetch


class PostListing(viewsets.ModelViewSet):
    serializer_class = PostListSerializer
    http_method_names = ['get']
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def get_queryset(self):
       
        # import pdb
        # pdb.set_trace()
        #return Post.objects.prefetch_related('post_tag','post_tag__tag' ).filter(post_tag__tag__tag = "A")
        # q = Post.objects.prefetch_related(
        #       Prefetch('post_tag', queryset=PostTag.objects.select_related('tag').all().extra(
        #         select={'tag_data': 'tag_id'}
        # ))).extra(select={'is_top': "post_tag__tag_data = A"})
        # q = q.extra(order_by = ['-is_top'])
        return Post.objects.all()


class BlogReaction(APIView):
    
    def post(self,request):
        post_id = request.data.get("post_id")
        reaction = request.data.get("reaction")
        if reaction not in ["1","2","3"]:
            return Response({"message": "wrong reaction.","status":"failed"})
        if not post_id:
            return Response({"message": "post id required.","status":"failed"})
        post=Post.objects.filter(pk=post_id).first()
        if not post:
            return Response({"message": "no data found.","status":"failed"})
        obj = UserReaction.objects.get_or_create(post=post, user=request.user)[0]
        obj.reaction = reaction
        obj.save()
        return Response({"message": "Reaction submitted.","status":"success"})

class LikedUsersList(viewsets.ModelViewSet):
    serializer_class = UserReactionSerializer
    http_method_names = ['get']
    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        if not post_id:
            return UserReaction.objects.none()
        return UserReaction.objects.filter(post=post_id,reaction="1")

