######################################
# Time:2020/02/07
# alter: ZWQ
######################################

from ADAM.user.urls import user_mold
from ADAM.task.urls import task_mold
from common import create_app

app = create_app()
app.register_blueprint(user_mold, url_prefix='/user')
app.register_blueprint(task_mold, url_prefix='/task')

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8080)