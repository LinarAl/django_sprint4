from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Кастомная форма для создания пользователя.
    Наследуется от стандартной формы, изменяет модель пользователя на
    кастомную.
    """

    class Meta(UserCreationForm.Meta):
        model = User
