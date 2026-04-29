import unittest

import app as app_module
from app import create_app
from app.models.Company import Company
from app.models.Disk import Disk
from app.models.Song import Song
from app.models.db import db


class SongDiskNameFlowTests(unittest.TestCase):
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

            company = Company(name='Test Company', labels_size=45)
            disk = Disk(name='Disk One', company=company)
            db.session.add_all([company, disk])
            db.session.commit()

    @staticmethod
    def _song_payload(title, disk_name):
        return {
            'title': title,
            'disk_name': disk_name,
            'lyrics': '',
            'notes': '',
            'persons-0-person_name': ''
        }

    def test_add_song_links_existing_disk_from_name(self):
        response = self.client.post(
            '/add-song',
            data=self._song_payload('Song with Disk', 'Disk One'),
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 302)

        with self.app.app_context():
            song = Song.query.filter_by(title='Song with Disk').first()
            self.assertIsNotNone(song)
            self.assertEqual(len(song.disks), 1)
            self.assertEqual(song.disks[0].name, 'Disk One')

    def test_save_song_links_disk_by_case_insensitive_name(self):
        with self.app.app_context():
            song = Song(title='Editable Song')
            db.session.add(song)
            db.session.commit()
            song_id = song.song_id

        response = self.client.post(
            f'/songs/{song_id}/save',
            data=self._song_payload('Editable Song', 'disk one'),
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 302)

        with self.app.app_context():
            saved_song = Song.query.get(song_id)
            self.assertIsNotNone(saved_song)
            self.assertEqual(len(saved_song.disks), 1)
            self.assertEqual(saved_song.disks[0].name, 'Disk One')

    def test_save_song_rejects_unknown_disk_name(self):
        with self.app.app_context():
            song = Song(title='Song without disk')
            db.session.add(song)
            db.session.commit()
            song_id = song.song_id

        response = self.client.post(
            f'/songs/{song_id}/save',
            data=self._song_payload('Song without disk', 'Missing Disk'),
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Please select an available disk.', response.data)

        with self.app.app_context():
            unchanged_song = Song.query.get(song_id)
            self.assertIsNotNone(unchanged_song)
            self.assertEqual(len(unchanged_song.disks), 0)


if __name__ == '__main__':
    unittest.main()