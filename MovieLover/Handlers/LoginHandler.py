import Settings
import pymysql
from Handlers.BaseHandler import BaseHandler
class LoginHandler(BaseHandler):
    def get(self):
        try:
            error = self.get_argument("error",None)
        except:
            error= None
        self.render("login.html", error = None)

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        back =self.get_argument("back",'/')
        auth = self.check_permission(password, username)
        self.set_current_user(auth)
        if auth:
            self.redirect(back)


    def check_permission(self, password, username):
        if username == Settings.ADMIN_NM and password == Settings.ADMIN_PW:
            return Settings.ADMIN_ID
        try:
            cur=self.cur
            cur.execute("select user_id from user where username='%s' and password='%s';" %(username,password))
            u_id=cur.fetchone()
            return u_id
        except pymysql.Error as error:
            self.render("login.html", error ="Login invalid")
            return None