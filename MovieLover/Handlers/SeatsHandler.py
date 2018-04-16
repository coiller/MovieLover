from Handlers.BaseHandler import BaseHandler
class SeatsHandler(BaseHandler):
    def get(self,show_id):
        show_id=int(show_id)
        detail=self.get_show_detail(show_id)
        username=self.get_username()
        cur=self.cur
        num=cur.execute('select seat from seats where show_id=%s and (TIMESTAMPDIFF(second,reserve_time,current_timestamp())<5*60 or payment_id is not null)'% show_id)
        if num==0:
            self.render("seats.html",show_id=show_id,reserved=[],detail=detail,username=username)
            return
        self.db.commit()
        reserved=[s[0] for s in cur.fetchall()]
        self.render("seats.html",show_id=show_id,reserved=reserved,detail=detail,username=username)
