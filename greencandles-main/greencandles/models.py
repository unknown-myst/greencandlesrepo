from datetime import datetime
from greencandles import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    # watchlist = db.Column(db.String(100),nullable=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
class Stockbasics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10))
    country = db.Column(db.String(100))
    company = db.Column(db.String(100))
    def __repr__(self):
        return f"Stock(symbol='{self.symbol}', country='{self.country}', company='{self.company}')"
    

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10))
    longName = db.Column(db.String(100))
    sector = db.Column(db.String(100))
    website = db.Column(db.String(100))
    address1 = db.Column(db.String(100))
    address2 = db.Column(db.String(100))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    zip = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    fullTimeEmployees = db.Column(db.Integer)
    longBusinessSummary = db.Column(db.Text)
    totalCash = db.Column(db.Float)
    totalDebt = db.Column(db.Float)
    totalRevenue = db.Column(db.Float)
    currentPrice = db.Column(db.Float)
    marketCap = db.Column(db.Float)
    open = db.Column(db.Float)
    dayLow = db.Column(db.Float)
    dayHigh = db.Column(db.Float)
    previousClose = db.Column(db.Float)
    fiftyTwoWeekHigh = db.Column(db.Float)
    fiftyTwoWeekLow = db.Column(db.Float)
    fiftyTwoWeekChange = db.Column(db.Float)
    fiftyDayAverage = db.Column(db.Float)
    twoHundredDayAverage = db.Column(db.Float)
    overallRisk = db.Column(db.String(100))
    recommendationKey = db.Column(db.String(100))
    volume = db.Column(db.Integer)
    averageVolume = db.Column(db.Integer)
    returnOnEquity = db.Column(db.Float)
    returnOnAssets = db.Column(db.Float)
    pegRatio = db.Column(db.Float)
    priceToBook = db.Column(db.Float)
    trailingEps = db.Column(db.Float)
    revenuePerShare = db.Column(db.Float)
    totalCashPerShare = db.Column(db.Float)
    symbol = db.Column(db.String(10))
    country = db.Column(db.String(100))
    company = db.Column(db.String(100))
    lastDateModified = db.Column(db.DateTime, default=None)

    def __repr__(self):
        return f"Stock('{self.longName}', '{self.symbol}')"