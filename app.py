from flask import Flask, render_template, redirect, request
# redirect - перенаправление, по сути как render_template
# render_template - только отображение
# Для работы с SQL
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
# Прописываем настройки для подключения к дб
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# Чтобы не показывалась предупреждение
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Создаём дб
db = SQLAlchemy(app)


class Article(db.Model):
    # primary_key - уникальное поле, не будет одинаковых.
    id = db.Column(db.Integer, primary_key=True)
    # nullable - непустое поле недопустимо, если False
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    # Text - для больших объёмов текста
    text = db.Column(db.Text, nullable=False)
    # DateTime - будет тип даных такой
    # default - здесь время по умолчанию
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        '''Этот метод указывает, что, когда будет выбираться объект этого класса,
        будет выдаваться сам объект и будет выдаваться его id'''

        return '<Article %r>' % self.id

# Можно указывать два пути, которые будут считываться за один переход на одну страницу
@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/create-article', methods=['GET', 'POST'])
def create_article():
    if request.method == 'GET':
        return render_template('create-article.html')
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        # Создаём объект бд и сохраняем в него данные
        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка"

@app.route('/posts')
def posts():
    # Обраещение к модели бд (например к первому полю бд)
    # articles = Article.query.first()
    # Взять все записи из бд отсортированых по полю date
    articles = Article.query.order_by(Article.date).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get_or_404(id)
    return render_template("postPage.html", article=article)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"


@app.route('/posts/<int:id>/update', methods=['GET', 'POST'])
def post_update(id):
    article = Article.query.get_or_404(id)

    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        # Создаём объект бд и сохраняем в него данные

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировани статьи произошла ошибка"

    if request.method == 'GET':
        return render_template('postUpdate.html', article=article)


@app.route('/user/<string:user>/<int:id>')
def user(user, id):
    return "User page: " + str(user) + ' - ' + str(id)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

