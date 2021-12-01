from AutoAnswer import AutoAnswer


def test_login():
    AutoAnswer().login(user_name="181451080414", password="minami373")


def test_question_bank():
    AutoAnswer.question_bank()


def test_match_answer():
    obj = AutoAnswer()
    obj.login(user_name="181451080414", password="minami373")
    obj.match_answer()


def test_auto():
    obj = AutoAnswer()
    obj.login(user_name="181451080438", password="328114zyc")
    obj.auto()


if __name__ == '__main__':
    # test_login()
    # test_question_bank()
    # test_match_answer()
    test_auto()
