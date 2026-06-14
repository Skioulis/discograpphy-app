from urllib.parse import urlparse

from flask import Blueprint, render_template, redirect, url_for, flash, request
from sqlalchemy import func, or_

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


def _safe_redirect(default_endpoint):
    """Redirect to the posted 'next' target if it is a local path, else fall back."""
    target = request.form.get('next')
    if target:
        parsed = urlparse(target)
        if not parsed.netloc and not parsed.scheme and target.startswith('/'):
            return redirect(target)
    return redirect(url_for(default_endpoint))


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

SONG_SORT_OPTIONS = {
    'updated': ('Recently updated', lambda: Song.updated_at.desc()),
    'name': ('Name (A–Z)', lambda: Song.title.asc()),
    'oldest_updated': ('Least recently updated', lambda: Song.updated_at.asc()),
}
PER_PAGE_CHOICES = [10, 20, 50, 100]


@main_bp.route('/songs')
def songs_list():
    sort = request.args.get('sort', 'updated')
    if sort not in SONG_SORT_OPTIONS:
        sort = 'updated'

    try:
        per_page = int(request.args.get('per_page', 10))
    except (TypeError, ValueError):
        per_page = 10
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    page = request.args.get('page', 1, type=int)

    pagination = Song.query.options(
        db.selectinload(Song.people).joinedload(PeopleSong.person)
    ).order_by(SONG_SORT_OPTIONS[sort][1]()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template(
        'songs_list.html',
        pagination=pagination,
        songs=pagination.items,
        sort=sort,
        per_page=per_page,
        sort_options=SONG_SORT_OPTIONS,
        per_page_choices=PER_PAGE_CHOICES,
    )


DISK_SORT_OPTIONS = {
    'updated': ('Recently updated', lambda: Disk.updated_at.desc()),
    'name': ('Name (A–Z)', lambda: Disk.name.asc()),
    'oldest_updated': ('Least recently updated', lambda: Disk.updated_at.asc()),
}


@main_bp.route('/disks')
def disks_list():
    sort = request.args.get('sort', 'updated')
    if sort not in DISK_SORT_OPTIONS:
        sort = 'updated'

    try:
        per_page = int(request.args.get('per_page', 10))
    except (TypeError, ValueError):
        per_page = 10
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    page = request.args.get('page', 1, type=int)

    pagination = Disk.query.options(
        db.joinedload(Disk.company)
    ).order_by(DISK_SORT_OPTIONS[sort][1]()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template(
        'disks_list.html',
        pagination=pagination,
        disks=pagination.items,
        sort=sort,
        per_page=per_page,
        sort_options=DISK_SORT_OPTIONS,
        per_page_choices=PER_PAGE_CHOICES,
    )


PERSON_SORT_OPTIONS = {
    'updated': ('Recently updated', lambda: Person.updated_at.desc()),
    'name': ('Name (A–Z)', lambda: Person.name.asc()),
    'oldest_updated': ('Least recently updated', lambda: Person.updated_at.asc()),
}


@main_bp.route('/persons')
def persons_list():
    sort = request.args.get('sort', 'updated')
    if sort not in PERSON_SORT_OPTIONS:
        sort = 'updated'

    try:
        per_page = int(request.args.get('per_page', 10))
    except (TypeError, ValueError):
        per_page = 10
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    page = request.args.get('page', 1, type=int)

    pagination = Person.query.order_by(PERSON_SORT_OPTIONS[sort][1]()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template(
        'persons_list.html',
        pagination=pagination,
        persons=pagination.items,
        sort=sort,
        per_page=per_page,
        sort_options=PERSON_SORT_OPTIONS,
        per_page_choices=PER_PAGE_CHOICES,
    )


COMPANY_SORT_OPTIONS = {
    'updated': ('Recently updated', lambda: Company.updated_at.desc()),
    'name': ('Name (A–Z)', lambda: Company.name.asc()),
    'oldest_updated': ('Least recently updated', lambda: Company.updated_at.asc()),
}


@main_bp.route('/companies')
def companies_list():
    sort = request.args.get('sort', 'updated')
    if sort not in COMPANY_SORT_OPTIONS:
        sort = 'updated'

    try:
        per_page = int(request.args.get('per_page', 10))
    except (TypeError, ValueError):
        per_page = 10
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    page = request.args.get('page', 1, type=int)

    pagination = Company.query.order_by(COMPANY_SORT_OPTIONS[sort][1]()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template(
        'companies_list.html',
        pagination=pagination,
        companies=pagination.items,
        sort=sort,
        per_page=per_page,
        sort_options=COMPANY_SORT_OPTIONS,
        per_page_choices=PER_PAGE_CHOICES,
    )


DISK_LABEL_SORT_OPTIONS = {
    'updated': ('Recently updated', lambda: DiskLabel.updated_at.desc()),
    'name': ('Name (A–Z)', lambda: DiskLabel.label.asc()),
    'oldest_updated': ('Least recently updated', lambda: DiskLabel.updated_at.asc()),
}


@main_bp.route('/disk-labels')
def disk_labels_list():
    sort = request.args.get('sort', 'updated')
    if sort not in DISK_LABEL_SORT_OPTIONS:
        sort = 'updated'

    try:
        per_page = int(request.args.get('per_page', 10))
    except (TypeError, ValueError):
        per_page = 10
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    page = request.args.get('page', 1, type=int)

    pagination = DiskLabel.query.options(
        db.joinedload(DiskLabel.company)
    ).order_by(DISK_LABEL_SORT_OPTIONS[sort][1]()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template(
        'disk_labels_list.html',
        pagination=pagination,
        labels=pagination.items,
        sort=sort,
        per_page=per_page,
        sort_options=DISK_LABEL_SORT_OPTIONS,
        per_page_choices=PER_PAGE_CHOICES,
    )


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
    edit_mode = request.args.get('edit') == '1'
    return render_template('single_pages/single_song.html', song=song, form=form, all_persons=all_persons, all_disks=all_disks, edit_mode=edit_mode)


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
    return _safe_redirect('main.home')


def _company_choices():
    return [(c.company_id, f"{c.name} {c.labels_size}") for c in Company.query.order_by(Company.name).all()]


def _load_disk(disk_id):
    return Disk.query.options(
        db.joinedload(Disk.company),
        db.joinedload(Disk.songs)
    ).filter(Disk.disk_id == disk_id).first_or_404()


@main_bp.route('/disks/<int:disk_id>')
def single_disk(disk_id):
    disk = _load_disk(disk_id)
    form = DiskForm(obj=disk)
    form.company_id.choices = _company_choices()
    form.company_id.data = disk.company_id
    form.labels_size.data = int(disk.size) if disk.size and disk.size.isdigit() else 45
    edit_mode = request.args.get('edit') == '1'
    return render_template('single_pages/single_disk.html', disk=disk, form=form, edit_mode=edit_mode)


@main_bp.route('/disks/<int:disk_id>/save', methods=['POST'])
def save_disk(disk_id):
    disk = _load_disk(disk_id)
    form = DiskForm()
    form.editing_id = disk.disk_id
    form.company_id.choices = _company_choices()

    if not form.validate_on_submit():
        return render_template('single_pages/single_disk.html', disk=disk, form=form, edit_mode=True), 400

    disk.name = form.name.data
    disk.company_id = form.company_id.data
    disk.size = str(form.labels_size.data) if form.labels_size.data else None
    disk.sakisid = form.sakisid.data
    disk.notes = form.notes.data
    db.session.commit()
    flash('Disk updated successfully!')
    return redirect(url_for('main.single_disk', disk_id=disk.disk_id))


@main_bp.route('/disks/<int:disk_id>/delete', methods=['POST'])
def delete_disk(disk_id):
    disk = Disk.query.get_or_404(disk_id)
    disk.songs.clear()
    db.session.delete(disk)
    db.session.commit()
    flash('Disk deleted successfully!')
    return _safe_redirect('main.home')


def _load_person(person_id):
    return Person.query.options(
        db.joinedload(Person.songs).joinedload(PeopleSong.song)
    ).filter(Person.person_id == person_id).first_or_404()


@main_bp.route('/persons/<int:person_id>')
def single_person(person_id):
    person = _load_person(person_id)
    form = PersonForm(obj=person)
    edit_mode = request.args.get('edit') == '1'
    return render_template('single_pages/single_person.html', person=person, form=form, edit_mode=edit_mode)


@main_bp.route('/persons/<int:person_id>/save', methods=['POST'])
def save_person(person_id):
    person = _load_person(person_id)
    form = PersonForm()
    form.editing_id = person.person_id

    if not form.validate_on_submit():
        return render_template('single_pages/single_person.html', person=person, form=form, edit_mode=True), 400

    person.name = form.name.data
    person.notes = form.notes.data
    db.session.commit()
    flash('Person updated successfully!')
    return redirect(url_for('main.single_person', person_id=person.person_id))


@main_bp.route('/persons/<int:person_id>/delete', methods=['POST'])
def delete_person(person_id):
    person = Person.query.get_or_404(person_id)
    PeopleSong.query.filter_by(person_id=person.person_id).delete(synchronize_session=False)
    db.session.delete(person)
    db.session.commit()
    flash('Person deleted successfully!')
    return _safe_redirect('main.home')


def _load_company(company_id):
    return Company.query.options(
        db.joinedload(Company.disks),
        db.joinedload(Company.labels)
    ).filter(Company.company_id == company_id).first_or_404()


@main_bp.route('/companies/<int:company_id>')
def single_company(company_id):
    company = _load_company(company_id)
    form = CompanyForm(obj=company)
    form.labels_size.data = company.labels_size
    edit_mode = request.args.get('edit') == '1'
    return render_template('single_pages/single_company.html', company=company, form=form, edit_mode=edit_mode)


@main_bp.route('/companies/<int:company_id>/save', methods=['POST'])
def save_company(company_id):
    company = _load_company(company_id)
    form = CompanyForm()
    form.editing_id = company.company_id

    if not form.validate_on_submit():
        return render_template('single_pages/single_company.html', company=company, form=form, edit_mode=True), 400

    company.name = form.name.data
    company.labels_size = form.labels_size.data
    company.info = form.info.data
    db.session.commit()
    flash('Company updated successfully!')
    return redirect(url_for('main.single_company', company_id=company.company_id))


@main_bp.route('/companies/<int:company_id>/delete', methods=['POST'])
def delete_company(company_id):
    company = _load_company(company_id)
    if company.disks or company.labels:
        flash('Cannot delete a company that still has disks or labels linked to it.')
        return redirect(url_for('main.single_company', company_id=company.company_id))

    db.session.delete(company)
    db.session.commit()
    flash('Company deleted successfully!')
    return _safe_redirect('main.home')


def _load_disk_label(label_id):
    return DiskLabel.query.options(
        db.joinedload(DiskLabel.company)
    ).filter(DiskLabel.label_id == label_id).first_or_404()


@main_bp.route('/disk-labels/<int:label_id>')
def single_disk_label(label_id):
    label = _load_disk_label(label_id)
    form = DiskLabelForm(obj=label)
    form.company_id.choices = _company_choices()
    form.company_id.data = label.company_id
    edit_mode = request.args.get('edit') == '1'
    return render_template('single_pages/single_disk_label.html', label=label, form=form, edit_mode=edit_mode)


@main_bp.route('/disk-labels/<int:label_id>/save', methods=['POST'])
def save_disk_label(label_id):
    label = _load_disk_label(label_id)
    form = DiskLabelForm()
    form.company_id.choices = _company_choices()

    if not form.validate_on_submit():
        return render_template('single_pages/single_disk_label.html', label=label, form=form, edit_mode=True), 400

    label.label = form.label.data
    label.company_id = form.company_id.data
    db.session.commit()
    flash('Disk Label updated successfully!')
    return redirect(url_for('main.single_disk_label', label_id=label.label_id))


@main_bp.route('/disk-labels/<int:label_id>/delete', methods=['POST'])
def delete_disk_label(label_id):
    label = DiskLabel.query.get_or_404(label_id)
    db.session.delete(label)
    db.session.commit()
    flash('Disk Label deleted successfully!')
    return _safe_redirect('main.home')


# Search categories: maps the dropdown value to a human label. 'everything'
# searches all of them.
SEARCH_CATEGORIES = ['songs', 'disks', 'persons', 'companies', 'disk_labels']


def _search_songs(term):
    return Song.query.filter(
        or_(Song.title.ilike(term), Song.notes.ilike(term))
    ).order_by(Song.title).all()


def _search_disks(term):
    return Disk.query.filter(
        or_(Disk.name.ilike(term), Disk.notes.ilike(term), Disk.sakisid.ilike(term))
    ).order_by(Disk.name).all()


def _search_persons(term):
    return Person.query.filter(
        or_(Person.name.ilike(term), Person.notes.ilike(term))
    ).order_by(Person.name).all()


def _search_companies(term):
    return Company.query.filter(
        or_(Company.name.ilike(term), Company.info.ilike(term))
    ).order_by(Company.name).all()


def _search_disk_labels(term):
    return DiskLabel.query.filter(DiskLabel.label.ilike(term)).order_by(DiskLabel.label).all()


_SEARCHERS = {
    'songs': _search_songs,
    'disks': _search_disks,
    'persons': _search_persons,
    'companies': _search_companies,
    'disk_labels': _search_disk_labels,
}


@main_bp.route('/search')
def search():
    query = (request.args.get('q') or '').strip()
    search_type = request.args.get('type', 'everything')
    if search_type not in _SEARCHERS:
        search_type = 'everything'

    results = {}
    total = 0
    if query:
        term = f'%{query}%'
        categories = SEARCH_CATEGORIES if search_type == 'everything' else [search_type]
        for category in categories:
            found = _SEARCHERS[category](term)
            results[category] = found
            total += len(found)

    return render_template(
        'search_results.html',
        query=query,
        search_type=search_type,
        results=results,
        total=total,
    )

