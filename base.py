from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# create an engine
engine = create_engine('postgresql://usr:pass@localhost:5432/beeherotask')

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
Base = declarative_base()