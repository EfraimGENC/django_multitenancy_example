from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
User = get_user_model()


class UserAdminCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = '__all__'


class UserAdminChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = '__all__'
