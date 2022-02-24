from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    likes_count= serializers.SerializerMethodField(read_only=True)
    class Meta:
        model= Blog
        fields= "__all__"

    def get_likes_count(self,obj):
        likes_count= obj.like_set.all().count()
        return likes_count