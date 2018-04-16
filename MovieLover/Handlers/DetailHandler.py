from Handlers.BaseHandler import BaseHandler
class DetailHandler(BaseHandler):
    def get(self,show_id):
        cur=self.cur
        username=self.get_username()
        sql='''select poster,show_id,description,show_time,length,rating,film.film_id 
        from on_show,film 
        where 
        show_id=%s and on_show.film_id=film.film_id
        '''% show_id
        cur.execute(sql)
        detail=cur.fetchone()
        cur.execute('''select concat(first_name," ",last_name) 
        from actor a,film_actor f 
        where film_id=%s and a.actor_id=f.actor_id'''% detail[6])
        actors=cur.fetchall()
        self.render('detail.html',username=username,detail=detail,actors=actors)

