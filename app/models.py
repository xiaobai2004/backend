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



class Sentence(db.Model):
    __tablename__ = "wenbai_sentences"
    id = db.Column(db.BigInteger, primary_key=True)
    scripture_id=db.Column(db.Integer, db.ForeignKey('wenbai_scriptures.id'))
    chapter_id=db.Column(db.Integer, db.ForeignKey('wenbai_chapters.id'))
    section_id=db.Column(db.Integer, db.ForeignKey('wenbai_sections.id'))
    classic_text = db.Column(db.Text )
    modern_text  = db.Column(db.Text )
    annotation_text = db.Column(db.Text )
    updated_at=db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP') )
    created_at=db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP') )

    def __repr__(self):
        return '<Sectence  %r>' % self.id

class Section(db.Model):
    __tablename__ = "wenbai_sections"
    id = db.Column(db.Integer, primary_key=True)
    chapter_id=db.Column(db.Integer, db.ForeignKey('wenbai_chapters.id'))
    section_display=db.Column(db.Unicode(16), index=True)
    section__title=db.Column(db.Unicode(128), index=True)
    updated_at=db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP') )
    created_at=db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP') )

    sentences = []

    def __repr__(self):
        return '<Section  %r>' % self.section_display

class Chapter(db.Model):
    __tablename__ = "wenbai_chapters"
    id = db.Column(db.Integer, primary_key=True)
    scripture_id=db.Column(db.Integer, db.ForeignKey('wenbai_scriptures.id'))
    chapter_display=db.Column(db.Unicode(16), index=True)
    chapter__title=db.Column(db.Unicode(128), index=True)
    updated_at=db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP') )
    created_at=db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP') )

    def __repr__(self):
        return '<Chapter  %r>' % self.chapter_display

class Scripture(db.Model):
    __tablename__ = "wenbai_scriptures"
    id = db.Column(db.Integer, primary_key=True)
    scripture_display=db.Column(db.Unicode(16), unique=True, index=True)
    scripture_title=db.Column(db.Unicode(128), index=True)
    updated_at=db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP') )
    created_at=db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP') )

    def __repr__(self):
        return '<Scripture  %r>' % self.scripture_display


class RecentList(db.Model):
    __tablename__ = "wenbai_recent_list"
    id = db.Column(db.Integer, primary_key=True)
    reader_id = db.Column(db.Integer, db.ForeignKey('wenbai_readers.id'))
    scripture_id=db.Column(db.Integer )
    chapter_id=db.Column(db.Integer)
    section_id=db.Column(db.Integer)
    sentence_id=db.Column(db.BigInteger)
    updated_at=db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP') )
    created_at=db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP') )

    def __repr__(self):
        return '<Recent  %r>' % self.id

class Reader(db.Model):
    __tablename__ = "wenbai_readers"
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.Unicode(64), index=True)
    updated_at=db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP') )
    created_at=db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP') )

    def __repr__(self):
        return '<Reader  %r>' % self.id


