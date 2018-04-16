import Settings
import tornado.escape
import pymysql
class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    @property
    def cur(self):
        # prepare a cursor object using cursor() method
        cursor = self.db.cursor()
        return cursor
    @property
    def sql_error(self):
        return pymysql.Error

    def get_username(self):
        user=self.get_current_user()
        cur=self.cur
        if not user:
            username=None
        else:
            cur.execute("select username from user where user_id=%s" % int(user))
            username=cur.fetchone()[0]
        return username

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")

    def get_show_detail(self,show_id):
        cur=self.cur
        r=cur.execute("select title,show_time,theater from film,on_show where film.film_id=on_show.film_id and show_id=%s;" % show_id)
        if r==0:
            raise tornado.web.HTTPError(404)
            self.finish()
        detail=cur.fetchone()
        return detail





