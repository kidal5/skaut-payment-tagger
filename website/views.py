from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Tag, User
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/manage-tags', methods=['GET', 'POST'])
@login_required
def manageTags():
    if request.method == 'POST':
        tag_name = request.form.get('new-tag-name') #Gets the note from the HTML 
        new_tag_description = request.form.get('new-tag-description') #Gets the note from the HTML 

        old_tag = Tag.query.filter_by(id_string=tag_name).first()
        if old_tag:
            flash(f'Tag {tag_name} už existuje.', category='error')
        elif len(tag_name) > 1:
            db.session.add(Tag(id_string = tag_name, description = new_tag_description, created_user=current_user.id))
            db.session.commit()
            flash('Nový tag vytvořen!', category='success')

    tags = db.session.query(Tag, User).order_by(Tag.id_string).join(User, Tag.created_user==User.id).all()
    return render_template("manage_tags.html", user=current_user, tags=tags)


@views.route('/delete-tag', methods=['POST'])
def delete_tag():  
    tagId = json.loads(request.data)['tagId']
    tag = Tag.query.get(tagId)
    if tag:
        db.session.delete(tag)
        db.session.commit()

    return jsonify({})
