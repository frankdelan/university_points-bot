import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('TOKEN')

login_url = 'https://lk.volsu.ru/user/sign-in/login'
main_link = 'https://lk.volsu.ru/student/grade?id=0'

db = {
    'database': os.environ.get('DB_NAME'),
    'host': os.environ.get('HOST'),
    'user': os.environ.get('USER'),
    'password': os.environ.get('PASS'),
    'port': os.environ.get('PORT')
}
