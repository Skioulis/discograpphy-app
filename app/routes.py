from flask import Blueprint, render_template, redirect, url_for, flash
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

@main_bp.route('/')
def home():

    songs = Song.query.limit(5).all()
    print(songs)

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
    # Populate disk choices
    disks = Disk.query.order_by(Disk.name).all()
    form.disk_id.choices = [(0, '-- None --')] + [(d.disk_id, d.name) for d in disks]

    all_persons = Person.query.order_by(Person.name).all()

    if form.validate_on_submit():
        new_song = Song(
            title=form.title.data,
            notes=form.notes.data
        )
        
        # Add lyrics if provided
        if form.lyrics.data:
            new_song.lyrics.append(Lyric(lyric=form.lyrics.data))
        
        # Link to disk if selected
        if form.disk_id.data and form.disk_id.data != 0:
            disk = Disk.query.get(form.disk_id.data)
            if disk:
                new_song.disks.append(disk)

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
    return render_template('add_pages/add_song.html', form=form, all_persons=all_persons)

