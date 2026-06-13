"""Quick local test of the reworked models against a local SQLite DB.

Run with:  FLASK_ENV=development-local python test_models_sqlite.py
"""
import os

# Force the local-sqlite config before anything imports it.
os.environ['FLASK_ENV'] = 'development-local'

from flask import Flask
from config import DevelopmentConfig as dc
from app.models import db, Song, Lyric, Person, PersonSongRole


def create_test_app():
    # Minimal app so we exercise only the models (not routes/forms).
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = dc.database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


def main():
    app = create_test_app()
    with app.app_context():
        # Start from a clean schema.
        db.drop_all()
        db.create_all()

        # Create persons.
        lennon = Person(name='John Lennon', notes='Beatle')
        mccartney = Person(name='Paul McCartney')

        # Create a song with lyrics and person-role links.
        song = Song(
            title='A Day in the Life',
            notes='Closing track of Sgt. Pepper',
            lyrics=[
                Lyric(text='I read the news today, oh boy'),
                Lyric(text='Found my coat and grabbed my hat'),
            ],
            person_roles=[
                PersonSongRole(person=lennon, isComposer=True, isSongwriter=True, isSinger=True),
                PersonSongRole(person=mccartney, isComposer=True, isMusician=True),
            ],
        )

        db.session.add(song)
        db.session.commit()

        # Read it back.
        loaded = db.session.query(Song).filter_by(title='A Day in the Life').one()
        print('Song:', loaded)
        print('  created_at:', loaded.created_at)
        print('  updated_at:', loaded.updated_at)
        print('  lyrics:')
        for lyric in loaded.lyrics:
            print('    -', lyric.text)
        print('  people & roles:')
        for pr in loaded.person_roles:
            print(f'    - {pr.person.name}: {", ".join(pr.roles())}')

        # Check the back-reference from a person.
        paul = db.session.query(Person).filter_by(name='Paul McCartney').one()
        print('Paul appears on:',
              [(sr.song.title, sr.roles()) for sr in paul.song_roles])

        # Assertions.
        assert len(loaded.lyrics) == 2
        assert {pr.person.name for pr in loaded.person_roles} == {'John Lennon', 'Paul McCartney'}
        lennon_role = next(pr for pr in loaded.person_roles if pr.person.name == 'John Lennon')
        assert lennon_role.roles() == ['Composer', 'Songwriter', 'Singer']
        assert paul.song_roles[0].song.title == 'A Day in the Life'
        assert paul.song_roles[0].isMusician is True
        assert loaded.created_at is not None and loaded.updated_at is not None
        print('\nAll assertions passed.')


if __name__ == '__main__':
    main()
