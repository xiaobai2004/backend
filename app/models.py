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

class Scriptures(db.Model):
    __tablename__ = "wenbai_scriptures"
    id = db.Column(db.Integer, primary_key=True)
    scripture_display=db.Column(db.Unicode(16), index=True)
    scripture_title=db.Column(db.Unicode(128), index=True)

    def __repr__(self):
        return '<Scripture  %r>' % self.scripture_display

class Chapters(db.Model):
    __tablename__ = "wenbai_chapters"
    id = db.Column(db.Integer, primary_key=True)
    scripture_id=db.Column(db.Integer, db.ForeignKey('wenbai_scriptures.id'))
    chapter_display=db.Column(db.Unicode(16), index=True)
    chapter__title=db.Column(db.Unicode(128), index=True)

    def __repr__(self):
        return '<Chapter  %r>' % self.chapter_display

class Sections(db.Model):
    __tablename__ = "wenbai_sectons"
    id = db.Column(db.Integer, primary_key=True)
    chapter_id=db.Column(db.Integer, db.ForeignKey('wenbai_chapters.id'))
    section_display=db.Column(db.Unicode(16), index=True)
    section__title=db.Column(db.Unicode(128), index=True)

    def __repr__(self):
        return '<Section  %r>' % self.section_display


class Sentences(db.Model):
    __tablename__ = "wenbai_sentences"
    id = db.Column(db.BigInteger, primary_key=True)
    scripture_id=db.Column(db.Integer, db.ForeignKey('wenbai_scriptures.id'))
    chapter_id=db.Column(db.Integer, db.ForeignKey('wenbai_scriptures.id'))
    section_id=db.Column(db.Integer, db.ForeignKey('wenbai_scriptures.id'))
    classic_text = db.Column(db.Text )
    modern_text  = db.Column(db.Text )

    def __repr__(self):
        return '<Sectence  %r>' % self.id
    

class TabMaterial(db.Model):
    __tablename__ = 'tab_materials'
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
    

    
