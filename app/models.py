from app import db
from app import app
from flask import flash
from datetime import datetime, timedelta
from sqlalchemy import desc, asc
import arrow
import sys
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
import numpy as np
import math
from geopy.geocoders import GoogleV3
geolocator = GoogleV3()
timeChanger = timedelta(hours=5, minutes=0)
da_time = datetime.now() - timeChanger
ROLE_USER = 0
ROLE_ADMIN = 1
ROLE_PROF = 2
ROLE_TA = 3
if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    #import flask.ext.whooshalchemy as whooshalchemy
    #c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


followers = db.Table('followers', db.Model.metadata,
    db.Column('fan_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
    )

friend_requests = db.Table('friend_requests', db.Model.metadata,
    db.Column('requester_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('requested_id', db.Integer, db.ForeignKey('user.id'))
    )

friends_confirmed = db.Table('friends_confirmed', db.Model.metadata,
    db.Column('requester_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('requested_id', db.Integer, db.ForeignKey('user.id'))
    )

comment_likers = db.Table('comment_likers', db.Model.metadata,
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    )

hashtagOwners = db.Table('hashtagOwners', db.Model.metadata,
    db.Column('hash_id', db.Integer, db.ForeignKey('hashtag.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    )

hashtagCommentOwners = db.Table('hashtagCommentOwners', db.Model.metadata,
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id')),
    db.Column('hash_id', db.Integer, db.ForeignKey('hashtag.id'))
    )

strong_hashtag_connection = db.Table('strong_hashtag_connection', db.Model.metadata,
    db.Column('parent_id', db.Integer, db.ForeignKey('hashtag.id')),
    db.Column('child_id', db.Integer, db.ForeignKey('hashtag.id'))
    )

weak_hashtag_connection = db.Table('weak_hashtag_connection', db.Model.metadata,
    db.Column('parent_id', db.Integer, db.ForeignKey('hashtag.id')),
    db.Column('child_id', db.Integer, db.ForeignKey('hashtag.id'))
    )


class User(db.Model):
    __searchable__ = ['nickname']
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    fb_id = db.Column(db.Integer, index=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    sentMessages = db.relationship('DirectMessage', foreign_keys='DirectMessage.user_id', backref='author', lazy='dynamic')
    receivedMessages = db.relationship('DirectMessage', foreign_keys='DirectMessage.receiver_id', backref='receiver', lazy='dynamic')
    is_private = db.Column(db.Boolean, default=True, index=True)
    recentLoc = db.Column(db.String())
    recentLatLon = db.Column(db.String())
    apsToken = db.Column(db.String())
    fbfriends = db.Column(db.String())
    friends = db.relationship('User', secondary=friends_confirmed, primaryjoin=friends_confirmed.c.requester_id == id, secondaryjoin=friends_confirmed.c.requested_id == id, backref=db.backref('frienders', lazy='dynamic'), lazy='dynamic')
    requests = db.relationship('User', secondary=friend_requests, primaryjoin=friend_requests.c.requester_id == id, secondaryjoin=friend_requests.c.requested_id == id, backref=db.backref('requesters', lazy='dynamic'), lazy='dynamic')
    followed = db.relationship('User', secondary=followers, primaryjoin=followers.c.fan_id == id, secondaryjoin=followers.c.followed_id == id, backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    recTime = db.Column(db.DateTime)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.nickname

    def follow(self, user):
        if self.is_following(user) is False:
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user) is True:
            self.followed.remove(user)
            return self

    def is_following(self, user):
        if self.followed.filter(followers.c.followed_id == user.id).count() > 0:
            return True
        else:
            return False

    def add_friend(self, user):
        self.friends.append(user)
        db.session.commit()

    def is_friend(self, user):
        if self.friends.filter(friends_confirmed.c.requested_id == user.id).count() > 0:
            return True
        elif user.friends.filter(friends_confirmed.c.requested_id == self.id).count() > 0:
            return True
        else:
            return False

    def request_friend(self, user):
        if self.has_requested(user) is False:
            self.requests.append(user)
            db.session.commit()

    def has_requested(self, user):
        if self.requests.filter(friend_requests.c.requested_id == user.id).count() > 0:
            return True
        else:
            return False

    def is_requested(self, user):
        if self.requesters.filter(friend_requests.c.requester_id == user.id).count() > 0:
            return True
        else:
            return False

    def get_status(self, user):
        if self.is_friend(user) is True:
            return 'friend'
        if self.has_requested(user) is True:
            return 'requester'
        if self.is_requested(user) is True:
            return 'requested'
        return 'connect'

    def add_fbfriend(self, fbid):
        if self.fbfriends is None:
            self.fbfriends = fbid
            db.session.commit()
            print 'did add first friend'
            return
        if fbid not in self.fbfriends:
            self.fbfriends += ', ' + fbid
            db.session.commit()
            print 'Did add friend'

    def get_mutual_fbfriends(self, user):
        fbf1 = []
        if self.fbfriends is not None:
            fbf1 = self.fbfriends.split(', ')
        fbf2 = []
        if user.fbfriends is not None:
            fbf2 = user.fbfriends.split(', ')
        return list(set(fbf1) & set(fbf2))

    def get_top_comments(self):
        return sorted(self.comments, key=lambda Comment: Comment.user_likers.count(), reverse=True)

    def get_total_likes(self):
        k = 0
        for c in self.comments.all():
            k = k + c.get_likes()

        return k

    def setRecLoc(self, rL):
        self.recentLatLon = rL
        db.session.commit()

    def setRecTime(self):
        self.recTime = datetime.now()
        db.session.commit()


    def get_messages(self, user):
        coms1 = self.sentMessages.filter_by(receiver_id = user.id).all()
        coms2 = self.receivedMessages.filter_by(user_id = user.id).all()
        coms3 = coms1 + coms2
        #coms4 = coms3.query.order_by(desc(DirectMessage.atTime)).all()
        return coms3



class Message(db.Model):
    #__searchable__ = ['body']
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    checkit = db.Column(db.String())
    body = db.Column(db.String(500, convert_unicode=True))
    whatthefuck = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reciever_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    latLon = db.Column(db.String())
    atTime = db.Column(db.DateTime)

#     # def __init__(self, body, user_id, reciever_id, atTime):
#     #     self.body = body
#     #     self.user_id = user_id
#     #     self.reciever_id =reciever_id
#     #     self.atTime = atTime

class DirectMessage(db.Model):
    __tablename__ = "directmessage"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500, convert_unicode=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    atTime = db.Column(db.DateTime)

class Comment(db.Model):
    __searchable__ = ['body']
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500, convert_unicode=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    atTime = db.Column(db.DateTime)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    depth = db.Column(db.Integer, default=1)
    latLon = db.Column(db.String())
    locationAddress = db.Column(db.String())
    imgLink = db.Column(db.String())
    bodyUni = db.Column(db.Unicode)
    hashtags = db.relationship('Hashtag', secondary=hashtagCommentOwners, primaryjoin=hashtagCommentOwners.c.comment_id == id, backref=db.backref('comments', lazy='dynamic'), lazy='dynamic')
    user_likers = db.relationship('User', secondary=comment_likers, backref=db.backref('likers', lazy='dynamic'), lazy='dynamic')
    reply_comments = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')

    def set_depth(self):
        """
                call after initializing
        """
        if self.parent:
            self.depth = self.parent.depth + 1
            db.session.commit()
        else:
            self.depth = 1
            db.session.commit()

    def get_comments(self, order_by = 'timestamp'):
        """
                default order by timestamp
        """
        if order_by == 'timestamp':
            print 'got a comment'
            return self.reply_comments.order_by(desc(Comment.atTime)).all()
        else:
            return self.reply_comments.order_by(desc(Comment.atTime)).all()

    def did_like(self, User):
        """
                When a user upvotes a comment, append that user to the list
        """
        if self.has_liked(User) == False:
            self.user_likers.append(User)
            db.session.commit()

    def did_unlike(self, User):
        """
                When a user downvotes a comment, remove that user to the list
        """
        if self.has_liked(User) == True:
            self.user_likers.remove(User)
            db.session.commit()

    def has_liked(self, User):
        """
                Checks the db of users who have upvoted comment. Returns 0 if this user has not.
        """
        if self.user_likers.filter(comment_likers.c.user_id == User.id).count() == 0:
            return False
        else:
            return True

    def get_likes(self):
        return self.user_likers.count()

    def add_hashtag(self, hashtag):
        self.hashtags.append(hashtag)

    def getDate(self):
        a = arrow.get(self.atTime).format('MMMM d, YYYY')
        return a

    def getAtTime(self):
        a = arrow.get(self.atTime)
        a = a.humanize()
        a = a.replace('seconds', 's')
        a = a.replace('second', 's')
        a = a.replace('an hour', '1 h')
        a = a.replace('hours', 'h')
        a = a.replace('hour', 'h')
        a = a.replace('a day', '1 d')
        a = a.replace('days', 'd')
        a = a.replace('day', 'd')
        a = a.replace('a minute', '1 m')
        a = a.replace('minutes', 'm')
        a = a.replace('minute', 'm')
        a = a.replace('a month', '1 M')
        a = a.replace('months', 'M')
        a = a.replace('month', 'M')
        a = a.replace('a week', '1 wk')
        a = a.replace('weeks', 'wk')
        a = a.replace('week', 'wk')
        a = a.replace('a year', '1 ')
        a = a.replace('years', 'yr')
        a = a.replace('year', 'yr')
        a = a.replace('ago', '')
        return a

    @hybrid_method
    def getDistance(self, loc, distanceMeters):
        if ',' not in self.latLon:
            return False
        if ',' in self.latLon:
            uLat = float(loc.split(',')[0])
        uLon = float(loc.split(',')[1])
        cLat = float(self.latLon.split(',')[0])
        cLon = float(self.latLon.split(',')[1])
        dist = getDistanceFromLatLonInKm(float(uLat), float(uLon), float(cLat), float(cLon))
        print dist
        if float(dist) <= distanceMeters:
            return True
        else:
            return False

    @hybrid_method
    def getWScore(self, loc):
        l = int(self.get_likes()) + 1
        t = 1000000000
        if self.atTime is not None:
            td = datetime.now() - self.atTime
            t = td.total_seconds()
        d = 100000000
        if ',' in self.latLon:
            uLat = float(loc.split(',')[0])
            uLon = float(loc.split(',')[1])
            cLat = float(self.latLon.split(',')[0])
            cLon = float(self.latLon.split(',')[1])
            d = getDistanceFromLatLonInKm(float(uLat), float(uLon), float(cLat), float(cLon))
        print t
        print d
        score = np.exp(-5e-06 * t) * 10000000 * (np.exp(-5e-05 * d) * 10000000) * l
        return score

    def createAddressString(self):
        if self.locationAddress is not None:
            print 'This is the location'
            if self.locationAddress != '@Yale University':
                print self.locationAddress
                return
            if self.locationAddress != 'Yale University':
                print self.locationAddress
                return
        print "No location. Let's create one"
        if self.latLon is not None:
            address = geolocator.reverse(self.latLon)
            if address is not None:
                simpleStreet = str(address[0][0]).split(',')[0]
                if simpleStreet == 'Yale University':
                    simpleStreet = str(address[0][0]).split(',')[1]
                locString = simpleStreet
                self.locationAddress = locString
                db.session.commit()
            else:
                print 'There was an error creating the street address'
                return
        else:
            print 'The Lat-Lon value is nil'
            return





class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    reply_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    typeNum = db.Column(db.Integer, default=1)#5 - request connection|6 - confirm connection| 7 - recieved message
    atTime = db.Column(db.DateTime)
    latLon = db.Column(db.String())

    def getAtTime(self):
        a = arrow.get(self.atTime)
        return a.humanize()

    def get_time_since(self):
        a = arrow.get(self.atTime)
        return a.humanize()

    def setPosition(self, lat, lon):
        foo = str(lat + ',' + lon)
        self.latLon = foo




class Hashtag(db.Model):
    __tablename__ = 'hashtag'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(120), index=True)
    user_owners = db.relationship('User', secondary=hashtagOwners, primaryjoin=hashtagOwners.c.hash_id == id, backref=db.backref('hashtags', lazy='dynamic'), lazy='dynamic')
    strong_relatives = db.relationship('Hashtag', secondary=strong_hashtag_connection, primaryjoin=strong_hashtag_connection.c.parent_id == id, secondaryjoin=strong_hashtag_connection.c.child_id == id, backref=db.backref('strongRelatives', lazy='dynamic'), lazy='dynamic')
    weak_relatives = db.relationship('User', secondary=weak_hashtag_connection, primaryjoin=weak_hashtag_connection.c.parent_id == id, secondaryjoin=weak_hashtag_connection.c.child_id == id, backref=db.backref('weakRelatives', lazy='dynamic'), lazy='dynamic')

    def add_user(self, user):
        if self.does_have_user(user) is False:
            self.user_owners.append(user)
            return self

    def remove_user(self, user):
        if self.does_have_user(user) is True:
            self.user_owners.remove(user)
            return self

    def does_have_user(self, user):
        if self.user_owners.filter(hashtagOwners.c.user_id == user.id).count() > 0:
            return True
        else:
            return False


units = ['',
 'one',
 'two',
 'three',
 'four',
 'five',
 'six',
 'seven',
 'eight',
 'nine ']
teens = ['',
 'eleven',
 'twelve',
 'thirteen',
 'fourteen',
 'fifteen',
 'sixteen',
 'seventeen',
 'eighteen',
 'nineteen']
tens = ['',
 'ten',
 'twenty',
 'thirty',
 'forty',
 'fifty',
 'sixty',
 'seventy',
 'eighty',
 'ninety']
thousands = ['',
 'thousand',
 'million',
 'billion',
 'trillion',
 'quadrillion',
 'quintillion',
 'sextillion',
 'septillion',
 'octillion',
 'nonillion',
 'decillion',
 'undecillion',
 'duodecillion',
 'tredecillion',
 'quattuordecillion',
 'sexdecillion',
 'septendecillion',
 'octodecillion',
 'novemdecillion',
 'vigintillion ']

def numToWords(num):
    words = []
    if num == 0:
        words.append('zero')
    else:
        numStr = '%d' % num
        numStrLen = len(numStr)
        groups = (numStrLen + 2) / 3
        numStr = numStr.zfill(groups * 3)
        for i in range(0, groups * 3, 3):
            h = int(numStr[i])
            t = int(numStr[i + 1])
            u = int(numStr[i + 2])
            g = groups - (i / 3 + 1)
            if h >= 1:
                words.append(units[h])
                words.append('hundred')
            if t > 1:
                words.append(tens[t])
                if u >= 1:
                    words.append(units[u])
            elif t == 1:
                if u >= 1:
                    words.append(teens[u])
                else:
                    words.append(tens[t])
            elif u >= 1:
                words.append(units[u])
            if g >= 1 and h + t + u > 0:
                words.append(thousands[g])

    str = ''
    for w in words:
        if w != words[0]:
            str += ' '
        str += w

    return str



def getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2):
    R = 6371
    dLat = deg2rad(lat2 - lat1)
    dLon = deg2rad(lon2 - lon1)
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c * 1000.0
    return d


def deg2rad(deg):
    return deg * (math.pi / 180)