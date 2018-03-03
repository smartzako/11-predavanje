from datetime import datetime, timedelta


from handlers.base_handler import BaseHandler
from models.models import Objava


class IzbrisObjavCron(BaseHandler):
    def get(self):
        trenutni_cas = datetime.now()

        mejni_cas_izbrisa = trenutni_cas - timedelta(days=30)

        objave = Objava.query(Objava.cas_izbrisa != None,
                              Objava.cas_izbrisa < mejni_cas_izbrisa).fetch()
        for objava in objave:
            objava.key.delete()
