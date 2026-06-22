import unicodedata
from urllib.parse import urlparse

from flask import Blueprint, render_template, redirect, url_for, flash, request
from sqlalchemy import func, or_

from .models.Song import Song
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
        db.joinedload(Song.disks)
    ).filter(Song.song_id == song_id).first_or_404()


def _build_single_song_form(song):
    form = SongForm(obj=song)

    form.title.data = song.title
    form.notes.data = song.notes or ''
    form.lyrics.data = song.lyrics or ''
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


def _merge_song_people(persons_field):
    """Resolve the submitted person rows into {person: roles}, creating missing
    people and OR-ing roles for repeated names (PeopleSong PK is person+song, so
    duplicates would otherwise raise an IntegrityError)."""
    merged = {}
    for p_form in persons_field:
        name = (p_form.person_name.data or '').strip()
        if not name:
            continue

        person = Person.query.filter_by(name=name).first()
        if not person:
            person = Person(name=name)
            db.session.add(person)
            db.session.flush()

        roles = merged.setdefault(person, {
            'isSinger': False, 'isComposer': False,
            'isSongwriter': False, 'isMusician': False,
        })
        roles['isSinger'] = roles['isSinger'] or bool(p_form.isSinger.data)
        roles['isComposer'] = roles['isComposer'] or bool(p_form.isComposer.data)
        roles['isSongwriter'] = roles['isSongwriter'] or bool(p_form.isSongwriter.data)
        roles['isMusician'] = roles['isMusician'] or bool(p_form.isMusician.data)

    return merged

@main_bp.route('/')
def home():
    songs = Song.query.options(db.joinedload(Song.people).joinedload(PeopleSong.person)).order_by(func.random()).limit(10).all()
    # testsong = Song.query.options(db.joinedload(Song.people).joinedload(PeopleSong.person)).filter(
    #     Song.song_id == 2).first()
    # print(testsong)
    # for person in testsong.people:
    #
    #     print(person.person_id)

    return render_template('index.html', songs=songs)

PER_PAGE_CHOICES = [10, 20, 50, 100]

# Each option maps a sort key to (label, column). The asc/desc direction is
# chosen separately via the `dir` query arg, so every field can be sorted both
# ways.
SORT_DIRECTIONS = {'asc', 'desc'}
DEFAULT_DIRECTION = 'desc'

SONG_SORT_OPTIONS = {
    'updated': ('Τελευταία ενημέρωση', lambda: Song.updated_at),
    'name': ('Τίτλος', lambda: Song.title),
}
DISK_SORT_OPTIONS = {
    'updated': ('Τελευταία ενημέρωση', lambda: Disk.updated_at),
    'name': ('Όνομα', lambda: Disk.name),
}
PERSON_SORT_OPTIONS = {
    'updated': ('Τελευταία ενημέρωση', lambda: Person.updated_at),
    'name': ('Όνομα', lambda: Person.name),
}
COMPANY_SORT_OPTIONS = {
    'updated': ('Τελευταία ενημέρωση', lambda: Company.updated_at),
    'name': ('Όνομα', lambda: Company.name),
}
DISK_LABEL_SORT_OPTIONS = {
    'updated': ('Τελευταία ενημέρωση', lambda: DiskLabel.updated_at),
    'name': ('Όνομα', lambda: DiskLabel.label),
}


def _resolve_per_page():
    try:
        per_page = int(request.args.get('per_page', 10))
    except (TypeError, ValueError):
        per_page = 10
    return per_page if per_page in PER_PAGE_CHOICES else 10


# ---------------------------------------------------------------------------
# Greek alphabet filter
# The catalogue lists can be filtered to entries whose title/name starts with
# a given Greek letter. Accents and dialytika fold onto the base letter
# (Άνοιξε → Α), and a '#' bucket catches everything that doesn't start with a
# Greek letter (Latin titles, digits, punctuation).
# ---------------------------------------------------------------------------
GREEK_LETTERS = ['Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ', 'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ',
                 'Ν', 'Ξ', 'Ο', 'Π', 'Ρ', 'Σ', 'Τ', 'Υ', 'Φ', 'Χ', 'Ψ', 'Ω']

# Accented / dialytika capital variants that fold onto each base letter. Used
# to build prefix matches; ILIKE makes the match case-insensitive so the
# lowercase forms (ά, ϊ, …) are covered too.
_GREEK_VARIANTS = {
    'Α': ['Α', 'Ά'],
    'Ε': ['Ε', 'Έ'],
    'Η': ['Η', 'Ή'],
    'Ι': ['Ι', 'Ί', 'Ϊ'],
    'Ο': ['Ο', 'Ό'],
    'Υ': ['Υ', 'Ύ', 'Ϋ'],
    'Ω': ['Ω', 'Ώ'],
}

# Latin alphabet, offered as an optional second filter row on listings (e.g.
# companies) that hold many Latin-named entries. Opt in per listing via
# latin=True; when off, Latin names fold to the '#' bucket exactly as before.
LATIN_LETTERS = [chr(c) for c in range(ord('A'), ord('Z') + 1)]


def _letter_variants(letter):
    return _GREEK_VARIANTS.get(letter, [letter])


def _fold_first_letter(text, latin=False):
    """Fold the first character of a title/name to a base Greek capital, a base
    Latin capital (only when latin=True), or '#' otherwise."""
    if not text:
        return '#'
    ch = text.strip()[:1].upper()
    if not ch:
        return '#'
    base = unicodedata.normalize('NFD', ch)[0]
    if base in GREEK_LETTERS:
        return base
    if latin and base in LATIN_LETTERS:
        return base
    return '#'


def _resolve_letter(latin=False):
    """Validate the requested ?letter= against the known buckets."""
    letter = request.args.get('letter')
    if letter in GREEK_LETTERS or letter == '#':
        return letter
    if latin and letter in LATIN_LETTERS:
        return letter
    return None


def _available_letters(column, latin=False):
    """Set of buckets (Greek letters, optionally Latin letters, and/or '#') that
    actually have entries, so the UI can dim letters that lead nowhere."""
    rows = db.session.query(func.substr(column, 1, 1)).distinct().all()
    return {_fold_first_letter(ch, latin=latin) for (ch,) in rows}


def _apply_letter_filter(query, column, letter, latin=False):
    if not letter:
        return query
    if letter == '#':
        bases = GREEK_LETTERS + (LATIN_LETTERS if latin else [])
        prefixes = [p for base in bases for p in _letter_variants(base)]
        conditions = [column.ilike(f'{p}%') for p in prefixes]
        return query.filter(column.isnot(None), ~or_(*conditions))
    conditions = [column.ilike(f'{p}%') for p in _letter_variants(letter)]
    return query.filter(or_(*conditions))


def _paginate(query, sort_options):
    """Apply the requested sort + direction + pagination from query args."""
    sort = request.args.get('sort', 'updated')
    if sort not in sort_options:
        sort = 'updated'
    direction = request.args.get('dir', DEFAULT_DIRECTION)
    if direction not in SORT_DIRECTIONS:
        direction = DEFAULT_DIRECTION
    per_page = _resolve_per_page()
    page = request.args.get('page', 1, type=int)
    column = sort_options[sort][1]()
    ordered = query.order_by(column.asc() if direction == 'asc' else column.desc())
    pagination = ordered.paginate(page=page, per_page=per_page, error_out=False)
    # Clamp past-the-end requests (e.g. after deleting the last item on a page)
    # to the last valid page so the user never lands on an empty page.
    if pagination.pages and page > pagination.pages:
        pagination = ordered.paginate(page=pagination.pages, per_page=per_page, error_out=False)
    return pagination, sort, direction, per_page


@main_bp.route('/songs')
def songs_list():
    query = Song.query.options(db.selectinload(Song.people).joinedload(PeopleSong.person))
    letter = _resolve_letter()
    available_letters = _available_letters(Song.title)
    query = _apply_letter_filter(query, Song.title, letter)
    pagination, sort, direction, per_page = _paginate(query, SONG_SORT_OPTIONS)
    return render_template(
        'songs_list.html', pagination=pagination, songs=pagination.items,
        sort=sort, direction=direction, per_page=per_page, sort_options=SONG_SORT_OPTIONS,
        per_page_choices=PER_PAGE_CHOICES,
        letter=letter, greek_letters=GREEK_LETTERS, available_letters=available_letters,
    )


@main_bp.route('/disks')
def disks_list():
    query = Disk.query.options(db.joinedload(Disk.company))
    letter = _resolve_letter()
    available_letters = _available_letters(Disk.name)
    query = _apply_letter_filter(query, Disk.name, letter)
    pagination, sort, direction, per_page = _paginate(query, DISK_SORT_OPTIONS)
    return render_template(
        'disks_list.html', pagination=pagination, disks=pagination.items,
        sort=sort, direction=direction, per_page=per_page, sort_options=DISK_SORT_OPTIONS,
        per_page_choices=PER_PAGE_CHOICES,
        letter=letter, greek_letters=GREEK_LETTERS, available_letters=available_letters,
    )


@main_bp.route('/persons')
def persons_list():
    letter = _resolve_letter()
    available_letters = _available_letters(Person.name)
    query = _apply_letter_filter(Person.query, Person.name, letter)
    pagination, sort, direction, per_page = _paginate(query, PERSON_SORT_OPTIONS)
    return render_template(
        'persons_list.html', pagination=pagination, persons=pagination.items,
        sort=sort, direction=direction, per_page=per_page, sort_options=PERSON_SORT_OPTIONS,
        per_page_choices=PER_PAGE_CHOICES,
        letter=letter, greek_letters=GREEK_LETTERS, available_letters=available_letters,
    )


@main_bp.route('/companies')
def companies_list():
    letter = _resolve_letter(latin=True)
    available_letters = _available_letters(Company.name, latin=True)
    query = _apply_letter_filter(Company.query, Company.name, letter, latin=True)
    pagination, sort, direction, per_page = _paginate(query, COMPANY_SORT_OPTIONS)
    return render_template(
        'companies_list.html', pagination=pagination, companies=pagination.items,
        sort=sort, direction=direction, per_page=per_page, sort_options=COMPANY_SORT_OPTIONS,
        per_page_choices=PER_PAGE_CHOICES,
        letter=letter, greek_letters=GREEK_LETTERS, latin_letters=LATIN_LETTERS,
        available_letters=available_letters,
    )


@main_bp.route('/disk-labels')
def disk_labels_list():
    query = DiskLabel.query.options(db.joinedload(DiskLabel.company))
    letter = _resolve_letter()
    available_letters = _available_letters(DiskLabel.label)
    query = _apply_letter_filter(query, DiskLabel.label, letter)
    pagination, sort, direction, per_page = _paginate(query, DISK_LABEL_SORT_OPTIONS)
    return render_template(
        'disk_labels_list.html', pagination=pagination, labels=pagination.items,
        sort=sort, direction=direction, per_page=per_page, sort_options=DISK_LABEL_SORT_OPTIONS,
        per_page_choices=PER_PAGE_CHOICES,
        letter=letter, greek_letters=GREEK_LETTERS, available_letters=available_letters,
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
        flash('Ο δίσκος προστέθηκε με επιτυχία!', 'success')
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
        flash('Η εταιρεία προστέθηκε με επιτυχία!', 'success')
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
        flash('Η ετικέτα προστέθηκε με επιτυχία!', 'success')
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
        flash('Ο καλλιτέχνης προστέθηκε με επιτυχία!', 'success')
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
            notes=form.notes.data,
            lyrics=(form.lyrics.data.strip() or None) if form.lyrics.data else None,
        )

        # Link to disk if selected
        if selected_disk:
            new_song.disks.append(selected_disk)

        # Process persons (merging duplicate names)
        for person, roles in _merge_song_people(form.persons).items():
            db.session.add(PeopleSong(person=person, song=new_song, **roles))

        db.session.add(new_song)
        db.session.commit()
        flash('Το τραγούδι προστέθηκε με επιτυχία!', 'success')
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

    song.lyrics = form.lyrics.data.strip() if form.lyrics.data and form.lyrics.data.strip() else None

    PeopleSong.query.filter_by(song_id=song.song_id).delete(synchronize_session=False)

    for person, roles in _merge_song_people(form.persons).items():
        db.session.add(PeopleSong(person=person, song=song, **roles))

    db.session.commit()
    flash('Το τραγούδι ενημερώθηκε με επιτυχία!', 'success')
    return redirect(url_for('main.single_song', song_id=song.song_id))


@main_bp.route('/songs/<int:song_id>/delete', methods=['POST'])
def delete_song(song_id):
    song = Song.query.get_or_404(song_id)

    PeopleSong.query.filter_by(song_id=song.song_id).delete(synchronize_session=False)
    song.disks.clear()
    db.session.delete(song)
    db.session.commit()

    flash('Το τραγούδι διαγράφηκε με επιτυχία!', 'success')
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
    form.labels_size.data = disk.size if disk.size else 45
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
    disk.size = form.labels_size.data or None
    disk.sakisid = form.sakisid.data
    disk.notes = form.notes.data
    db.session.commit()
    flash('Ο δίσκος ενημερώθηκε με επιτυχία!', 'success')
    return redirect(url_for('main.single_disk', disk_id=disk.disk_id))


@main_bp.route('/disks/<int:disk_id>/delete', methods=['POST'])
def delete_disk(disk_id):
    disk = Disk.query.get_or_404(disk_id)
    disk.songs.clear()
    db.session.delete(disk)
    db.session.commit()
    flash('Ο δίσκος διαγράφηκε με επιτυχία!', 'success')
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
    flash('Ο καλλιτέχνης ενημερώθηκε με επιτυχία!', 'success')
    return redirect(url_for('main.single_person', person_id=person.person_id))


@main_bp.route('/persons/<int:person_id>/delete', methods=['POST'])
def delete_person(person_id):
    person = Person.query.get_or_404(person_id)
    PeopleSong.query.filter_by(person_id=person.person_id).delete(synchronize_session=False)
    db.session.delete(person)
    db.session.commit()
    flash('Ο καλλιτέχνης διαγράφηκε με επιτυχία!', 'success')
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
    flash('Company updated successfully!', 'success')
    return redirect(url_for('main.single_company', company_id=company.company_id))


@main_bp.route('/companies/<int:company_id>/delete', methods=['POST'])
def delete_company(company_id):
    company = _load_company(company_id)
    if company.disks or company.labels:
        flash('Δεν είναι δυνατή η διαγραφή εταιρείας που έχει συνδεδεμένους δίσκους ή ετικέτες.', 'warning')
        return redirect(url_for('main.single_company', company_id=company.company_id))

    db.session.delete(company)
    db.session.commit()
    flash('Η εταιρεία διαγράφηκε με επιτυχία!', 'success')
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
    flash('Η ετικέτα ενημερώθηκε με επιτυχία!', 'success')
    return redirect(url_for('main.single_disk_label', label_id=label.label_id))


@main_bp.route('/disk-labels/<int:label_id>/delete', methods=['POST'])
def delete_disk_label(label_id):
    label = DiskLabel.query.get_or_404(label_id)
    db.session.delete(label)
    db.session.commit()
    flash('Η ετικέτα διαγράφηκε με επιτυχία!', 'success')
    return _safe_redirect('main.home')


# Search categories: maps the dropdown value to a human label. 'everything'
# searches all of them.
SEARCH_CATEGORIES = ['songs', 'disks', 'persons', 'companies', 'disk_labels']


# Number of per-category results shown when searching 'everything'.
SEARCH_PREVIEW = 5


def _like_term(query):
    """Build a contains-match term, escaping LIKE wildcards so user-typed
    '%', '_' or '\\' are matched literally rather than as wildcards."""
    escaped = query.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
    return f'%{escaped}%'


def _search_songs(term):
    # Match a song by its own fields, its disks, or its people (EXISTS subqueries
    # avoid join-duplicated rows so count()/paginate() stay correct).
    return Song.query.filter(
        or_(
            Song.title.ilike(term, escape='\\'),
            Song.notes.ilike(term, escape='\\'),
            Song.disks.any(Disk.name.ilike(term, escape='\\')),
            Song.people.any(PeopleSong.person.has(Person.name.ilike(term, escape='\\'))),
        )
    ).order_by(Song.title)


def _search_disks(term):
    return Disk.query.options(db.joinedload(Disk.company)).filter(
        or_(
            Disk.name.ilike(term, escape='\\'),
            Disk.notes.ilike(term, escape='\\'),
            Disk.sakisid.ilike(term, escape='\\'),
            Disk.company.has(Company.name.ilike(term, escape='\\')),
        )
    ).order_by(Disk.name)


def _search_persons(term):
    return Person.query.filter(
        or_(Person.name.ilike(term, escape='\\'), Person.notes.ilike(term, escape='\\'))
    ).order_by(Person.name)


def _search_companies(term):
    return Company.query.filter(
        or_(Company.name.ilike(term, escape='\\'), Company.info.ilike(term, escape='\\'))
    ).order_by(Company.name)


def _search_disk_labels(term):
    return DiskLabel.query.options(db.joinedload(DiskLabel.company)).filter(
        DiskLabel.label.ilike(term, escape='\\')
    ).order_by(DiskLabel.label)


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
    pagination = None
    per_page = _resolve_per_page()

    if query:
        term = _like_term(query)
        if search_type == 'everything':
            # Show a capped preview per category, each with a "view all" link.
            for category in SEARCH_CATEGORIES:
                q = _SEARCHERS[category](term)
                count = q.count()
                total += count
                results[category] = {'items': q.limit(SEARCH_PREVIEW).all(), 'count': count}
        else:
            page = request.args.get('page', 1, type=int)
            search_query = _SEARCHERS[search_type](term)
            pagination = search_query.paginate(page=page, per_page=per_page, error_out=False)
            if pagination.pages and page > pagination.pages:
                pagination = search_query.paginate(page=pagination.pages, per_page=per_page, error_out=False)
            total = pagination.total
            results[search_type] = {'items': pagination.items, 'count': pagination.total}

    return render_template(
        'search_results.html',
        query=query,
        search_type=search_type,
        results=results,
        total=total,
        pagination=pagination,
        per_page=per_page,
        per_page_choices=PER_PAGE_CHOICES,
        preview=SEARCH_PREVIEW,
    )

