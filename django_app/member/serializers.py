from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


# class UserSerializer(serializers.Serializer):
#     pk = serializers.IntegerField(read_only=True)
#     username = serializers.CharField(max_length=36)
#     password = serializers.CharField()
#     email = serializers.EmailField()
#
#     user_type = serializers.CharField()
#
#     def create(self, validated_data):
#         """
#         검증한 데이터로 새 'MyUser' 인스턴스를 생성하여 리턴
#         :param validated_data:
#         :return:
#         """
#         return User.objects.create_user(
#             username=validated_data['username'],
#
#         )
#
#     def update(self, instance, validated_data):
#         """
#         검증한 데이터로 기존 'MyUser' 인스턴스를 업데이트한 후 리턴
#         :param instance:
#         :param validated_data:
#         :return:
#         """
#         instance.username = validated_data.get('username', instance.username)
#         instance.password = validated_data.get('password', instance.password)
#         instance.email = validated_data.get('email', instance.email)
#
#         instance.save()
#         return instance

##
# ModelSerializer
#   - 필드를 자동으로 인식한다.
#   - create() 와 update() 가 이미 구현되어 있다.
##
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')