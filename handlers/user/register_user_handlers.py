from handlers.user import start, questions, photos


def register_user_handler(dp):
    start.register_start_handler(dp)
    questions.register_handler(dp)
    photos.register_handler(dp)
