from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
    )
from werkzeug.exceptions import abort

from cookbook.auth import login_required
from cookbook.db import get_db

bp = Blueprint('recipes', __name__, url_prefix='/recipes')

@bp.route('/')
@login_required
def index():
    db = get_db()
    recipes = db.execute(
        'SELECT r.id, title, created, description, user_id'
        ' FROM recipe r JOIN user u ON r.user_id = u.id'
        ' ORDER BY title DESC'
        ).fetchall()
    return render_template('recipes/index.html', recipes=recipes)

@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO recipe (user_id, title, description)'
                ' VALUES (?, ?, ?)',
                (g.user['id'], title, description)
                )
            db.commit()
            return redirect(url_for('recipes.index'))

    return render_template('recipes/add.html')

