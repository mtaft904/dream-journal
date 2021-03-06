import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


def format_order(order):
    if order:
        return "Newest"
    else:
        return "Oldest"


app = Flask(__name__)
app.config["SECRET_KEY"] = "ziopn4rlsdfu983n"


newest_first = True


@app.route("/", methods=("GET", "POST"))
def home():
    global newest_first
    if request.method == "POST":
        newest_first = not newest_first
    order = newest_first
    conn = get_db_connection()
    if newest_first:
        posts = conn.execute("SELECT * FROM posts ORDER BY created DESC").fetchall()
    else:
        posts = conn.execute("SELECT * FROM posts").fetchall()
    conn.close()
    return render_template("home.html", posts=posts, order=format_order(order))


@app.route("/<int:post_id>")
def post(post_id):
    post = get_post(post_id)
    return render_template("post.html", post=post)


@app.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        if not title:
            flash("Title is required!")
        else:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO posts (title, content) VALUES (?, ?)", (title, content)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("home"))

    return render_template("create.html")


@app.route("/<int:post_id>/delete", methods=["POST"])
def delete(post_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM posts WHERE id = ? ", (post_id,))
    conn.commit()
    conn.close()
    flash("Successfully deleted post!")

    return redirect(url_for("home"))


@app.route("/<int:post_id>/edit", methods=["GET", "POST"])
def edit(post_id):
    post = get_post(post_id)
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        conn = get_db_connection()
        conn.execute(
            "UPDATE posts SET (title, content) = (?, ?) WHERE id = ?",
            (title, content, post_id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("post", post_id=post_id))

    return render_template("edit.html", post=post)
