from google.appengine.api import users

from handlers.base_handler import BaseHandler
from models.models import Komentar


class MojiKomentarjiHandler(BaseHandler):
    def get(self):
        moj_email = users.get_current_user().email()

        moji_komentarji = Komentar.query(Komentar.uporabnik_email == moj_email).fetch()

        params = {
            "moji_komentarji": moji_komentarji
        }
        return self.render_template("moji_komentarji.html", params)