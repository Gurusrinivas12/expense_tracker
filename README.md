Expense Tracker App
A Flask-based Python application to help users track daily expenses, set monthly category budgets, receive alerts, and generate reports.

Features
Log daily expenses with categories like Food, Transport, Entertainment

Set monthly budgets per category

Alert when spending exceeds 90% or goes over budget

Monthly spending reports

Email notifications for budget alerts

How to Run
1. Clone the repo
bash
Copy
Edit
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker
2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Run the app
bash
Copy
Edit
python app.py
The server will run at http://127.0.0.1:5000/

Test Steps
Add Expense
http
Copy
Edit
POST /expense
Content-Type: application/json

{
  "category": "Food",
  "amount": 200,
  "description": "Lunch"
}
Set Budget

POST /budget
Content-Type: application/json

{
  "month": "2025-04",
  "category": "Food",
  "limit": 3000
}
Get Monthly Report

GET /report/2025-04
SQL / ORM
ORM: Flask-SQLAlchemy

Tables: Expense, Budget

Docker Build and Run
Build the image

docker build -t expense-tracker .
Run the container

docker run -p 5000:5000 expense-tracker
Notes
Configure email credentials in utils.py securely using environment variables.

Edge case handled: Alert if expense exceeds 90% of the budget.

The application can be extended to support group expense sharing in the future.

