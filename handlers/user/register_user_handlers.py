from handlers.user import start, questions, photos, skip_photo,generate


def register_user_handler(dp):
    start.register_start_handler(dp)
    questions.register_handler(dp)
    photos.register_handler(dp)
    generate.register_handler(dp)
    skip_photo.register_handler(dp)
