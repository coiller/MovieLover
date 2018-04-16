import json
import time
import tornado
from Handlers.BaseHandler import BaseHandler
class PaymentHandler(BaseHandler):
    def get(self,show_id):
        user_id=self.get_current_user()
        if not user_id:
            self.redirect('/login?back='+self.request.uri)
            return
        username=self.get_username()
        cur=self.cur
        show_id=int(show_id)
        detail=self.get_show_detail(show_id)
        r=cur.execute(
            ("select seat,reserve_time from seats where show_id=%s and user_id=%s" + \
                " and TIMESTAMPDIFF(second,reserve_time,current_timestamp())<5*60 and payment_id is null;") % (show_id,int(user_id)))
        if r!=0:
            re=cur.fetchall()
            seats=[r[0] for r in re]
            start=min([r[1] for r in re]).timestamp()*1000
            self.render('payment.html',detail=detail,seats=self.format_seats(seats),start=start,error="unfinish",username=username)
            return
        seats = json.loads(self.get_query_argument('seats'))
        data=[]
        for seat in seats:
            data.append(tuple([user_id,seat,show_id]))
        tmp="seat in "+str(tuple(seats))
        if len(seats)==1:
            tmp="seat='%s'" % seats[0]
        start=int(round(time.time() * 1000))
        self.db.begin()
        cur.execute("lock table seats write")
        r=cur.execute(
            "select 1 from seats where show_id="+ str(show_id)+" and "+ tmp+ \
            " and (TIMESTAMPDIFF(second,reserve_time,current_timestamp())<5*60 or payment_id is not null);")
        if r==0:
            r=cur.executemany(
                "insert into seats(user_id,seat,show_id) values (%s,%s,%s)",data)    
            if r==len(seats):
                cur.execute('unlock tables')
                self.db.commit()
                self.render('payment.html',detail=detail,seats=self.format_seats(seats),start=start,error=None,username=username)
                return
        self.db.rollback()
        cur.execute('unlock tables')
        self.db.commit()
        error='seats taken'
        self.render('payment.html',detail=detail,seats=self.format_seats(seats),error=error,start=None,username=username)
        

    def post(self,show_id):
        user_id=self.get_current_user()
        if not user_id:
            self.redirect('/login?back='+self.request.uri)
            return
        show_id=int(show_id)
        username=self.get_username()
        cur=self.cur
        seats = json.loads(self.get_query_argument('seats'))
        tmp="seat in "+str(tuple(seats))
        if len(seats)==1:
            tmp="seat='%s'" % seats[0]

        detail=self.get_show_detail(show_id)
        self.db.begin()
        sql=("select 1 from seats where show_id=%s and user_id=%s and %s"+\
             " and TIMESTAMPDIFF(second,reserve_time,current_timestamp())<5*60 and payment_id is null;") \
           % (show_id,int(user_id),tmp)
        r=cur.execute(sql)
        if r!=len(seats):
            raise tornado.web.HTTPError(404)
            return
        cur.execute(
            "insert into payment(user_id,amount) value (%s,%s)" % \
                (int(user_id),len(seats)*9)
            )      
        cur.execute(
            "update seats set payment_id=%s where show_id=%s and user_id=%s and %s"\
                % (self.db.insert_id(),show_id,int(user_id),tmp)
            )
        self.db.commit()
        self.render('success.html',detail=detail,seats=seats,username=username)

    def format_seats(self,seats):
        for seat in seats:
            tmp=seat.split('_')
            seat='Row %s No. %s' % (seat[0],seat[1])
        return seats