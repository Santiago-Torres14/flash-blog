from flask import Blueprint, render_template, request, url_for, redirect, flash
from .models import Article
from flask_login import login_required, current_user
from . import db
import markdown

views = Blueprint('views', __name__)

@views.route('/')
def home():
    articles = Article.query.order_by(Article.date).all()
    return render_template('home.html', articles=articles, user=current_user)

@views.route('/create-article', methods=["GET", "POST"])
@login_required
def create_article():
    if request.method == "POST":
        article_title = request.form.get('title')
        article_description = request.form.get('description')
        article_text = request.form.get('text')

        if len(article_text) < 50:
            flash('Article is too short', category='error')
        elif len(article_text) < 5:
            flash('Article title too short', category='error')
        elif len(article_description) < 20:
            flash('Article description too short', category='error')
        else:
            new_article = Article(author_id=current_user.id, title=article_title, description=article_description, text=article_text)
            db.session.add(new_article)
            db.session.commit()
            flash("Article created", category='success')

            return redirect(url_for('views.home'))
    
    if request.method == "GET":
        return render_template('create_article.html', user=current_user)
    
    return redirect(url_for('views.home'))

@views.route('/delete/<int:id>')
@login_required
def delete(id):
    article_to_delete = Article.query.get_or_404(id)

    if article_to_delete:
        if article_to_delete.author_id == current_user.id:
            try:
                db.session.delete(article_to_delete)
                db.session.commit()
            except:
                flash("There was a problem deleting your article", category="error")
        else:
            flash('You cannot delete this article', category='error')
    
    return redirect(url_for('views.home'))

@views.route('/edit/<int:id>', methods=["GET","POST"])
@login_required
def edit_article(id):
    article_to_edit = Article.query.get_or_404(id)
    
    if request.method == "POST":
        if article_to_edit:
            if article_to_edit.author_id == current_user.id:
                try:
                    article_to_edit.title = request.form.get("title")
                    article_to_edit.description = request.form.get('description')
                    article_to_edit.text = request.form.get('text')
                    db.session.add(article_to_edit)
                    db.session.commit()
                    flash("Article edited", category="success")

                    return redirect(url_for('views.home'))
                except:
                    flash("There was a problem editing your article", category="error")
            else:
                flash('You cannot edit this article', category='error')
    elif request.method == "GET":
        if article_to_edit.author_id == current_user.id:
            return render_template("edit_article.html", article=article_to_edit, user=current_user)

    flash('You cannot edit this article', category='error')
    return redirect(url_for('views.home'))


@views.route('/article/<int:id>')
def article(id):
    article = Article.query.get_or_404(id)
    article.text = markdown.markdown(article.text)
    print(article)
    return render_template('article.html', article=article, user=current_user)