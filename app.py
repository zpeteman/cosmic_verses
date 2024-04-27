# app.py
from flask import Flask, render_template, request
from static.data.model import poem_gen

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("screen_1.html")

@app.route("/free_users")
def fr_user():
    return render_template('index.html')

@app.route("/check_user")
def check_user():
    return render_template('check_user.html')

@app.route("/process_input", methods=["POST"])
def process_input():
  # Retrieve the input text from the form
  cosmic_line = request.form.get("cosmic_line")
  
  # Validate and process the input here (server-side)
  # ... your logic here ...
  
  # Based on the logic, redirect to different pages (optional)
  if cosmic_line == "Rime the cosmic quenne":
    return render_template("pre_index.html")
  else:
    error_message="رمز المستخدم غير صحيح"
    return render_template("check_user.html", error=error_message)

@app.route("/f_user")
def f_user():
   return render_template("f_user.html")

@app.route('/create_acc')
def acc():
   return render_template("premium_account.html")

@app.route("/generate_pm", methods=["POST"])
def generate_pm():
    # Retrieve the input text from the form submission
    input_text = request.form.get("cosmic_line", "")
    # Generate the poem based on the input text
    poem = poem_gen(input_text)
    # Render gen_pm.html with the generated poem displayed
    return render_template("gen_pm.html", poem=poem)

# Handler for 404 errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)

