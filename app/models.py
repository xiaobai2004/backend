from . import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

class TabMaterial(db.Model):
    __talbename__ = 'tab_materials'
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, unique=True, index=True)
    chapter_name = db.Column( db.Unicode, index=True )
    content = db.Column( db.Unicode )
    type = db.Column( db.Integer )
    status = db.Column( db.Integer )

    def __repr__(self):
        return '<Material %r>' % self.chapter_name

class TabConfig(db.Model):
    __tablename__ = 'tab_config'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column( db.String, unique=True )
    value = db.Column( db.String )

    def __repr__(self):
        return '<Config %r : %r>' % ( self.key, self.value )
    

    
