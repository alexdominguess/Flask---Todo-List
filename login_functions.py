import sqlite3
from datetime import datetime
from db_functions import get_data, update_data

def add_acount(email, pwd):
    sql = "SELECT email FROM accounts WHERE email = " + "'" + email + "'"
    result = get_data(sql)
    if len(result) == 0:
        time = datetime.now()
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
        if password == pwd:
            
            return "sucess"
        else:
            return "Senha inválida"

def recupera_senha(email):
    sql = "SELECT email, pwd FROM accounts WHERE email = " + "'" + email + "'"
    result = get_data(sql)
    if len(result) == 0:
        return "Email não cadastrado"
    else:
        result = result[0]
        user_email = result[0]
        user_password = result[1]
        #send password to email provided
        return user_password
        
        
        
    

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
