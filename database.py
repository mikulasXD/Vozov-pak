

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Vozidlo(db.Model):
    __tablename__ = 'vozidla'
    
    id = db.Column(db.Integer, primary_key=True)
    vyrobce = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    rok_vyroby = db.Column(db.Integer, nullable=False)
    stav_tachometru = db.Column(db.Integer, nullable=False)
    palivo = db.Column(db.String(20), nullable=False)
    karoserie = db.Column(db.String(20), nullable=False)
    spz = db.Column(db.String(10), unique=True, nullable=False)
    stav = db.Column(db.String(20), nullable=False)
    v_bazaru_od = db.Column(db.Date, nullable=False, default=datetime.now().date)
    poznamka = db.Column(db.Text, nullable=True)
    
    # Možné hodnoty pro výběrová pole
    PALIVA = ['Benzin', 'Nafta', 'LPG', 'CNG', 'Elektro', 'Hybrid']
    KAROSERIE = ['Sedan', 'Hatchback', 'Kombi', 'SUV', 'MPV', 'Kupé', 'Kabriolet']
    STAVY = ['Výborný', 'Velmi dobrý', 'Dobrý', 'Po opravě', 'Na náhradní díly']
    
    def to_dict(self):
        return {
            'id': self.id,
            'vyrobce': self.vyrobce,
            'model': self.model,
            'rok_vyroby': self.rok_vyroby,
            'stav_tachometru': self.stav_tachometru,
            'palivo': self.palivo,
            'karoserie': self.karoserie,
            'spz': self.spz,
            'stav': self.stav,
            'v_bazaru_od': self.v_bazaru_od.strftime('%d.%m.%Y') if self.v_bazaru_od else '',
            'poznamka': self.poznamka
        }
    
    def __repr__(self):
        return f'<Vozidlo {self.vyrobce} {self.model} {self.spz}>'