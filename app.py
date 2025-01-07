from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Veritabanı modelleri
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(255), nullable=False)
    option1 = db.Column(db.String(100), nullable=False)
    option2 = db.Column(db.String(100), nullable=False)
    option3 = db.Column(db.String(100), nullable=False)
    option4 = db.Column(db.String(100), nullable=False)
    correct_option = db.Column(db.String(100), nullable=False)

class UserScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)

# Ana sayfa: Soruları Göster
@app.route('/')
def index():
    question_count = Question.query.count()  # Mevcut soru sayısını kontrol et
    highest_score = UserScore.query.order_by(UserScore.score.desc()).first()
    highest_score = highest_score.score if highest_score else 0

    if question_count == 0:
        return render_template('error.html', message="Henüz eklenmiş soru bulunmamaktadır. Lütfen veritabanına soru ekleyin.")
    
    questions = Question.query.all()
    return render_template('index.html', questions=questions, highest_score=highest_score)

# Sonuç sayfası: Kullanıcıların Puanını Göster
@app.route('/result', methods=['POST'])
def result():
    score = 0
    questions = Question.query.all()
    
    # Kullanıcı cevaplarını kontrol et
    for question in questions:
        user_answer = request.form.get(f'q{question.id}')
        if user_answer == question.correct_option:
            score += 1
    
    # Skoru veritabanına kaydet
    user_score = UserScore(score=score)
    db.session.add(user_score)
    db.session.commit()

    # Sonuç sayfasına yönlendir
    return render_template('result.html', score=score)

# Skorları sıfırlamak için rota
@app.route('/reset_scores', methods=['POST'])
def reset_scores():
    UserScore.query.delete()  # Tüm skorları sil
    db.session.commit()
    return redirect(url_for('index'))  # Ana sayfaya yönlendir

if __name__ == '__main__':
    with app.app_context():  # Uygulama bağlamı oluştur
        db.create_all()  # Veritabanını oluştur
    app.run(debug=True)
