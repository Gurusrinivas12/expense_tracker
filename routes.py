from flask import Blueprint, request, jsonify
from models import db, Expense, Budget
from datetime import datetime
from utils import send_alert_email

routes = Blueprint('routes', __name__)

@routes.route('/expense', methods=['POST'])
def add_expense():
    data = request.json
    expense = Expense(
        category=data['category'],
        amount=data['amount'],
        description=data.get('description')
    )
    db.session.add(expense)
    db.session.commit()

    # Budget check
    today = datetime.today()
    month_str = today.strftime("%Y-%m")
    budget = Budget.query.filter_by(month=month_str, category=data['category']).first()
    if budget:
        total = db.session.query(db.func.sum(Expense.amount)).filter(
            db.func.strftime("%Y-%m", Expense.date) == month_str,
            Expense.category == data['category']
        ).scalar() or 0
        if total > budget.limit:
            send_alert_email(data['category'], month_str, 0)
        elif total > 0.9 * budget.limit:
            send_alert_email(data['category'], month_str, round(budget.limit - total, 2))

    return jsonify({"message": "Expense logged successfully"}), 201

@routes.route('/budget', methods=['POST'])
def set_budget():
    data = request.json
    month = data['month']
    category = data['category']
    limit = data['limit']

    existing = Budget.query.filter_by(month=month, category=category).first()
    if existing:
        existing.limit = limit
    else:
        budget = Budget(month=month, category=category, limit=limit)
        db.session.add(budget)
    db.session.commit()
    return jsonify({"message": "Budget set successfully"})

@routes.route('/report/<month>', methods=['GET'])
def report(month):
    # month format: "YYYY-MM"
    expenses = Expense.query.filter(
        db.func.strftime("%Y-%m", Expense.date) == month
    ).all()

    budgets = Budget.query.filter_by(month=month).all()

    report_data = {}

    for exp in expenses:
        cat = exp.category.lower()
        if cat not in report_data:
            report_data[cat] = {"spent": 0, "budget": "Not set", "exceeded": False}
        report_data[cat]["spent"] += exp.amount

    for bud in budgets:
        cat = bud.category.lower()
        if cat not in report_data:
            report_data[cat] = {"spent": 0, "budget": bud.limit, "exceeded": False}
        else:
            report_data[cat]["budget"] = bud.limit

        report_data[cat]["exceeded"] = report_data[cat]["spent"] > bud.limit

    return jsonify(report_data)
