import endpoints


def checkAuth():
    current_user = endpoints.get_current_user()
    if current_user is None:
        raise endpoints.NotFoundException('User is not authorised')
