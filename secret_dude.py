#!flask/bin/python

from app import db, models
#from models import User

us = models.User.query.all()
zombies = []

for u in us:
    if u.comments.count() == 0:
        countf = 0
        for c in u.likers:
            count = 0
            ninam = c.author.nickname
            if ninam != "Henry Guild":
                if ninam != "Gareth Imparato":
                    if ninam != "Hannah Fornero":
                        count = 1
            if count == 0:
                if u.nickname != "Sudhir Gupta":
                    print "Only liking who we want"
                    print u.nickname
                    #zombies.append(u)
            else:
                countf = 1
        for a in u.followed:
            count2 = 0
            ninam2 = a.nickname
            if ninam2 != "Henry Guild":
                if ninam2 != "Gareth Imparato":
                    if ninam2 != "Hannah Fornero":
                        count2 = 1
            if count2 == 0:
                print "Only following who we want"
                print u.nickname
            else:
                countf = 1
        if countf == 0:
            print "Added Zombie"
            zombies.append(u)

for z in zombies:
    if z.nickname == "Sudhir K Gupta":
        zombies.remove(z)
    if z.nickname == "Sam Frampton":
        zombies.remove(z)

for z in zombies:
    print z.nickname
    print z.id
    print "\n"
