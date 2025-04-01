from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # schema/ 경로로 OpenAPI 스펙(JSON)을 반환하는 API
    # 이 API를 통해 Swagger에서 API 정보 제공
    # http://localhost:8000/schema/에 접속하면 JSON 형태의 OpenAPI 문서 제공

    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # swagger/ 경로에 Swagger UI를 제공하는 뷰
    # swagger UI는 API를 더 직관적으로 테스트할 수 있는 웹 페이지 제공
    # http://localhost:8000/swagger/에 접속하면 Swagger 문서 페이지 제공

    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # redoc/ 경로에서 Redoc 스타일 API 문서를 제공하는 뷰
    # Redoc은 Swagger와 비슷하지만, 조금 더 깔끔하고 정리된 문서 페이지 제공
    # http://localhost:8000/redoc/에 접속하면 Redoc 기반의 API 문서 페이지 제공
]