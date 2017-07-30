from rest_framework import generics
from rest_framework import permissions

from ..serializers import BookInfoSerializer
from ..models import BookInfo

##
# - 인증 받은 사용자만 데이터를 생성할 수 있다.
# - 해당 데이터를 만든 사람만 이를 편집하거나 삭제할 수 있다.
# - 인증받지 않은 사용자는 '읽기 전용'으로만 사용 가능하다.
##


class BookList(generics.ListCreateAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer

    ##
    # 코드 조각을 만들었더라도 해당 코드 조각을 만든 사용자와 아무 관게를 맺지 않았다.
    # 사용자는 직렬화된 표현에 나타나지 않았고 요청하는 측에서 지정하는 속성이었을 뿐이다.
    # 이를 해결하기 위해 뷰에서 perform_create() 오버라이딩
    #   - 인스턴스를 저장하는 과정을 조정하며 요청이나 요청 url 에서 정보를 가져와 원하는 대로 다룰 수 있다.검증한 요청 데이터 + 'owner' 필드도 전달
    ##
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        # 검증한 요청 데이터 + 'owner' 필드도 전달

    # 인증 받은 사용자만 데이터 생성/업데이트/삭제
    #   IsAuthenticatedOrReadOnly : 인정 받은 요청에 읽기와 쓰기 권한 부여 인증 받지 않은 요청에 대해 읽기 권한만 부여한다.
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    pass