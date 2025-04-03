import datetime
from unittest import TestCase
from django.contrib.auth import get_user_model

from analysis.models import Analysis

User = get_user_model()


class AnalysisModelTestCase(TestCase):
    def setUp(self):
        # User.objects.filter(email="analysis_test3@test.com").delete()

        user = User.objects.create(
            email="analysis_test4324234233@test.com",
            name="박유진3",
            nickname="analysis_test4324234233",
            phone_number="01185695541",
            password="qwer1234",
        )

        Analysis.objects.create(
            analysis_description="test analysis description",
            result_image="테스트 이미지 입니다.",
            user=user,
        )

    ## 테스트
    # 생성된 인스턴스 카운트
    def test_analysis_creation(self):
        objects_count = Analysis.objects.count()

        self.assertEqual(objects_count, 1)

    # 각 필드에 잘 들어 갔는지 확인 (기본값들도 확인)
    def test_transaction_fields(self):
        analysis = Analysis.objects.first()

        self.assertEqual(analysis.analysis_about, "TOTAL_SPENDING")
        self.assertEqual(analysis.analysis_type, "DAILY")
        self.assertEqual(analysis.period_start, datetime.date.today())
        self.assertEqual(analysis.period_end, datetime.date.today())
        self.assertEqual(analysis.analysis_description, "test analysis description")
        self.assertEqual(analysis.result_image, "테스트 이미지 입니다.")

    # 관계 테이블 확인(유저 정보)
    def test_transaction_relationship(self):
        analysis = Analysis.objects.first()
        user = analysis.user

        self.assertEqual(user.email, 'analysis_test4324234233@test.com')
