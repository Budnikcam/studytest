import csv
from datetime import timedelta
from werkzeug.utils import secure_filename
from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory, Response
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from forms import RegistrationForm, LoginForm
from flask_migrate import Migrate
from models import db, User, Lecture, LectureFile  # Добавлено LectureFile
import os

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///your_database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx', 'pptx'}
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)


db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
@login_required
def upload_lecture():
    title = request.form.get('lecture_title')
    lecture_type = request.form.get('lecture_type')
    content = request.form.get('lecture_content')
    files = request.files.getlist('lecture_files')

    if not title or not lecture_type or not content:
        flash('Пожалуйста, заполните все обязательные поля.', 'danger')
        return redirect(url_for('lectures'))

    new_lecture = Lecture(title=title, type=lecture_type, content=content)
    db.session.add(new_lecture)
    db.session.flush()

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Проверка на существование файла
            if os.path.exists(filepath):
                flash(f'Файл с именем "{filename}" уже существует. Пожалуйста, выберите другое имя.', 'danger')
                continue

            try:
                file.save(filepath)
                new_lecture_file = LectureFile(lecture_id=new_lecture.id, filename=filename, filepath=filepath)
                db.session.add(new_lecture_file)
            except Exception as e:
                db.session.rollback()  # Откат транзакции в случае ошибки
                flash(f'Ошибка при загрузке файла "{filename}": {str(e)}', 'danger')
                return redirect(url_for('lectures'))

    try:
        db.session.commit()
        flash(f'Лекция "{title}" загружена успешно!', 'success')
    except Exception as e:
        db.session.rollback()  # Откат транзакции в случае ошибки
        flash(f'Ошибка при сохранении лекции: {str(e)}', 'danger')

    return redirect(url_for('lectures'))

@app.route('/download/<int:lecture_file_id>')
@login_required
def download_lecture(lecture_file_id):
    lecture_file = LectureFile.query.get_or_404(lecture_file_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'], lecture_file.filename, as_attachment=True)

@app.route('/export_users')
@login_required
def export_users():
    if not current_user.is_admin:  
        flash('У Вас нет прав для доступа к этой странице.', 'danger')
        return redirect(url_for('main'))

    users = User.query.all()  

    def generate():
        data = [['ID', 'Username', 'Email']]  
        for user in users:
            data.append([user.id, user.username, user.email])

        csv_writer = csv.writer(Response(), quoting=csv.QUOTE_MINIMAL)
        for row in data:
            csv_writer.writerow(row)

    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=users.csv"})

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Регистрация успешна!', 'success')
            return redirect(url_for('main'))
        except Exception as e:
            db.session.rollback()
            flash(f'Произошла ошибка при регистрации: {str(e)}', 'danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Вы вошли в систему!', 'success')
            return redirect(url_for('main'))
        else:
            flash('Неверный email или пароль', 'danger')
    return render_template('login.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required  
def profile():
    if request.method == 'POST':
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('Фотография профиля загружена!', 'success')
            else:
                flash('Неподходящий формат файла. Загрузите изображение.', 'danger')

    return render_template('profile.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('login'))

@app.route('/lectures.html')
@login_required
def lectures():
    lectures = Lecture.query.all()
    return render_template('lectures.html', lectures=lectures)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_lecture_page():
    if request.method == 'POST':
        return upload_lecture()  # Вызов функции загрузки лекции
    return render_template('upload.html')  # Отображение страницы загрузки лекции

@app.route('/delete_lecture/<int:lecture_id>', methods=['POST'])
@login_required
def delete_lecture(lecture_id):
    if current_user.is_admin:
        lecture = Lecture.query.get(lecture_id)
        if lecture:
            for file in lecture.files:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file.filename)) 
                db.session.delete(file)
            db.session.delete(lecture)
            db.session.commit()
            flash('Лекция успешно удалена!', 'success')
        else:
            flash('Лекция не найдена.', 'danger')
    return redirect(url_for('lectures'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0")
