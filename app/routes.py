from flask import Blueprint, render_template, redirect, url_for, flash
from .models.Song import Song
from .models.db import db
from .forms.disk_form import DiskForm
from .models.Disk import Disk
from .models.Company import Company
from .forms.company_form import CompanyForm



main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():

    songs = Song.query.limit(5).all()
    print(songs)

    return render_template('index.html', songs=songs)

@main_bp.route('/add-disk', methods=['GET', 'POST'])
def add_disk():
    form = DiskForm()
    if form.validate_on_submit():
        new_disk = Disk(
            name=form.name.data,
            company_id=form.company_id.data,
            size=form.size.data,
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

