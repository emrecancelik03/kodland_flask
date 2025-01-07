from flask_sqlalchemy import SQLAlchemy
from app import app, db, Question  # Ana uygulama dosyasından import ediyoruz

def add_sample_questions():
    if Question.query.count() == 0:
        questions = [
            Question(
                question_text="Python'da hangi kütüphane AI geliştirmeye yönelik kullanılır?",
                option1="Flask", option2="TensorFlow",
                option3="Django", option4="NumPy",
                correct_option="TensorFlow"
            ),
            Question(
                question_text="Bilgisayar görüşü nedir?",
                option1="Verilerin görsel analizi", option2="Metin analizi",
                option3="Ses tanıma", option4="Karmaşık hesaplamalar",
                correct_option="Verilerin görsel analizi"
            ),
            Question(
                question_text="NLP hangi alanı kapsar?",
                option1="Bilgisayar donanımı", option2="Doğal dil işleme",
                option3="Veritabanı yönetimi", option4="Web geliştirme",
                correct_option="Doğal dil işleme"
            ),
            Question(
                question_text="Yapay zeka nedir?",
                option1="Makine öğrenme ve robotik ile ilgili bilim dalı",
                option2="Sadece robotları içeren bir alan",
                option3="Veritabanı yönetimiyle ilgili bir kavram",
                option4="Sadece insan benzeri zeka",
                correct_option="Makine öğrenme ve robotik ile ilgili bilim dalı"
            )
        ]
        db.session.add_all(questions)
        db.session.commit()
        print("Sorular başarıyla eklendi.")
    else:
        print("Sorular zaten mevcut, ekleme yapılmadı.")

if __name__ == "__main__":
    with app.app_context():  # Uygulama bağlamı içinde çalıştırıyoruz
        db.create_all()  # Veritabanı tablolarını oluştur
        add_sample_questions()
