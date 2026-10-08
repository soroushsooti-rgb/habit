from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from habit.models import Habit
from .forms import AccountChangeForm, AccountCreationForm
from .models import User
from .serializers import RegisterSerializer


class CustomUserTests(TestCase):
    password = 'River!Sky-7429-Pine'

    def test_project_uses_accounts_model_and_habit_relation(self):
        self.assertIs(get_user_model(), User)
        self.assertEqual(User._meta.label, 'accounts.User')
        self.assertIs(Habit._meta.get_field('user').remote_field.model, User)

    def test_manager_hashes_password_and_normalizes_email(self):
        user = User.objects.create_user('member', 'Name@EXAMPLE.COM', self.password)
        self.assertEqual(user.email, 'Name@example.com')
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(authenticate(username='member', password=self.password), user)

    def test_manager_rejects_missing_username_and_invalid_superuser_flags(self):
        with self.assertRaises(ValueError):
            User.objects.create_user('')
        for field in ('is_staff', 'is_superuser', 'is_active'):
            with self.assertRaises(ValueError):
                User.objects.create_superuser('admin', password=self.password, **{field: False})

    def test_superuser_permissions(self):
        user = User.objects.create_superuser('admin', 'admin@example.com', self.password)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.has_perm('accounts.change_user'))

    def test_group_permissions_and_habit_ownership(self):
        user = User.objects.create_user('member', password=self.password)
        group = Group.objects.create(name='Editors')
        permission = Permission.objects.get(content_type__app_label='accounts', codename='change_user')
        group.permissions.add(permission)
        user.groups.add(group)
        self.assertTrue(user.has_perm('accounts.change_user'))
        habit = Habit.objects.create(user=user, name='Read')
        self.assertEqual(Habit.objects.get(pk=habit.pk).user, user)

    def test_admin_forms_use_custom_model_and_hash_password(self):
        form = AccountCreationForm(data={
            'username': 'admin-created', 'email': 'member@example.com',
            'password1': self.password, 'password2': self.password,
        })
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertIsInstance(user, User)
        self.assertTrue(user.check_password(self.password))
        self.assertIs(AccountChangeForm._meta.model, User)

    def test_registration_rejects_invalid_email_and_password_confirmation(self):
        valid = {
            'username': 'newmember', 'email': 'new@example.com',
            'password': self.password, 'password_confirm': self.password,
        }
        for field, value in [
            ('email', ''), ('email', 'invalid'), ('username', ''),
            ('password_confirm', 'different'),
        ]:
            serializer = RegisterSerializer(data={**valid, field: value})
            self.assertFalse(serializer.is_valid())
            self.assertIn(field, serializer.errors)
        for field in valid:
            serializer = RegisterSerializer(data={key: value for key, value in valid.items() if key != field})
            self.assertFalse(serializer.is_valid())
            self.assertIn(field, serializer.errors)
        self.assertFalse(User.objects.filter(username='newmember').exists())

    def test_admin_registration_requires_email_and_matching_passwords(self):
        data = {'username': 'newmember', 'password1': self.password, 'password2': self.password}
        form = AccountCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        form = AccountCreationForm(data={**data, 'email': 'new@example.com', 'password2': 'different'})
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_existing_account_api_uses_custom_user(self):
        client = APIClient(enforce_csrf_checks=True)
        token = client.get(reverse('accounts:csrf')).data['csrfToken']
        response = client.post(reverse('accounts:register'), {
            'username': 'newmember', 'email': 'new@example.com',
            'password': self.password, 'password_confirm': self.password,
        }, format='json', HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 201, response.data)
        user = User.objects.get(username='newmember')
        self.assertTrue(user.check_password(self.password))
        self.assertEqual(client.get(reverse('accounts:profile')).data['id'], user.pk)
        token = response.data['csrfToken']
        changed = client.post(reverse('accounts:change-password'), {
            'old_password': self.password,
            'new_password': 'Cloud!Mountain-9837',
            'new_password_confirm': 'Cloud!Mountain-9837',
        }, format='json', HTTP_X_CSRFTOKEN=token)
        self.assertEqual(changed.status_code, 200)
        self.assertEqual(client.get(reverse('accounts:profile')).status_code, 200)
        token = client.get(reverse('accounts:csrf')).data['csrfToken']
        self.assertEqual(client.post(reverse('accounts:logout'), {}, format='json',
                                     HTTP_X_CSRFTOKEN=token).status_code, 204)
        self.assertEqual(client.get(reverse('accounts:profile')).status_code, 403)
        token = client.get(reverse('accounts:csrf')).data['csrfToken']
        logged_in = client.post(reverse('accounts:login'), {
            'username': 'newmember', 'password': 'Cloud!Mountain-9837',
        }, format='json', HTTP_X_CSRFTOKEN=token)
        self.assertEqual(logged_in.status_code, 200)
