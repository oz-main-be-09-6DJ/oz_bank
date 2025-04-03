from django.test import TestCase
from users.models import CustomUser
from users.models import Notification


class NotificationModelTest(TestCase):
    def setUp(self):
        """테스트용 사용자 생성"""
        self.user = CustomUser.objects.create(name="testuser", email="test@example.com")

    def test_create_notification(self):
        """알림이 정상적으로 생성되는지 확인"""
        notification = Notification.objects.create(user=self.user, message="새로운 알림입니다.")
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.message, "새로운 알림입니다.")
        self.assertFalse(notification.is_read)  # 기본값이 False인지 확인

    def test_auto_now_add_created_at(self):
        """created_at 필드가 자동으로 설정되는지 확인"""
        notification = Notification.objects.create(user=self.user, message="시간 테스트")
        self.assertIsNotNone(notification.created_at)

    def test_delete_user_deletes_notifications(self):
        """사용자가 삭제되면 해당 사용자의 알림도 삭제되는지 확인"""
        notification = Notification.objects.create(user=self.user, message="삭제 테스트")
        self.assertEqual(Notification.objects.count(), 1)  # 알림이 생성되었는지 확인

        self.user.delete()  # 사용자 삭제
        self.assertEqual(Notification.objects.count(), 0)  # 알림이 삭제되었는지 확인
