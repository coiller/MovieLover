from Handlers.BaseHandler import BaseHandler
class MainHandler(BaseHandler):
    def get(self):
        cur=self.cur
        username=self.get_username()
        sql="select show_id,poster,title,length,rating,show_time from on_show,film where on_show.film_id=film.film_id;"
        r=cur.execute(sql)
        items=cur.fetchall()
        self.render('index.html',username=username,items=items)