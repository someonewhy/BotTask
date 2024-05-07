import psycopg2
# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname="название базы данных",
    user="пользователь",
    password="пароль",
    host="хост",
    port="порт"
)
cursor = conn.cursor()