from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)


class Tempdata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data1 = db.Column(db.String(5))
    data2 = db.Column(db.String(5))
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Tempdata %r>' % (self.id)

class Conf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    relstate = db.Column(db.Integer)
    updateinsec = db.Column(db.Integer)
    tresh1 = db.Column(db.Integer)
    tresh2 = db.Column(db.Integer)

    def __repr__(self):
        return '<Conf %r>' % (self.relstate)
