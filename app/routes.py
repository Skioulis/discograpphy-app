from flask import Blueprint, render_template, redirect, url_for, flash
from sqlalchemy import func

from .models.Song import Song
from .models.Lyric import Lyric
from .models.associations import PeopleSong
from .models.db import db
from .forms.disk_form import DiskForm
from .models.Disk import Disk
from .models.Company import Company
from .forms.company_form import CompanyForm
from .models.DiskLabel import DiskLabel
from .forms.disk_label_form import DiskLabelForm
from .models.Person import Person
from .forms.person_form import PersonForm
from .forms.song_form import SongForm



main_bp = Blueprint('main', __name__)


def _load_song_with_details(song_id):
    return Song.query.options(
        db.joinedload(Song.people).joinedload(PeopleSong.person),
        db.joinedload(Song.lyrics),
        db.joinedload(Song.disks)
    ).filter(Song.song_id == song_id).first_or_404()


def _build_single_song_form(song):
    form = SongForm(obj=song)

    form.title.data = song.title
    form.notes.data = song.notes or ''
    form.lyrics.data = '\n\n'.join(lyric.lyric for lyric in song.lyrics)
    form.disk_name.data = song.disks[0].name if song.disks else ''

    while len(form.persons) > 0:
        form.persons.pop_entry()

    if song.people:
        for ps in song.people:
            person_form = form.persons.append_entry()
            person_form.form.person_name.data = ps.person.name
            person_form.form.isSinger.data = ps.isSinger
            person_form.form.isComposer.data = ps.isComposer
            person_form.form.isSongwriter.data = ps.isSongwriter
            person_form.form.isMusician.data = ps.isMusician
    else:
        form.persons.append_entry()

    return form

@main_bp.route('/')
def home():
    songs = Song.query.options(db.joinedload(Song.people).joinedload(PeopleSong.person)).order_by(func.random()).limit(9).all()
    # testsong = Song.query.options(db.joinedload(Song.people).joinedload(PeopleSong.person)).filter(
    #     Song.song_id == 2).first()
    # print(testsong)
    # for person in testsong.people:
    #
    #     print(person.person_id)

    return render_template('index.html', songs=songs)

@main_bp.route('/add-disk', methods=['GET', 'POST'])
def add_disk():
    form = DiskForm()
    # Populate company choices
    form.company_id.choices = [(c.company_id, f"{c.name} {c.labels_size}") for c in Company.query.order_by(Company.name).all()]

    if form.validate_on_submit():
        new_disk = Disk(
            name=form.name.data,
            company_id=form.company_id.data,
            size=form.labels_size.data,
            sakisid=form.sakisid.data,
            notes=form.notes.data
        )
        db.session.add(new_disk)
        db.session.commit()
        flash('Disk added successfully!')
        return redirect(url_for('main.home'))
    return render_template('add_pages/add_disk.html', form=form)

@main_bp.route('/add-company', methods=['GET', 'POST'])
def add_company():
    form = CompanyForm()
    if form.validate_on_submit():
        new_company = Company(
            name=form.name.data,
            labels_size=form.labels_size.data,
            info=form.info.data
        )
        db.session.add(new_company)
        db.session.commit()
        flash('Company added successfully!')
        return redirect(url_for('main.home'))
    return render_template('add_pages/add_company.html', form=form)

@main_bp.route('/add-disk-label', methods=['GET', 'POST'])
def add_disk_label():
    form = DiskLabelForm()
    # Populate company choices
    form.company_id.choices = [(c.company_id, f"{c.name} {c.labels_size}") for c in Company.query.order_by(Company.name).all()]
    
    if form.validate_on_submit():
        new_label = DiskLabel(
            label=form.label.data,
            company_id=form.company_id.data
        )
        db.session.add(new_label)
        db.session.commit()
        flash('Disk Label added successfully!')
        return redirect(url_for('main.home'))
    return render_template('add_pages/add_disk_label.html', form=form)


@main_bp.route('/add-person', methods=['GET', 'POST'])
def add_person():
    form = PersonForm()
    if form.validate_on_submit():
        new_person = Person(
            name=form.name.data,
            notes=form.notes.data
        )
        db.session.add(new_person)
        db.session.commit()
        flash('Person added successfully!')
        return redirect(url_for('main.home'))
    return render_template('add_pages/add_person.html', form=form)


@main_bp.route('/add-song', methods=['GET', 'POST'])
def add_song():
    form = SongForm()
    all_disks = Disk.query.order_by(Disk.name).all()

    all_persons = Person.query.order_by(Person.name).all()

    if form.validate_on_submit():
        disk_name = (form.disk_name.data or '').strip()
        selected_disk = None
        if disk_name:
            selected_disk = Disk.query.filter(func.lower(Disk.name) == disk_name.lower()).first()
            if not selected_disk:
                form.disk_name.errors.append('Please select an available disk.')
                return render_template('add_pages/add_song.html', form=form, all_persons=all_persons, all_disks=all_disks), 400

        new_song = Song(
            title=form.title.data,
            notes=form.notes.data
        )
        
        # Add lyrics if provided
        if form.lyrics.data:
            new_song.lyrics.append(Lyric(lyric=form.lyrics.data))
        
        # Link to disk if selected
        if selected_disk:
            new_song.disks.append(selected_disk)

        # Process persons
        for p_form in form.persons:
            name = p_form.person_name.data
            if name:
                person = Person.query.filter_by(name=name).first()
                if not person:
                    person = Person(name=name)
                    db.session.add(person)
                
                ps = PeopleSong(
                    person=person,
                    song=new_song,
                    isSinger=p_form.isSinger.data,
                    isComposer=p_form.isComposer.data,
                    isSongwriter=p_form.isSongwriter.data,
                    isMusician=p_form.isMusician.data
                )
                db.session.add(ps)

        db.session.add(new_song)
        db.session.commit()
        flash('Song added successfully!')
        return redirect(url_for('main.home'))
    return render_template('add_pages/add_song.html', form=form, all_persons=all_persons, all_disks=all_disks)


@main_bp.route('/songs/<int:song_id>')
def single_song(song_id):
    song = _load_song_with_details(song_id)
    form = _build_single_song_form(song)
    all_persons = Person.query.order_by(Person.name).all()
    all_disks = Disk.query.order_by(Disk.name).all()
    return render_template('single_pages/single_song.html', song=song, form=form, all_persons=all_persons, all_disks=all_disks, edit_mode=False)


@main_bp.route('/songs/<int:song_id>/save', methods=['POST'])
def save_song(song_id):
    song = _load_song_with_details(song_id)
    form = SongForm()
    all_disks = Disk.query.order_by(Disk.name).all()
    all_persons = Person.query.order_by(Person.name).all()

    if not form.validate_on_submit():
        return render_template('single_pages/single_song.html', song=song, form=form, all_persons=all_persons, all_disks=all_disks, edit_mode=True), 400

    disk_name = (form.disk_name.data or '').strip()
    selected_disk = None
    if disk_name:
        selected_disk = Disk.query.filter(func.lower(Disk.name) == disk_name.lower()).first()
        if not selected_disk:
            form.disk_name.errors.append('Please select an available disk.')
            return render_template('single_pages/single_song.html', song=song, form=form, all_persons=all_persons, all_disks=all_disks, edit_mode=True), 400

    song.title = form.title.data
    song.notes = form.notes.data

    song.disks.clear()
    if selected_disk:
        song.disks.append(selected_disk)

    song.lyrics.clear()
    if form.lyrics.data and form.lyrics.data.strip():
        song.lyrics.append(Lyric(lyric=form.lyrics.data.strip()))

    PeopleSong.query.filter_by(song_id=song.song_id).delete(synchronize_session=False)

    merged_people = {}
    for p_form in form.persons:
        person_name = (p_form.person_name.data or '').strip()
        if not person_name:
            continue

        person = Person.query.filter_by(name=person_name).first()
        if not person:
            person = Person(name=person_name)
            db.session.add(person)
            db.session.flush()

        person_roles = merged_people.get(person.person_id)
        if person_roles:
            person_roles['isSinger'] = person_roles['isSinger'] or bool(p_form.isSinger.data)
            person_roles['isComposer'] = person_roles['isComposer'] or bool(p_form.isComposer.data)
            person_roles['isSongwriter'] = person_roles['isSongwriter'] or bool(p_form.isSongwriter.data)
            person_roles['isMusician'] = person_roles['isMusician'] or bool(p_form.isMusician.data)
        else:
            merged_people[person.person_id] = {
                'isSinger': bool(p_form.isSinger.data),
                'isComposer': bool(p_form.isComposer.data),
                'isSongwriter': bool(p_form.isSongwriter.data),
                'isMusician': bool(p_form.isMusician.data)
            }

    for person_id, roles in merged_people.items():
        db.session.add(PeopleSong(
            person_id=person_id,
            song_id=song.song_id,
            isSinger=roles['isSinger'],
            isComposer=roles['isComposer'],
            isSongwriter=roles['isSongwriter'],
            isMusician=roles['isMusician']
        ))

    db.session.commit()
    flash('Song updated successfully!')
    return redirect(url_for('main.single_song', song_id=song.song_id))


@main_bp.route('/songs/<int:song_id>/delete', methods=['POST'])
def delete_song(song_id):
    song = Song.query.get_or_404(song_id)

    PeopleSong.query.filter_by(song_id=song.song_id).delete(synchronize_session=False)
    song.disks.clear()
    db.session.delete(song)
    db.session.commit()

    flash('Song deleted successfully!')
    return redirect(url_for('main.home'))

