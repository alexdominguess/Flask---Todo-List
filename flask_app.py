from flask import Flask, render_template, request, redirect, session
from login_functions import add_acount, login, recupera_senha, alterar_senha
from db_functions import get_data, update_data
from send_email import send_email


app= Flask(__name__)
app.secret_key = "Nj!fxX<LI=[$\\}3,^`j];vS4-%De!;k0n9MQze7I&_4gLcERq[!|yS]XCTRdblocQ=*)Rz"

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        email = request.form.get("email")
        pwd = request.form.get("pwd")
        if len(email) == 0 or len(pwd) == 0:
            return render_template("index.html", message = "Email ou Password não preenchido")
        login_msg = login(email, pwd)#function to validate user
        if login_msg != "sucess":
            return render_template("index.html", message = login_msg)
        else:
            session["user"] = email
            return redirect("todo")
    if request.method == "GET":
        return render_template ("index.html")


@app.route("/todo", methods = ["GET", "POST"])
def todo_list():
    try:
        if session["user"]:
            sql = "SELECT * FROM tarefas WHERE email = "+ "'" + session["user"] + "'"
            tarefas = get_data(sql)
            return render_template("todo.html", tarefas=tarefas, user=session["user"])
    except:
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
        new_password = recupera_senha(user_email)
        if new_password == "Email não cadastrado":
            return render_template ("recuperarsenha.html", message = "Email não cadastrado")
        else:
            subject = 'Senha Recuperada'
            msg = 'Aqui esta sua senha sua nova senha - ' + new_password
            send_email(user_email, subject, msg)
            return render_template ("recuperarsenha.html", message = "Nova senha enviada")
    else:
        return render_template ("recuperarsenha.html")


@app.route("/add_tarefa", methods = ["POST"])

def add_tarefa():
    #gets tarefa from the form and add to db
    tarefa = request.form.get("tarefa")
    email = session["user"]
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


@app.route("/mudar_senha", methods = ["GET","POST"])
def mudar_senha():
    if request.method == "GET":
        try:
            if session["user"]:
                return render_template("mudar_senha.html", user=session["user"])
        except:
            return redirect("/")
    else:
        pwd_atual = request.form.get("password_atual")
        pwd_novo_1 = request.form.get("novo_password_1")
        pwd_novo_2 = request.form.get("novo_password_2")

        result = alterar_senha(session["user"], pwd_atual, pwd_novo_1, pwd_novo_2)
        return render_template("mudar_senha.html", user=session["user"], message= result)


if __name__ == '__main__':
    app.run()
    