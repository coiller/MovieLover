import re
from Handlers.BaseHandler import BaseHandler
class SignUpHandler(BaseHandler):
    def get(self):
        self.render("signup.html",error=None)
    
    def post(self):
        username=self.get_argument('username','')
        email=self.get_argument('email')
        try:
            self.cur.execute("insert into user(username,password,email) values ('%s','%s','%s');"\
                % (username,self.get_argument('password'),email))
            self.db.commit()
        except self.sql_error as error:
            #check duplicate key?
            if error.args[0]==1062:
                error=re.findall(r"([A-Za-z]+)_UNIQUE",error.args[1])[0]
                self.render("signup.html",error='%s existed' % error.title())
            else:
                self.render("signup.html",error=str(error))
            return
        self.redirect("/login")
        

