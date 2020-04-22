from db import db, Articles, Users, AddedArticles
from datetime import datetime

db.create_all()
print('Database created succesfully!')
print('Populating database...')

print('Adding Initial articles to database...')

tmp = Articles(
    date='02.01.2019',
    link='www.wcjb.com/content/news/Florida-man-doesnt-get-straw-attacks-McDonalds-employee-503812581.html', 
    headline="Florida man doesn't get straw, attacks McDonald's employee", 
    modtime=datetime.now()
)
db.session.add(tmp)
db.session.commit()

tmp = Articles(
    date='01.02.2019',
    link='www.orlandoweekly.com/Blogs/archives/2019/02/01/a-man-actually-punted-a-rabid-coyote-in-kissimmee', 
    headline="A Man Actually Punted a Rabid Coyote in Kissimmee", 
    modtime=datetime.now()
)
db.session.add(tmp)
db.session.commit()

tmp = Articles(
    date='01.03.2019',
    link='www.tampabay.com/florida-politics/buzz/2019/03/01/florida-house-speaker-apologizes-for-referring-to-pregnant-women-as-host-bodies-in-interview-on-abortion/', 
    headline="Florida House Speaker Apologizes for Referring to Pregnant Women as ‘Host Bodies’ in Interview on Abortion", 
    modtime=datetime.now()
)
db.session.add(tmp)
db.session.commit()

tmp = Articles(
    date='01.04.2019',
    link='www.brevardtimes.com/2018/04/florida-man-catches-cooks-baby-manatee/', 
    headline="Florida Man Catches, Cooks Baby Manatee", 
    modtime=datetime.now()
)
db.session.add(tmp)
db.session.commit()

tmp = Articles(
    date='01.05.2019',
    link='wtfflorida.com/news/crime/after-crashing-his-car-florida-man-asks-trooper-if-he-can-get-more-meth/', 
    headline="After Crashing his Car, Florida Man Asks Trooper if He Can Get More Meth", 
    modtime=datetime.now()
)
db.session.add(tmp)
db.session.commit()

tmp = Articles(
    date='01.06.2018',
    link='wtfflorida.com/news/crime/florida-man-flees-from-car-crash-crashes-twice-again-cusses-out-good-samaritan-victims/', 
    headline="Florida Man Flees from Car Crash, Crashes Twice Again, Cusses Out Good Samaritan Victims", 
    modtime=datetime.now()
)
db.session.add(tmp)
db.session.commit()

tmp = Articles(
    date='09.07.2019',
    link='www.rblandmark.com/News/Articles/7-9-2019/Florida-man-chants-as-police-try-to-arrest-him-%7C-Police-reports-July-1_7/', 
    headline="Florida man chants as police try to arrest him", 
    modtime=datetime.now()
)
db.session.add(tmp)
db.session.commit()

tmp = Articles(
    date='01.08.2018',
    link='www.country935.ca/2018/08/01/florida-man-carries-live-alligator-liquor-store/', 
    headline="Florida Man carries Live Alligator into Liquor Store", 
    modtime=datetime.now()
)
db.session.add(tmp)
db.session.commit()

tmp = Articles(
    date='01.09.2018',
    link='www.wsbradio.com/news/florida-man-accused-shooting-home-after-woman-leaves-negative-restaurant-review/sPcDDNf3nhs5jIk1GDamwM/', 
    headline="Florida man accused of shooting at home after woman leaves negative restaurant review", 
    modtime=datetime.now()
)
db.session.add(tmp)
db.session.commit()

tmp = Articles(
    date='01.10.2019',
    link='www.wwnytv.com/2019/10/01/florida-man-tried-sell-beer-dolphins-game-police-say/', 
    headline="Florida man tried to sell beer for $724 at Dolphins game, police say", 
    modtime=datetime.now()
)
db.session.add(tmp)
db.session.commit()

tmp = Articles(
    date='13.11.2018',
    link='newschannel9.com/news/offbeat/florida-man-breaks-into-restaurant-strips-naked-eats-noodles-plays-bongos', 
    headline="Florida man breaks into restaurant, strips naked, eats noodles, plays bongos", 
    modtime=datetime.now()
)
db.session.add(tmp)
db.session.commit()

print('Successfully populated the database with initial articles!')
print('Populating the database with initial users...')

user = Users(username='sample1')
db.session.add(user)
db.session.commit()
article = AddedArticles(
    headline="First added article", 
    modtime=datetime.now(), 
    owner=user
)
db.session.add(article)
db.session.commit()

user = Users(username='sample2')
db.session.add(user)
db.session.commit()
article = AddedArticles(
    headline="Second added article", 
    modtime=datetime.now(), 
    owner=user
)
db.session.add(article)
db.session.commit()

user = Users(username='sample3')
db.session.add(user)
db.session.commit()
article = AddedArticles(
    headline="Third added article", 
    modtime=datetime.now(), 
    owner=user
)
db.session.add(article)
db.session.commit()
