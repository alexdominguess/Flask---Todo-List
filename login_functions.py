from datetime import datetime
from db_functions import get_data, update_data
from werkzeug.security import check_password_hash, generate_password_hash
import random
import string


def add_acount(email, pwd):
    sql = "SELECT email FROM accounts WHERE email = " + "'" + email + "'"
    result = get_data(sql)
    if len(result) == 0:
        time = datetime.now()
        pwd = generate_password_hash(pwd)
        sql = "INSERT INTO accounts(email, pwd, date_time) VALUES('{}','{}','{}')".format(email, pwd, time)
        update_data(sql)
        return "Cadastro realizado com sucesso"
    else:
        return "Email já cadastrado"


def login(email, pwd):
    sql = "SELECT email, pwd FROM accounts WHERE email = " + "'" + email + "'"
    result = get_data(sql)
    if len(result) == 0:
        return "Email não cadastrado"
    else:
        result = result[0]
        password = str(result[1])
        result = check_password_hash(password, pwd)
        if result == True:
            return "sucess"
        else:
            return "Senha inválida"


def recupera_senha(email):
    sql = "SELECT email, pwd FROM accounts WHERE email = " + "'" + email + "'"
    result = get_data(sql)
    if len(result) == 0:
        return "Email não cadastrado"
    else:
        randon_pwd = get_random_alphanumeric_string(10)
        new_pwd = generate_password_hash(randon_pwd)
        sql = "UPDATE accounts SET pwd='{}' WHERE email = '{}'".format(new_pwd, email)
        update_data(sql)
        return randon_pwd


def alterar_senha(email, pwd_atual, pwd_novo_1, pwd_novo_2):
    # check email and pwd
    result = login(email, pwd_atual)
    if result == "sucess":
        # check if new passords provided  match
        if pwd_novo_1 == pwd_novo_2:
            new_pwd = generate_password_hash(pwd_novo_1)
            sql = "UPDATE accounts SET pwd='{}' WHERE email = '{}'".format(new_pwd, email)
            update_data(sql)
            return "Password alterado com sucesso."
        else:
            return "Password novos são diferentes."
    else:
        return "Password atual é invalido."


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str


if __name__ == '__main__':
    pass
    # email = 'teste@teste'
    # pwd = '67890a'
    # login(email, pwd)
    # #add_acount(email, pwd)
    # #recuperar_senha(email)

    # conn = sqlite3.connect('data_base.db')
    # cursor = conn.cursor()
    # cursor.execute("CREATE TABLE tarefas (tarefa_id integer primary key, email text, tarefa text NOT NULL)")
    # conn.commit()
    # conn.close()
