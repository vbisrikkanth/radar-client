from radar.lib.auth.sessions import logout, logout_other_sessions
from radar.lib.views.core import ApiView


class LogoutView(ApiView):
    def post(self):
        logout()
        return '', 200


class LogoutOtherSessionsView(ApiView):
    def post(self):
        logout_other_sessions()
        return '', 200
