from apps.member.forms import SignupForm


def create_user(email="tin@domain.com", password="123", nickname="tin", activate=True):
    signup_form = SignupForm(
        {
            "email": email,
            "password1": password,
            "nickname": nickname,
            "password2": password,
        }
    )
    member = signup_form.save()
    if activate:
        member.user.is_active = True
        member.user.save()
    return member
