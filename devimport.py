from gamehype import db
from gamehype.models import Company
from config import Config
import pandas
import numpy

devs=pandas.read_csv("devs.csv")
values = {'City': "", 'Area': "", 'Country': "", 'Year Established': 0}
devs = devs.fillna(value=values)
devs['Year Established'] = devs['Year Established'].apply(numpy.int64)

for i in devs.itertuples():
    c=Company(company_name=i[1], city=i[2], region=i[3], country=i[4], established=i[5])
    db.session.add(c)
    db.session.commit()
