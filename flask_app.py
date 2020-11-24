from flask import Flask, render_template, request, redirect
from login_functions import add_acount, login, recupera_senha
from db_functions import get_data, update_data
from send_email import send_email

app= Flask(__name__)
user = [""]

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        email = request.form.get("email")
        user[0] = email
        pwd = request.form.get("pwd")

        if len(email) == 0 or len(pwd) == 0:
            return render_template("index.html", message = "Email ou Password não preenchido")
        login_msg = login(email, pwd)#function to validate user
        if login_msg != "sucess":
            return render_template("index.html", message = login_msg)
        else:
            return redirect("todo")
    if request.method == "GET":
        user[0] = "" #Requires user to login every time login page is loaded
        
        return render_template ("index.html")


@app.route("/todo", methods = ["GET", "POST"])
def todo_list():
    if user[0] != "":
        sql = "SELECT * FROM tarefas WHERE email = "+ "'" + user[0] + "'"
        tarefas = get_data(sql)
        return render_template("todo.html", tarefas=tarefas, user=user[0])
    else:
        return redirect("/")


@app.route("/cadastrar", methods = ["GET", "POST"])
def cadastrar():
    if request.method == "GET":
        return render_template ("cadastrar.html")

    else:
        email = request.form.get("cad_email")
        pwd = request.form.get("cad_pwd")
        cad_masg = add_acount(email, pwd)
        return render_template("cadastrar.html", message = cad_masg)


@app.route("/recuperarsenha", methods = ["GET", "POST"])
def recuperar_senha():
    if request.method == "POST":
        user_email = request.form.get("rec_email")
        user_password = recupera_senha(user_email)
        if user_password == "Email não cadastrado":
            return render_template ("recuperarsenha.html", message = "Email não cadastrado")
        else:
            subject = 'Senha Recuperada'
            msg = 'Aqui esta sua senha - ' + user_password
            send_email(user_email, user_password, subject, msg)
            return render_template ("recuperarsenha.html", message = "Senha enviada")
    else:
        return render_template ("recuperarsenha.html")


@app.route("/add_tarefa", methods = ["POST"])
def add_tarefa():
    #gets tarefa from the form and add to the db
    tarefa = request.form.get("tarefa")
    email = user[0]
    sql = "INSERT INTO tarefas(email, tarefa) VALUES('{}','{}')".format(email, tarefa)
    update_data(sql)
    return redirect("todo")


@app.route("/completar_tarefa", methods = ["POST"])
def delete_tarefa():
    #gets the tarefa's id and delete from db
    tarefa_id = request.form.get("tarefa_id")
    sql = "DELETE FROM tarefas WHERE tarefa_id = {}".format(tarefa_id)
    update_data(sql)
    return redirect("todo")


if __name__ == '__main__':
    app.run()
    
