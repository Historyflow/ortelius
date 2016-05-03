import sqlalchemy
import datetime
from ortelius import db
from ortelius.types.historical_date import HistoricalDate as hd
from ortelius.models.Coordinates import Coordinates, Shape, Quadrant
from ortelius.models.Date import Date, Millenium, Century, Year
from ortelius.models.Fact import Fact, FactType
from ortelius.models.Hist_region import HistRegion, HistPlace
from ortelius.models.User import User, UsersRoles, Role

from test_data.test_facts import test_facts, test_hist_regions

def create_admin():
    """Creates the admin user."""
    admin_role = Role(id=1, name='admins', label='Administrators')
    admin_user = User(id=1, username='admin',
                      email='ad@min.com', password='admin', active=True)
    admin_user_role = UsersRoles(user_id=admin_user.id, role_id=admin_role.id)
    db.session.add(admin_role)
    db.session.add(admin_user)
    db.session.commit()
    db.session.add(admin_user_role)
    db.session.commit()

def create_years():
    # Create millenimus, centuries and years from -5000 to 2999
    for i in (-5, -4, -3, -2, -1, 1, 2, 3):
        print('Create millenium: ' + str(i))
        mil = Millenium(number=i)
        db.session.add(mil)
        for j in range(0, 10):
            centNumber = j+(i*10) if i < 0 else j + 1 + ((i-1)*10)
            cent = Century(number=centNumber, millenium=mil)
            db.session.add(cent)
            for k in range(0, 100):
                yearNumber = k+(centNumber*100) - 1 if i < 0 else k + ((centNumber-1)*100)
                year = Year(number=yearNumber, century=cent)
                db.session.add(year)

    db.session.commit()

def create_fact_types():
    f_types = [
                ['battle', 'сражение'],
                ['peace_treaty', 'мирный договор']
              ]

    for t in f_types:
        new_type = FactType(name=t[0], label=t[1])
        db.session.add(new_type)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()

def create_facts():
    for f in test_facts:
        new_start_date = Date.create(date=hd(f['start_date']))
        new_end_date = Date.create(date=hd(f['end_date']))
        if f['coordinates']:
            point = Coordinates.create(f['coordinates'][0], f['coordinates'][1])
            db.session.add(point)

            new_shape = Shape(start_date=new_start_date, end_date=new_end_date, coordinates=[point])
            db.session.add(new_shape)

        new_fact = Fact(name = f['name'],
                        label=f['label'],
                        description=f['description'],
                        info=f['info'],
                        weight=f['weight'],
                        type=FactType.create(name=f['type'][0], label=f['type'][1]),
                        start_date=new_start_date,
                        end_date=new_end_date,
                        text=f['text'],
                        shape=new_shape
                       )
        db.session.add(new_fact)
        db.session.commit()

def create_hist_regions():
    for region in test_hist_regions:
        region_facts = []
        region_shapes = []
        start_date = None
        end_date = None
        if region['start_date'] != None:
            start_date = Date.create(date=hd(region['start_date']))

        if region['end_date'] != None:
            end_date = Date.create(date=hd(region['end_date']))

        if region['facts']:
            for fact in region['facts']:
                region_facts.append(Fact.query.get(fact))

        if region['shapes']:
            for shape in region['shapes']:
                region_shapes.append(Shape.query.get(shape))

        hr = HistRegion(name=region['name'],
                        label=region['label'],
                        description=region['description'],
                        text=region['text'],
                        start_date=start_date,
                        end_date=end_date,
                        shapes=region_shapes,
                        facts=region_facts
                        )
        db.session.add(hr)
    db.session.commit()


def create_shape():
    point = Coordinates.create(66.82, 10.5)
    sh = Shape(start_date=Date.create(date=hd(datetime.date.today())), end_date=Date.create(date=hd(datetime.date.today())), coordinates=[point])
    db.session.add(sh)
    db.session.commit()

def create_quadrants():
    for q in Quadrant.quadrants:
        quadrant = Quadrant(hash=Quadrant.make_hash(q[0], q[1]))
        db.session.add(quadrant)
    db.session.commit()