from Handlers.BaseHandler import BaseHandler
class SeatsHandler(BaseHandler):
    def get(self,show_id):
        show_id=int(show_id)
        detail=self.get_show_detail(show_id)
        username=self.get_username()
        cur=self.cur
        num=cur.execute('select seat from seats group by seat order by count(*) desc limit 3')
        if num==0:pop=None
        else:
            pop=cur.fetchall()
            pop=[p[0] for p in pop]
            tmp=self.format_seats(pop)
            pop=" "
            for t in tmp:
                pop+=t+" | "
            pop=pop[:-3]
        num=cur.execute('select seat from seats where show_id=%s and (TIMESTAMPDIFF(second,reserve_time,current_timestamp())<5*60 or payment_id is not null)'% show_id)
        if num==0:
            self.render("seats.html",show_id=show_id,reserved=[],detail=detail,username=username,pop=pop)
            return
        reserved=[s[0] for s in cur.fetchall()]
        self.render("seats.html",show_id=show_id,reserved=reserved,detail=detail,username=username,pop=pop)
