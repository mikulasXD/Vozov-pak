
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from database import db, Vozidlo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tajny-klic-pro-flash-zpravy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vozovy_park.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.context_processor
def utility_processor():
    return {'now': datetime.now}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/seznam')
def seznam():
    vozidla = Vozidlo.query.all()
    return render_template('seznam.html', vozidla=vozidla)

@app.route('/detail/<int:id>')
def detail(id):
    vozidlo = Vozidlo.query.get_or_404(id)
    return render_template('detail.html', vozidlo=vozidlo)

@app.route('/pridat', methods=['GET', 'POST'])
def pridat():
    if request.method == 'POST':
        try:
            nove_vozidlo = Vozidlo(
                vyrobce=request.form['vyrobce'],
                model=request.form['model'],
                rok_vyroby=int(request.form['rok_vyroby']),
                stav_tachometru=int(request.form['stav_tachometru']),
                palivo=request.form['palivo'],
                karoserie=request.form['karoserie'],
                spz=request.form['spz'].upper(),
                stav=request.form['stav'],
                v_bazaru_od=datetime.strptime(request.form['v_bazaru_od'], '%Y-%m-%d').date(),
                poznamka=request.form.get('poznamka', '')
            )
            db.session.add(nove_vozidlo)
            db.session.commit()
            flash('Vozidlo bylo úspěšně přidáno!', 'success')
            return redirect(url_for('detail', id=nove_vozidlo.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Chyba při ukládání: Duplicitní SPZ', 'danger')
    
    return render_template('pridat.html', 
                         paliva=Vozidlo.PALIVA,
                         karoserie=Vozidlo.KAROSERIE,
                         stavy=Vozidlo.STAVY)

@app.route('/upravit/<int:id>', methods=['GET', 'POST'])
def upravit(id):
    vozidlo = Vozidlo.query.get_or_404(id)
    
    if request.method == 'POST':
        vozidlo.vyrobce = request.form['vyrobce']
        vozidlo.model = request.form['model']
        vozidlo.rok_vyroby = int(request.form['rok_vyroby'])
        vozidlo.stav_tachometru = int(request.form['stav_tachometru'])
        vozidlo.palivo = request.form['palivo']
        vozidlo.karoserie = request.form['karoserie']
        vozidlo.stav = request.form['stav']
        vozidlo.v_bazaru_od = datetime.strptime(request.form['v_bazaru_od'], '%Y-%m-%d').date()
        vozidlo.poznamka = request.form.get('poznamka', '')
        
        nova_spz = request.form['spz'].upper()
        if nova_spz != vozidlo.spz:
            existujici = Vozidlo.query.filter_by(spz=nova_spz).first()
            if existujici:
                flash('Tato SPZ již existuje!', 'danger')
                return render_template('upravit.html', vozidlo=vozidlo,
                                     paliva=Vozidlo.PALIVA,
                                     karoserie=Vozidlo.KAROSERIE,
                                     stavy=Vozidlo.STAVY)
            vozidlo.spz = nova_spz
        
        try:
            db.session.commit()
            flash('Vozidlo bylo úspěšně upraveno!', 'success')
            return redirect(url_for('detail', id=vozidlo.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Chyba při ukládání: {str(e)}', 'danger')
    
    return render_template('upravit.html', vozidlo=vozidlo,
                         paliva=Vozidlo.PALIVA,
                         karoserie=Vozidlo.KAROSERIE,
                         stavy=Vozidlo.STAVY)

@app.route('/smazat/<int:id>', methods=['POST'])
def smazat(id):
    vozidlo = Vozidlo.query.get_or_404(id)
    db.session.delete(vozidlo)
    db.session.commit()
    flash('Vozidlo bylo smazáno!', 'success')
    return redirect(url_for('seznam'))

@app.route('/statistiky')
def statistiky():
    from database import Vozidlo
    from sqlalchemy import func
    
    celkem = Vozidlo.query.count()
    
     
    do_100k = Vozidlo.query.filter(Vozidlo.stav_tachometru <= 100000).count()
    nad_100k = Vozidlo.query.filter(Vozidlo.stav_tachometru > 100000).count()
    
    
    pocty_paliv = {}
    for palivo in Vozidlo.PALIVA:
        pocet = Vozidlo.query.filter_by(palivo=palivo).count()
        pocty_paliv[palivo] = pocet
    
    
    print(f"Statistiky načteny: Celkem={celkem}, Do 100k={do_100k}, Nad 100k={nad_100k}")
    print(f"Počty paliv: {pocty_paliv}")
    
    return render_template('statistiky.html',
                         celkem=celkem,
                         do_100k=do_100k,
                         nad_100k=nad_100k,
                         pocty_paliv=pocty_paliv)

@app.route('/ajax/kontrola-spz')
def kontrola_spz():
    spz = request.args.get('spz', '').upper()
    vozidlo_id = request.args.get('id', None)
    
    if vozidlo_id:
        existuje = Vozidlo.query.filter(Vozidlo.spz == spz, Vozidlo.id != int(vozidlo_id)).first()
    else:
        existuje = Vozidlo.query.filter_by(spz=spz).first()
    
    return jsonify({'exists': existuje is not None})


@app.route('/api/vozidla', methods=['GET'])
def api_vozidla():
    """Vrátí všechna vozidla jako JSON"""
    vozidla = Vozidlo.query.all()
    return jsonify([{
        'id': v.id,
        'vyrobce': v.vyrobce,
        'model': v.model,
        'rok_vyroby': v.rok_vyroby,
        'stav_tachometru': v.stav_tachometru,
        'spz': v.spz,
        'palivo': v.palivo,
        'karoserie': v.karoserie,
        'stav': v.stav,
        'poznamka': v.poznamka
    } for v in vozidla])
@app.route('/test')
def test():
    return "Flask funguje! Statistiky budou brzy hotovy."

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
