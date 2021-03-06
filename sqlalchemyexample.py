from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
class Factoid(Base):
    __tablename__ = 'factoids'

    id = Column(Integer, primary_key=True)
    keyword = Column(String, unique=True)
    response = Column(String)

    def __init__(self, key, response):
        self.keyword = key
        self.response = response

    def __repr__(self):
        return "<Factoid('%s', '%s')>" % (self.keyword, self.response)

class FactoidAlreadyExists(Exception): pass
class NoSuchFactoid(Exception): pass

class FactoidManager(object):
    def __init__(self, db="/:memory:"):
        self.engine = create_engine('sqlite://%s' % db)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def addFact(self, key, response, replace=False):
        key = key.lower()
        exists = self.session.query(Factoid).filter_by(keyword=key)

        if exists.count():
            if not replace:
                raise FactoidAlreadyExists, key

        if exists.count():
            fact = exists.first()
            fact.response = response
        else:
            fact = Factoid(key, response)
            self.session.add(fact)

        self.session.commit()
        return fact

    def updateFact(self, key, response):
        return self.addFact(key, response, True)

    def getFact(self, key):
        key = key.lower()
        exists = self.session.query(Factoid).filter_by(keyword=key)

        if not exists.count():
            raise NoSuchFactoid, key

        return exists.first().response

    def remFact(self, key):
        exists = self.session.query(Factoid).filter_by(keyword=key)

        if not exists.count():
            raise NoSuchFactoid, key

        self.session.delete(exists.first())
        self.session.commit()

if __name__ == "__main__":
    m = FactoidManager()

    print "Adding bot"
    m.addFact("bot", "I am a bot")

    print "Adding User"
    m.addFact("User", "Some guy I know")

    try:
        print "Trying to redefine bot, without replacing"
        m.addFact("bot", "should make an error")
    except FactoidAlreadyExists, key:
        print "Passed, FactoidAlready raised for %s" % key

    try:
        print "Trying to replace bot"
        m.updateFact("bot", "Updated!")
        print "Passed, bot is now '%s'" % m.getFact("bot")
    except FactoidAlreadyExists, key:
        print "Got FactoidAlreadyExists, %s" % key
    except Exception, err:
        print "Got error: %s" % err

    print "User is '%s'" % m.getFact("User")
    print "bot is '%s'" % m.getFact("bot")

    print "Deleting bot."
    m.remFact('bot')
    try:
        print m.getFact('bot')
    except NoSuchFactoid:
        print "Passed: NoSuchFactoid"