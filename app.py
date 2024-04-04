# imports
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# App Setup
app = Flask(__name__)
Scss(app)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


# Data Class == row of data
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    is_complete = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Task {self.id}"


# Routes to webpages
# Home Page
@app.route("/", methods=["POST", "GET"])
def index():
    # Add a task
    if request.method == "POST":
        # Grab the content
        current_task = request.form['content']
        # create instance of MyTask using content
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"

    # See all current tasks
    else:
        tasks = MyTask.query.order_by(MyTask.date_created).all()
        return render_template("index.html", tasks=tasks)
    

# Delete an item
@app.route("/delete/<int:id>")
def delete(id:int):
    task_to_delete = MyTask.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"ERROR:{e}")
        return f"ERROR:{e}"    


# Edit an item
@app.route("/update/<int:id>", methods = ["GET", "POST"])
def update(id:int):
    task_to_edit = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task_to_edit.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}" 
    else:
        return render_template("edit.html", task=task_to_edit)


# Run the app
if __name__ in "__main__":
    with app.app_context():
        db.create_all()


    app.run(debug=True)


