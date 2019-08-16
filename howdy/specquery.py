import mysql.connector
from datetime import datetime
from .checkinput import *


class SpecificQuery:

    def __init__(self):
        self.mydb=mysql.connector.connect(
            host="192.168.51.28",
            user="hiface",
            passwd="Tinhvan@123",
            database="faceid"
        )
        self.mycursor = self.mydb.cursor() 
    
    def close_connect(self):
        self.mycursor.close()
        self.mydb.close()
   
    def get_photoID(self,name,sdate,edate):
        sql="""
            SELECT name, min(photoID)
            FROM monitor 
            WHERE 
                datetime >= %s
                AND datetime < %s
                AND name = %s
        """
        val=(sdate,edate,name)
        self.mycursor.execute(sql,val)
        myresults=self.mycursor.fetchall()
        return myresults[0][1]
   
    def show_workdays(self,name,sdate,edate):
        '''các ngày đi làm của một người'''
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
                SELECT
                    name,
                    DATE(datetime) as day,
                    min(datetime) as arrivaltime,
                    max(datetime) as closingtime
                FROM
                    monitor
                WHERE
                    datetime >= %s
                    AND datetime < %s
                    AND name = %s
                group by
                    day
                """
            val=(sdate,edate,name)
            self.mycursor.execute(sql,val)
            myresult=self.mycursor.fetchall()
            return myresult

    def count_lateworking_days(self,name,sdate,edate):
        '''đếm các ngày đến muộn sau thời gian quy định'''
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
                    SELECT
                        M.name,
                        count(M.day) as latedays
                    from
                    (
                        SELECT
                        name,
                        DATE(datetime) as day,
                        min(datetime) as gioden,
                        max(datetime) as giove
                        FROM
                        monitor
                        WHERE
                        datetime >= %s
                        AND datetime < %s
                        AND name=%s
                        group by
                        day
                    ) As M,
                    (
                        SELECT
                        E.name,
                        X.start_time,
                        X.end_time,
                        X.lunch_start,
                        X.lunch_end
                        FROM
                        employee as E,
                        (
                            SELECT
                            department.id,
                            work_time.start_time,
                            work_time.end_time,
                            work_time.lunch_start,
                            work_time.lunch_end
                            FROM
                            department,
                            work_time
                            WHERE
                            department.id_work_time = work_time.id
                        ) as X
                        where
                        X.id = E.id_depart
                    ) as N
                    where
                        M.name = N.name
                        and ((TIME(M.gioden)> N.start_time and TIME(M.gioden)<=N.lunch_start)
                        or (TIME(M.gioden)>N.lunch_end and TIME(M.giove)<N.end_time))
                    GROUP by M.name
            """
            val=(sdate,edate,name)
            self.mycursor.execute(sql,val)
            myresult=self.mycursor.fetchall()
            return myresult       
   
    def show_lateday(self,name,sdate,edate):
        '''in ra các ngày đến muộn của một người'''
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
                SELECT
                    M.name,
                    M.day as lateday
                from
                (
                    SELECT
                    name,
                    DATE(datetime) as day,
                    min(datetime) as gioden,
                    max(datetime) as giove
                    FROM
                    monitor
                    WHERE
                    datetime >= %s
                    AND datetime < %s
                    AND name=%s
                    group by
                    day
                ) As M,
                (
                    SELECT
                    E.name,
                    X.start_time,
                    X.end_time,
                    X.lunch_start,
                    X.lunch_end
                    FROM
                    employee as E,
                    (
                        SELECT
                        department.id,
                        work_time.start_time,
                        work_time.end_time,
                        work_time.lunch_start,
                        work_time.lunch_end
                        FROM
                        department,
                        work_time
                        WHERE
                        department.id_work_time = work_time.id
                    ) as X
                    where
                    X.id = E.id_depart
                ) as N
                where
                    M.name = N.name
                    and ((TIME(M.gioden)> N.start_time and TIME(M.gioden)<=N.lunch_start)
                    or (TIME(M.gioden)>N.lunch_end and TIME(M.giove)<N.end_time))
            """
            val=(sdate,edate,name)
            self.mycursor.execute(sql,val)
            myresult=self.mycursor.fetchall()
            return myresult    

    def count_earlyworking_days(self,name,sdate,edate):
        '''đếm các ngày đến sớm trước thời gian quy định'''
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
                SELECT 
                M.name, 
                COUNT(M.day) as earlydays 
                from 
                (
                    SELECT 
                    name, 
                    DATE(datetime) as day, 
                    min(datetime) as gioden 
                    FROM 
                    monitor 
                    WHERE 
                    datetime >= %s
                    AND datetime < %s
                    AND name = %s
                    group by 
                    day
                ) As M, 
                (
                    SELECT 
                    E.name, 
                    X.start_time 
                    FROM 
                    employee as E, 
                    (
                        SELECT 
                        department.id, 
                        work_time.start_time 
                        FROM 
                        department, 
                        work_time 
                        WHERE 
                        department.id_work_time = work_time.id
                    ) as X 
                    where 
                    X.id = E.id_depart
                ) as N 
                where 
                M.name = N.name and TIME(M.gioden)< N.start_time 
                GROUP by name
            """
            val=(sdate,edate,name)
            self.mycursor.execute(sql,val)
            myresult=self.mycursor.fetchall()
            return myresult    

    def show_earlydays(self,name,sdate,edate):
        '''hiển thị các ngày đến sớm trước thời gian quy định'''
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
               SELECT 
                M.name, 
                M.day as earlyday
                from 
                (
                    SELECT 
                    name, 
                    DATE(datetime) as day, 
                    min(datetime) as gioden 
                    FROM 
                    monitor 
                    WHERE 
                    datetime >= %s
                    AND datetime < %s
                    AND name = %s
                    group by 
                    day
                ) As M, 
                (
                    SELECT 
                    E.name, 
                    X.start_time 
                    FROM 
                    employee as E, 
                    (
                        SELECT 
                        department.id, 
                        work_time.start_time 
                        FROM 
                        department, 
                        work_time 
                        WHERE 
                        department.id_work_time = work_time.id
                    ) as X 
                    where 
                    X.id = E.id_depart
                ) as N 
                where 
                M.name = N.name and TIME(M.gioden)< N.start_time 
            """
            val=(sdate,edate,name)
            self.mycursor.execute(sql,val)
            myresult=self.mycursor.fetchall()
            return myresult 
    
    def count_absent_days(self,name,sdate,edate):
        '''đếm các ngày vắng mặt không tính thứ 7, chủ nhật'''
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
                SELECT 
                    X.name, 
                    count(day) as earlyarrivaldays
                from 
                    (
                        SELECT 
                        name, 
                        DATE(datetime) as day, 
                        min(datetime) as arrivaltime, 
                        max(datetime) as closingtime 
                        FROM 
                        monitor 
                        WHERE 
                        datetime >= %s 
                        AND datetime < %s
                        AND name = %s
                        group by 
                        day
                    ) As X 
                where 
                    HOUR(X.arrivaltime)< 9 
                    OR (
                        MINUTE(X.arrivaltime)<= 5 
                        AND HOUR(X.arrivaltime)= 9
                    ) 
                GROUP by 
                    name
                """
            val=(sdate,edate,name)
            self.mycursor.execute(sql,val)
            myresult=self.mycursor.fetchall()
            return myresult    
  
    def count_working_days(self,name,sdate,edate):
        '''đếm các ngày đi làm không tính thứ 7, chủ nhật'''
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
                select
                    name,
                    count(X.day) as workingdays
                from
                    (
                        SELECT
                        name,
                        DATE(datetime) as day
                        FROM
                        monitor
                        WHERE
                        datetime >= %s
                        AND datetime < %s
                        AND name = %s
                        group by
                        day
                    ) as X
                where
                    DAYOFWEEK(X.day)<> 1
                    AND DAYOFWEEK(X.day)<> 7
                group by
                    X.name
                """
            val=(sdate,edate,name)
            self.mycursor.execute(sql,val)
            myresult=self.mycursor.fetchall()
            return myresult    

    def count_ot_days(self,name,sdate,edate):
        '''đếm các ngày làm thêm giờ tính thứ 7, chủ nhật'''
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
                SELECT
                M.name,
                count(M.day) as OTdays
                from
                (
                    SELECT
                    name,
                    DATE(datetime) as day,
                    min(datetime) as gioden,
                    max(datetime) as giove
                    FROM
                    monitor
                    WHERE
                    datetime >= %s
                    AND datetime < %s
                    and name=%s
                    group by
                    name,
                    day
                ) As M,
                (
                    SELECT
                    E.name,
                    X.start_time,
                    X.end_time
                    FROM
                    employee as E,
                    (
                        SELECT
                        department.id,
                        work_time.start_time,
                        work_time.end_time
                        FROM
                        department,
                        work_time
                        WHERE
                        department.id_work_time = work_time.id
                    ) as X
                    where
                    X.id = E.id_depart
                ) as N
                where
                    M.name = N.name
                    and ((TIME(M.gioden)<=N.start_time and TIME(M.giove)>N.end_time) or (DAYOFWEEK(M.day)=1 or DAYOFWEEK(M.day)=7))
                group by M.name
            """
            val=(sdate,edate,name)
            self.mycursor.execute(sql,val)
            myresult=self.mycursor.fetchall()
            return myresult    

    def show_ot_days(self,name,sdate,edate):
        '''in ra những ngày làm thêm giờ tính thứ 7, CN'''
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
                SELECT
                M.name,
                M.day as OTday
                from
                (
                    SELECT
                    name,
                    DATE(datetime) as day,
                    min(datetime) as gioden,
                    max(datetime) as giove
                    FROM
                    monitor
                    WHERE
                    datetime >= %s
                    AND datetime < %s
                    and name=%s
                    group by
                    name,
                    day
                ) As M,
                (
                    SELECT
                    E.name,
                    X.start_time,
                    X.end_time
                    FROM
                    employee as E,
                    (
                        SELECT
                        department.id,
                        work_time.start_time,
                        work_time.end_time
                        FROM
                        department,
                        work_time
                        WHERE
                        department.id_work_time = work_time.id
                    ) as X
                    where
                    X.id = E.id_depart
                ) as N
                where
                M.name = N.name
                and ((TIME(M.gioden)<=N.start_time and TIME(M.giove)>N.end_time) or (DAYOFWEEK(M.day)=1 or DAYOFWEEK(M.day)=7))
            """       
            val=(sdate,edate,name)
            self.mycursor.execute(sql,val)
            myresult=self.mycursor.fetchall()
            return myresult 

    def count_ot_hours(self,name,sdate,edate):
        '''số giờ làm thêm với ngày thường và thứ 7 chủ nhật tách riêng'''
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
                SELECT H.name, SEC_TO_TIME(sum(TIME_TO_SEC(ot_hour))) as ot_hours, 'weekend' as dayofweek
                from (SELECT
                    X.name,
                    X.day,
                    TIMEDIFF(X.giove,X.gioden) as ot_hour
                    FROM
                    (
                        select
                        name,
                        DATE(datetime) as day,
                        min(datetime) as gioden,
                        max(datetime) as giove
                        from
                        monitor
                        where
                        datetime >= %s
                        and datetime < %s
                        and name = %s
                        group by
                        name,
                        DATE(datetime)
                    ) as X
                    WHERE
                    DAYOFWEEK(X.day)= 1
                    OR DAYOFWEEK(X.day)= 7) as H
                GROUP by H.name
                UNION 
                SELECT K.name, SEC_TO_TIME(sum(TIME_TO_SEC(ot_hour))) as ot_hours, 'weekday' as dayofweek
                from (SELECT
                M.name,
                M.day as OTday,
                TIMEDIFF(TIME(M.giove),N.end_time) as ot_hour
                from
                (
                    SELECT
                    name,
                    DATE(datetime) as day,
                    min(datetime) as gioden,
                    max(datetime) as giove
                    FROM
                    monitor
                    WHERE
                    datetime >= %s
                    AND datetime < %s
                    and name=%s
                    group by
                    name,
                    day
                ) As M,
                (
                    SELECT
                    E.name,
                    X.start_time,
                    X.end_time
                    FROM
                    employee as E,
                    (
                        SELECT
                        department.id,
                        work_time.start_time,
                        work_time.end_time
                        FROM
                        department,
                        work_time
                        WHERE
                        department.id_work_time = work_time.id
                    ) as X
                    where
                    X.id = E.id_depart
                ) as N
                where
                M.name = N.name
                and TIME(M.gioden)<=N.start_time
                and TIME(M.giove)>N.end_time
                and DATE(M.gioden)!=1 and DATE(M.giove)!=7 ) as K
                group by K.name
            """
            val=(sdate,edate,name,sdate,edate,name)
            self.mycursor.execute(sql,val)
            myresult=self.mycursor.fetchall()
            return myresult

    def count_lackdays(self,name,sdate,edate):
        '''đếm các ngày làm thiếu công của một người: đến trước max_st hoặc về trước min_et'''
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
                SELECT
                    M.name, count(M.day) as lack_days
                from
                (
                    SELECT
                        name, DATE(datetime) as day, min(datetime) as gioden, max(datetime) as giove
                    FROM
                        monitor
                    WHERE
                        datetime >= %s AND datetime < %sand name=%s
                    group by
                        name, day
                ) As M,
                (
                    SELECT
                    E.name, X.max_st, X.min_et
                    FROM
                    employee as E,
                    (
                        SELECT
                            department.id, work_time.max_st, work_time.min_et
                        FROM
                            department, work_time
                        WHERE
                            department.id_work_time = work_time.id
                    ) as X
                    where
                        X.id = E.id_depart
                ) as N
                where
                    M.name = N.name and (TIME(M.gioden)> N.max_st or TIME(M.giove)<=N.min_et)
                GROUP by name
            """
            val=(sdate,edate,name)
            self.mycursor.execute(sql,val)
            myresult=self.mycursor.fetchall()
            return myresult

    def show_lackdays(self,name,sdate,edate):
        '''in các ngày làm thiếu công của một người: đến trước max_st hoặc về trước min_et'''
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
                SELECT
                M.name, M.day as lack_day
                from
                (
                    SELECT
                    name, DATE(datetime) as day,
                    min(datetime) as gioden, max(datetime) as giove
                    FROM
                    monitor
                    WHERE
                    datetime >= %s AND datetime < %sand name=%s
                    group by
                    name,
                    day
                ) As M,
                (
                    SELECT
                    E.name, X.max_st, X.min_et
                    FROM
                    employee as E,
                    (
                        SELECT
                            department.id, work_time.max_st, work_time.min_et
                        FROM
                            department, work_time
                        WHERE
                            department.id_work_time = work_time.id
                    ) as X
                    where
                        X.id = E.id_depart
                ) as N
                where
                    M.name = N.name and (TIME(M.gioden)> N.max_st or TIME(M.giove)<=N.min_et)
            """
            val=(sdate,edate,name)
            self.mycursor.execute(sql,val)
            myresult=self.mycursor.fetchall()
            return myresult
