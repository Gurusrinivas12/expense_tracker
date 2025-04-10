from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(100))

    def __repr__(self):
        return f'<Expense {self.category} ₹{self.amount} on {self.date}>'

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(7), nullable=False)  # Format: YYYY-MM
    category = db.Column(db.String(50), nullable=False)
    limit = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Budget {self.category} ₹{self.limit} for {self.month}>'
