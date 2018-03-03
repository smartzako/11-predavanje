#!/usr/bin/env python

import webapp2

from cron.izbris_cron import IzbrisObjavCron
from handlers.cookie_handler import CookieHandler
from handlers.main_handler import MainHandler
from handlers.objave_handler import DodajObjavoHandler, PreglejObjaveHandler, PreglejObjavoHandler, IzbrisObjaveHandler
from handlers.moji_komentarji_handler import MojiKomentarjiHandler
from handlers.objave_handler import StKomentarjevHandler
from workers.mail_worker import MailWorker

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieHandler),
    webapp2.Route('/dodaj-objavo', DodajObjavoHandler),
    webapp2.Route('/preglej-objave', PreglejObjaveHandler),
    webapp2.Route('/preglej-objavo/<objava_id:\d+>', PreglejObjavoHandler),
    webapp2.Route('/izbris-objave/<objava_id:\d+>', IzbrisObjaveHandler),
    webapp2.Route('/moji-komentarji', MojiKomentarjiHandler),
    webapp2.Route('/st-komentarjev/<objava_id:\d+>', StKomentarjevHandler),

    webapp2.Route('/task/send-comment-mail', MailWorker),
    webapp2.Route('/cron/izbris-objav', IzbrisObjavCron)
], debug=True)
