from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Profile


class ProfileSerializer(ModelSerializer):
    user_name = SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'user_name')

    def get_user_name(self, obj: Profile):
        return obj.user.username
