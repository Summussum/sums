from sums.models import Users

test = Users.objects.create_user(username="test", email="test@test.com", password="admin123")
test.save()