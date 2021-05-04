from gamehype import db
from gamehype.models import Genre, Platform, Game, Company
from config import Config
import pandas
import numpy

games=pandas.read_csv("games.csv")
values = {'System(s)': "", 'Release Date': "1/1/1900", 'Genre': "", 'Developer': ""}
games = games.fillna(value=values)

for i in games.itertuples():
    game = Game(game_name=i[1], release_date=i[3])
    db.session.add(game)
    db.session.commit()
    #see if genres exist, if not, add them
    genres = i[9].split(',')
    for j in genres:
        genre = Genre.query.filter_by(genre_name=j).first()
        if genre is None:
            genre = Genre(genre_name=j)
            db.session.add(genre)
            db.session.commit()
        game.add_genre(genre)
    #see if platforms exist, if not, add them
    platforms = i[2].split(',')
    for k in platforms:
        platform = Platform.query.filter_by(platform_name=k).first()
        if platform is None:
            platform = Platform(platform_name=k)
            db.session.add(platform)
            db.session.commit()
        game.add_platform(platform)
    #see if devs exist, if not, add them
    developers = i[10].split(',')
    for m in developers:
        developer = Company.query.filter_by(company_name=m).first()
        if developer is None:
            developer = Company(company_name=m)
            db.session.add(developer)
            db.session.commit()
        game.add_developer(developer)
    db.session.commit()
