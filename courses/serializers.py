from rest_framework import serializers 
from .models import Course,OrderCourses,OwnedCourse


class CourseSerializerWithoutFile(serializers.ModelSerializer):
    class Meta:
        model= Course
        fields = ["title", "description", "price", "createdAt", "id", "students", "available", "thumbnail"]


class CourseSerializerWithFile(serializers.ModelSerializer):
    class Meta:
        model= Course
        fields = "__all__"


class OrderCourseSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = OrderCourses
        fields = "__all__"

    def get_course(self,obj):
        course = obj.course
        serializer = CourseSerializerWithoutFile(course, many=False)
        return serializer.data


class OwnedCourseWithFileSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = OwnedCourse
        fields = "__all__"

    def get_course(self,obj):
        course = obj.course
        serializer = CourseSerializerWithFile(course, many=False)
        return serializer.data


class OwnedCourseWithoutFileSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = OwnedCourse
        fields = "__all__"

    def get_course(self,obj):
        course = obj.course
        serializer = CourseSerializerWithoutFile(course, many=False)
        return serializer.data
