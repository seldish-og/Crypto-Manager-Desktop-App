from UserModel import User


class RegistrationUserModel(User):
    def __init__(self, user_password: str, user_login: str, user_email: str) -> None:
        super().__init__(user_password, user_login)
        self.user_email = user_email
