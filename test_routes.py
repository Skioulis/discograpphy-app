import unittest

import app as app_module
from app import create_app
from app.models.db import db
from app.models.Song import Song
from app.models.Disk import Disk
from app.models.Person import Person
from app.models.Company import Company
from app.models.DiskLabel import DiskLabel
from app.models.associations import PeopleSong


class RoutesTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app_module.dc.database_uri = 'sqlite:///:memory:'
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['WTF_CSRF_ENABLED'] = False
        cls.client = cls.app.test_client()

    def setUp(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()

            company = Company(name='Acme Records', labels_size=45, info='A label')
            disk = Disk(name='Greatest Hits', company=company, size=45, sakisid='SK-1', notes='mint')
            person = Person(name='John Doe', notes='singer')
            song = Song(title='Hello World', notes='a song', lyrics='la la la')
            song.disks.append(disk)
            label = DiskLabel(label='Side A', company=company)
            db.session.add_all([company, disk, person, song, label])
            db.session.flush()
            db.session.add(PeopleSong(person=person, song=song, isSinger=True))
            db.session.commit()

            self.company_id = company.company_id
            self.disk_id = disk.disk_id
            self.person_id = person.person_id
            self.song_id = song.song_id
            self.label_id = label.label_id

    # ---- listing pages ----
    def test_listing_pages_render(self):
        for path in ['/songs', '/disks', '/persons', '/companies', '/disk-labels']:
            self.assertEqual(self.client.get(path).status_code, 200, path)

    def test_listing_invalid_params_fall_back(self):
        r = self.client.get('/songs?sort=bogus&per_page=999')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Hello World', r.data)

    def test_pagination_clamps_out_of_range_page(self):
        # Only one person exists; page 99 should clamp and still show it.
        r = self.client.get('/persons?page=99')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'John Doe', r.data)

    # ---- search ----
    def test_search_empty_query(self):
        r = self.client.get('/search')
        self.assertEqual(r.status_code, 200)
        self.assertIn('για να ξεκινήσετε'.encode(), r.data)

    def test_search_everything_finds_across_types(self):
        r = self.client.get('/search?q=a&type=everything')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Acme Records', r.data)

    def test_search_invalid_type_falls_back_to_everything(self):
        r = self.client.get('/search?q=Acme&type=bogus')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Acme Records', r.data)

    def test_search_preview_caps_and_links(self):
        with self.app.app_context():
            for i in range(7):
                db.session.add(Person(name=f'Preview Person {i}'))
            db.session.commit()
        r = self.client.get('/search?q=Preview&type=everything')
        self.assertEqual(r.status_code, 200)
        self.assertIn('Όλα τα'.encode(), r.data)  # "view all" link, more than the preview cap

    def test_search_specific_type_paginates(self):
        with self.app.app_context():
            for i in range(15):
                db.session.add(Person(name=f'Page Person {i}'))
            db.session.commit()
        r = self.client.get('/search?q=Page&type=persons&per_page=10')
        self.assertEqual(r.status_code, 200)
        self.assertIn('Σελιδοποίηση αναζήτησης'.encode(), r.data)

    # ---- create ----
    def test_add_company(self):
        r = self.client.post('/add-company', data={'name': 'New Co', 'labels_size': 33, 'info': ''})
        self.assertEqual(r.status_code, 302)
        with self.app.app_context():
            self.assertIsNotNone(Company.query.filter_by(name='New Co').first())

    def test_add_disk_stores_integer_size(self):
        r = self.client.post('/add-disk', data={
            'name': 'New Disk', 'company_id': self.company_id,
            'labels_size': 78, 'sakisid': '', 'notes': ''})
        self.assertEqual(r.status_code, 302)
        with self.app.app_context():
            disk = Disk.query.filter_by(name='New Disk').first()
            self.assertEqual(disk.size, 78)
            self.assertIsInstance(disk.size, int)

    def test_add_person(self):
        r = self.client.post('/add-person', data={'name': 'Jane Roe', 'notes': ''})
        self.assertEqual(r.status_code, 302)
        with self.app.app_context():
            self.assertIsNotNone(Person.query.filter_by(name='Jane Roe').first())

    # ---- edit (save) ----
    def test_save_person_same_name_allowed(self):
        r = self.client.post(f'/persons/{self.person_id}/save',
                             data={'name': 'John Doe', 'notes': 'updated'})
        self.assertEqual(r.status_code, 302)
        with self.app.app_context():
            self.assertEqual(db.session.get(Person, self.person_id).notes, 'updated')

    def test_save_person_duplicate_name_rejected(self):
        with self.app.app_context():
            db.session.add(Person(name='Other Person'))
            db.session.commit()
        r = self.client.post(f'/persons/{self.person_id}/save',
                             data={'name': 'Other Person', 'notes': ''})
        self.assertEqual(r.status_code, 400)
        self.assertIn('Υπάρχει ήδη πρόσωπο'.encode(), r.data)

    def test_save_disk_updates_integer_size(self):
        r = self.client.post(f'/disks/{self.disk_id}/save', data={
            'name': 'Greatest Hits', 'company_id': self.company_id,
            'labels_size': 33, 'sakisid': 'SK-1', 'notes': ''})
        self.assertEqual(r.status_code, 302)
        with self.app.app_context():
            self.assertEqual(db.session.get(Disk, self.disk_id).size, 33)

    # ---- edit mode query param ----
    def test_edit_query_param_opens_edit_mode(self):
        r = self.client.get(f'/persons/{self.person_id}?edit=1')
        self.assertIn(b'edit-mode-toggle" checked', r.data)
        r2 = self.client.get(f'/persons/{self.person_id}')
        self.assertNotIn(b'edit-mode-toggle" checked', r2.data)

    # ---- delete + safe redirect ----
    def test_delete_person_with_local_next(self):
        with self.app.app_context():
            p = Person(name='Temp Del')
            db.session.add(p)
            db.session.commit()
            pid = p.person_id
        r = self.client.post(f'/persons/{pid}/delete', data={'next': '/persons?sort=name'})
        self.assertEqual(r.status_code, 302)
        self.assertTrue(r.headers['Location'].endswith('/persons?sort=name'))

    def test_delete_rejects_external_next(self):
        with self.app.app_context():
            p = Person(name='Temp Del 2')
            db.session.add(p)
            db.session.commit()
            pid = p.person_id
        r = self.client.post(f'/persons/{pid}/delete', data={'next': 'https://evil.com/x'})
        self.assertEqual(r.status_code, 302)
        self.assertTrue(r.headers['Location'].endswith('/'))

    def test_delete_company_blocked_when_has_dependents(self):
        r = self.client.post(f'/companies/{self.company_id}/delete', follow_redirects=True)
        self.assertIn(b'alert-warning', r.data)
        self.assertIn('Δεν είναι δυνατή η διαγραφή'.encode(), r.data)
        with self.app.app_context():
            self.assertIsNotNone(db.session.get(Company, self.company_id))

    def test_delete_empty_company_succeeds(self):
        with self.app.app_context():
            co = Company(name='Empty Co', labels_size=45)
            db.session.add(co)
            db.session.commit()
            cid = co.company_id
        r = self.client.post(f'/companies/{cid}/delete')
        self.assertEqual(r.status_code, 302)
        with self.app.app_context():
            self.assertIsNone(db.session.get(Company, cid))

    def test_delete_disk_clears_song_links(self):
        r = self.client.post(f'/disks/{self.disk_id}/delete')
        self.assertEqual(r.status_code, 302)
        with self.app.app_context():
            self.assertIsNone(db.session.get(Disk, self.disk_id))
            # the song remains, just unlinked
            self.assertIsNotNone(db.session.get(Song, self.song_id))

    # ---- flash category on success ----
    def test_success_flash_uses_success_category(self):
        r = self.client.post('/add-person', data={'name': 'Flash Person', 'notes': ''},
                             follow_redirects=True)
        self.assertIn(b'alert-success', r.data)

    # ---- search wildcard escaping ----
    def test_search_escapes_like_wildcards(self):
        with self.app.app_context():
            db.session.add_all([Person(name='100% Pure'), Person(name='1000 Songs')])
            db.session.commit()
        # '%' must be matched literally, so only '100% Pure' should appear.
        r = self.client.get('/search?q=100%25&type=persons')  # %25 = '%'
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'100% Pure', r.data)
        self.assertNotIn(b'1000 Songs', r.data)

    # ---- search across relationships ----
    def test_search_song_by_person_name(self):
        r = self.client.get('/search?q=John&type=songs')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Hello World', r.data)  # song matched via its person 'John Doe'

    def test_search_disk_by_company_name(self):
        r = self.client.get('/search?q=Acme&type=disks')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Greatest Hits', r.data)  # disk matched via company 'Acme Records'

    # ---- error pages ----
    def test_404_page(self):
        r = self.client.get('/songs/999999')
        self.assertEqual(r.status_code, 404)
        self.assertIn('Η σελίδα δεν βρέθηκε'.encode(), r.data)

    # ---- add_song with duplicate person names merges roles ----
    def test_add_song_merges_duplicate_person_rows(self):
        data = {
            'title': 'Dup People Song',
            'disk_name': '',
            'lyrics': 'words',
            'notes': '',
            'persons-0-person_name': 'Repeated Artist',
            'persons-0-isSinger': 'y',
            'persons-1-person_name': 'Repeated Artist',
            'persons-1-isComposer': 'y',
        }
        r = self.client.post('/add-song', data=data)
        self.assertEqual(r.status_code, 302)  # no IntegrityError
        with self.app.app_context():
            song = Song.query.filter_by(title='Dup People Song').first()
            self.assertEqual(len(song.people), 1)
            self.assertTrue(song.people[0].isSinger)
            self.assertTrue(song.people[0].isComposer)
            self.assertEqual(song.lyrics, 'words')

    # ---- unique constraints ----
    def test_person_name_unique_constraint(self):
        from sqlalchemy.exc import IntegrityError
        with self.app.app_context():
            db.session.add(Person(name='John Doe'))  # already exists from setUp
            with self.assertRaises(IntegrityError):
                db.session.commit()
            db.session.rollback()


class ConfigSelectionTests(unittest.TestCase):
    def test_get_config_by_name(self):
        from config import get_config, DevelopmentConfig, ProductionConfig
        self.assertIs(get_config('development'), DevelopmentConfig)
        self.assertIs(get_config('production'), ProductionConfig)

    def test_get_config_unknown_defaults_to_development(self):
        from config import get_config, DevelopmentConfig
        self.assertIs(get_config('nonsense'), DevelopmentConfig)

    def test_production_requires_non_default_secret_key(self):
        from unittest import mock
        from config import ProductionConfig, DEFAULT_SECRET_KEY
        with mock.patch.object(ProductionConfig, 'SECRET_KEY', DEFAULT_SECRET_KEY):
            with self.assertRaises(RuntimeError):
                ProductionConfig.validate()
        with mock.patch.object(ProductionConfig, 'SECRET_KEY', 'a-real-secret'):
            ProductionConfig.validate()  # should not raise


if __name__ == '__main__':
    unittest.main()
