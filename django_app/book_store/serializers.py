from rest_framework import serializers
from rest_framework import permissions

from .models import BookInfo


class BookInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInfo
        fields = ('id', 'username', 'password', 'email', 'book_info', 'owner')

    owner = serializers.ReadOnlyField(source='owner.user')
    # source 인자로 특정 필드를 지정
    # 직렬화된 인스턴스의 속성 뿐만아니라 마침표 표기 방식을 통해 속성을 탐색(Django 템플릿 언어)
    # ReadOnlyField : 타입이 없는 클래스 이를 직렬화에 사용했을 땐 언제나 읽기 전용 모델 인스턴스 업데이트 불가능
    # CharField(read_only=True) 와 같은 기능 수행

    # 인증 받은 사용자만 코드 조각을 생성/업데이트/삭제
