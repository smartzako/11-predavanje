import os
import unittest
import uuid

import webtest
from google.appengine.api import memcache

from google.appengine.ext import testbed

from main import app
from models.models import Objava


class MainPageTests(unittest.TestCase):
    def setUp(self):
        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        """ Uncomment the stubs that you need to run tests. """
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # self.testbed.init_mail_stub()
        # self.testbed.init_taskqueue_stub()
        self.testbed.init_user_stub()
        # ...

        """ Uncomment if you need user (Google Login) and if this user needs to be admin. """
        os.environ['USER_EMAIL'] = 'some.user@example.com'
        # os.environ['USER_IS_ADMIN'] = '1'

    def tearDown(self):
        self.testbed.deactivate()

    def test_main_page_handler(self):
        get = self.testapp.get('/')  # get main handler
        self.assertEqual(get.status_int, 200)  # if GET request was ok, it should return 200 status code

    def test_moji_komentarji(self):
        get = self.testapp.get('/moji-komentarji')
        self.assertEqual(get.status_int, 200)

    def test_neobstojeca_objava(self):
        # Objava s tem id-jem ne obstaja.
        get = self.testapp.get('/preglej-objavo/123')
        self.assertEqual(get.body, 'Te objave ni.')

    def test_dodaj_objavo(self):
        # Preverimo ali GET zahteva na /dodaj-objavo deluje.
        get = self.testapp.get('/dodaj-objavo')  # do a GET request
        self.assertEqual(get.status_int, 200)

        # Preverimo ali POST zahteva na /dodaj-objavo deluje.
        # Najprej moramo v memcache bazo dodati CSRF zeton.
        # Pozor: To je samo testna memcache baza, namenjena izkljucno za
        #        test test_dodaj_objavo! Na zacetku je torej prazna.
        csrf_zeton = str(uuid.uuid4())
        memcache.add(key=csrf_zeton, value=True, time=20)

        naslov = "Nova objava"
        vsebina = "To je nova objava"

        params = {"title": naslov, "text": vsebina, "csrf-zeton": csrf_zeton}

        # Sedaj naredimo post zahtevo. Ce je vse prav, bi se morala v bazo
        # dodati nova objava. Spet pozor: gre se za testno bazo, ki obstaja
        # le za test test_dodaj_objavo. Na zacetku je torej prazna.
        post = self.testapp.post('/dodaj-objavo', params)  # do a POST request
        self.assertEqual(post.status_int, 200)

        # Iz te testne baze sedaj preberemo objavo in preverimo, da so se podatki
        # pravilno zapisali.
        objava = Objava.query().get()  # Ker imamo sedaj v bazi le eno objavo, lahko naredimo get().
        self.assertEqual(objava.naslov, naslov)
        self.assertEqual(objava.vsebina, vsebina)
