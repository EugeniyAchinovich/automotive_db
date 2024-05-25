from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///AutomotiveDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(300), nullable=False)


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    owner = db.relationship('Owner', backref=db.backref('cars', lazy=True))


class Maintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)


class Inspection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    results = db.Column(db.Text, nullable=False)


class Insurance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Integer, nullable=False)


class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False)


class Repair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Integer, nullable=False)


class FuelExpense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fuel_amount = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Integer, nullable=False)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/cars')
def cars():
    cars_list = Car.query.all()
    return render_template("cars.html", cars=cars_list)


@app.route('/cars/<int:car_id>')
def car_detail(car_id):
    car = Car.query.get(car_id)
    inspection = Inspection.query.get(car_id)
    insurance = Insurance.query.get(car_id)
    maintenance = Maintenance.query.get(car_id)
    incident = Incident.query.get(car_id)
    fuelExpense = FuelExpense.query.get(car_id)

    return render_template("car_detail.html",
                           car=car,
                           maintenance=maintenance,
                           inspection=inspection,
                           incident=incident,
                           insurance=insurance,
                           fuelExpense=fuelExpense)


@app.route('/create-owner', methods=['POST', 'GET'])
def create_owner():
    if request.method == "POST":
        name = request.form['name']
        contact_info = request.form['contact_info']

        owner = Owner(name=name, contact_info=contact_info)

        try:
            db.session.add(owner)
            db.session.commit()
            return redirect('/create-car')
        except:
            return "Ошибка при добавлении"
    else:
        return render_template("create_owner.html")


@app.route('/create-car', methods=['POST', 'GET'])
def create_car():
    if request.method == "POST":
        model = request.form['model']
        year = request.form['year']
        owner_id = request.form['owner_id']

        car = Car(model=model, year=year, owner_id=owner_id)

        try:
            db.session.add(car)
            db.session.commit()
            return redirect(f'create-maintenance/{owner_id}')
        except:
            return "Ошибка при добавлении"
    else:
        owners = Owner.query.all()
        return render_template("create_car.html", owners=owners)


@app.route('/create-maintenance/<int:car_id>', methods=['POST', 'GET'])
def create_maintenance(car_id):
    if request.method == "POST":
        date = datetime.strptime(request.form['date'], '%Y-%m-%d %H:%M:%S')
        description = request.form['description']

        maintenance = Maintenance(car_id=car_id, date=date, description=description)

        try:
            db.session.add(maintenance)
            db.session.commit()
            return redirect(f'create-inspection/{car_id}')
        except:
            return "Ошибка при добавлении"
    else:
        return render_template("create_maintenance.html", car_id=car_id)


@app.route('/create-inspection/<int:car_id>', methods=['POST', 'GET'])
def create_inspection(car_id):
    if request.method == "POST":
        date = datetime.strptime(request.form['date'], '%Y-%m-%d %H:%M:%S')
        results = request.form['result']

        inspection = Inspection(car_id=car_id, date=date, results=results)

        try:
            db.session.add(inspection)
            db.session.commit()
            return redirect(f'create-incident/{car_id}')
        except:
            return "Ошибка при добавлении"
    else:
        return render_template("create_inspection.html", car_id=car_id)


@app.route('/create-incident/<int:car_id>', methods=['POST', 'GET'])
def create_incident(car_id):
    if request.method == "POST":
        date = datetime.strptime(request.form['date'], '%Y-%m-%d %H:%M:%S')
        description = request.form['description']
        status = request.form['status']

        incident = Incident(car_id=car_id, date=date, description=description, status=status)

        try:
            db.session.add(incident)
            db.session.commit()
            return redirect(f'create-insurance/{car_id}')
        except:
            return "Ошибка при добавлении"
    else:
        return render_template("create_incident.html", car_id=car_id)


@app.route('/create-insurance/<int:car_id>', methods=['POST', 'GET'])
def create_insurance(car_id):
    if request.method == "POST":
        date1 = datetime.strptime(request.form['date1'], '%Y-%m-%d')
        date2 = datetime.strptime(request.form['date2'], '%Y-%m-%d')
        amount = request.form['amount']

        insurance = Insurance(car_id=car_id, start_date=date1, end_date=date2, amount=amount)

        try:
            db.session.add(insurance)
            db.session.commit()
            return redirect(f'create-fuel-expense/{car_id}')
        except:
            return "Ошибка при добавлении"
    else:
        return render_template("create_insurance.html", car_id=car_id)


@app.route('/create-fuel-expense/<int:car_id>', methods=['POST', 'GET'])
def create_fuel_expense(car_id):
    if request.method == "POST":
        date = datetime.strptime(request.form['date'], '%Y-%m-%d %H:%M:%S')
        fuel_amount = request.form['amount']
        cost = request.form['price_per_liter']

        fuel_expense = FuelExpense(car_id=car_id, date=date, fuel_amount=fuel_amount, cost=cost)

        try:
            db.session.add(fuel_expense)
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка при добавлении"
    else:
        return render_template("create_fuelexpense.html", car_id=car_id)


@app.route('/cars/<int:car_id>/update', methods=['POST', 'GET'])
def car_update(car_id):
    car = Car.query.get(car_id)

    if request.method == "POST":
        car.model = request.form['model']
        car.year = request.form['year']
        car.owner_id = request.form['owner_id']

        try:
            db.session.commit()
            return redirect('/cars')
        except:
            return "Ошибка при обновлении"
    else:
        owners = Owner.query.all()
        return render_template("car_update.html", car=car, owners=owners)


@app.route('/cars/<int:car_id>/delete')
def car_delete(car_id):
    car = Car.query.get_or_404(car_id)

    try:
        db.session.delete(car)
        db.session.commit()
        return redirect('/cars')
    except:
        return "Ошибка при удалении"


if __name__ == "__main__":
    app.run(debug=True)
