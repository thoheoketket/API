import mysql.connector
from datetime import datetime
from .checkinput import *

# mydb=mysql.connector.connect(
#     host="192.168.51.28",
#     user="hiface",
#     passwd="Tinhvan@123",
#     database="faceid"
# )
# self.mycursor = mydb.cursor() 


class GeneralQuery:

    def __init__(self):
        self.mydb=mysql.connector.connect(
            host="192.168.51.28",
            user="hiface",
            passwd="Tinhvan@123",
            database="faceid"
        )
        self.mycursor = self.mydb.cursor() 
    
    def count_all_workdays(self,sdate,edate):
        '''số ngày đi làm tính cả thứ 7, chủ nhật của tất cả mọi người'''
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
                select 
                M.name, 
                M.appearances, 
                N.IDphoto 
                from 
                (
                    SELECT 
                    X.name, 
                    count(X.day) as appearances 
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
                        group by 
                        name, 
                        DATE(datetime)
                    ) as X 
                    GROUP by 
                    name
                ) as M, 
                (
                    select 
                    name, 
                    min(photoID) as IDphoto 
                    from 
                    monitor 
                    GROUP by 
                    name
                ) as N 
                where 
                M.name = N.name
            """
            val=(sdate,edate)
            self.mycursor.execute(sql,val)
            myresult=self.mycursor.fetchall()
            return myresult
   
    def count_all_absences(self,sdate,edate):
        '''đếm số ngày vắng không phải t7-cn của tất cả mọi người'''
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
                select 
                M.name, 
                M.tongngayvang, 
                N.IDphoto
                from 
                (
                    select 
                    name, 
                    count(T.day) as tongngayvang 
                    from 
                    (
                        select 
                        Z.name, 
                        Z.day, 
                        DAYNAME(Z.day) 
                        from 
                        (
                            select 
                            X.name, 
                            Y.day 
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
                                group by 
                                name, 
                                day
                            ) as X, 
                            (
                                SELECT 
                                DATE(datetime) as day 
                                FROM 
                                monitor 
                                WHERE 
                                datetime >= %s 
                                AND datetime < %s
                                group by 
                                day
                            ) as Y 
                            where 
                            X.day != Y.day 
                            and Y.day not in (
                                SELECT 
                                day 
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
                                    group by 
                                    name, 
                                    day
                                ) as X2 
                                where 
                                X2.name = X.name
                            ) 
                            GROUP by 
                            X.name, 
                            Y.day
                        ) as Z 
                        Where 
                        DAYOFWEEK(Z.day)<> 1 
                        and DAYOFWEEK(Z.day)<> 7
                    ) as T 
                    group by 
                    name
                ) as M, 
                (
                    select 
                    name, 
                    min(photoID) as IDphoto 
                    from 
                    monitor
                    group by name
                ) as N 
                where 
                M.name = N.name
            """
            val=(sdate,edate,sdate,edate,sdate,edate)
            self.mycursor.execute(sql,val)
            myresult=self.mycursor.fetchall()
            return myresult
           
    def count_OTdays(self,sdate,edate):
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
                SELECT
                    M.name,
                    count(M.day) as OTday,
                    min(M.IDphoto) as photoID
                from
                    (
                    SELECT
                        name,
                        DATE(datetime) as day,
                        min(datetime) as gioden,
                        max(datetime) as giove,
                        min(photoID) as IDphoto
                    FROM
                        monitor
                    WHERE
                        datetime >= %s
                        AND datetime < %s
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
                GROUP by name
            """
            val=(sdate,edate)
            self.mycursor.execute(sql,val)
            myresult=self.mycursor.fetchall()
            return myresult
   
    def count_latedays(self,sdate,edate):
        '''Đếm số ngày đến muộn của từng người'''
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
                SELECT
                    M.name,
                    count(M.day) as latedays,
                    min(M.IDphoto) as photoID
                from
                    (
                    SELECT
                        name,
                        DATE(datetime) as day,
                        min(datetime) as gioden,
                        max(datetime) as giove,
                        min(photoID) as IDphoto
                    FROM
                        monitor
                    WHERE
                        datetime >= %s
                        AND datetime < %s
                    group by
                        name,
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
                GROUP by name
            """
            val=(sdate,edate)
            self.mycursor.execute(sql,val)
            myresult=self.mycursor.fetchall()
            return myresult

    def count_lackdays(self,sdate,edate):
        '''Đếm số ngày làm thiếu giờ của một người'''
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
                SELECT
                M.name,
                count(M.day) as lack_days,
                min(M.IDphoto) as photoID
                from
                (
                    SELECT
                    name,
                    DATE(datetime) as day,
                    min(datetime) as gioden,
                    max(datetime) as giove,
                    min(photoID) as IDphoto
                    FROM
                    monitor
                    WHERE
                    datetime >= %s
                    AND datetime < %s
                    group by
                    name,
                    day
                ) As M,
                (
                    SELECT
                    E.name,
                    X.start_time,
                    X.end_time,
                    X.max_st,
                    X.min_et
                    FROM
                    employee as E,
                    (
                        SELECT
                        department.id,
                        work_time.start_time,
                        work_time.end_time,
                        work_time.max_st,
                        work_time.min_et
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
                and
                (TIME(M.gioden)> N.max_st
                or TIME(M.giove)<=N.min_et)
                GROUP by name
            """
            val=(sdate,edate)
            self.mycursor.execute(sql,val)
            myresult=self.mycursor.fetchall()
            return myresult

    def count_lunchtime(self,sdate,edate):
        '''đếm các ngày đi ăn trưa trong khoảng 11:30 đến 12:30 của mọi người'''
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
                SELECT T.name,
                    COUNT(T.lunch_time) as days,
                    MIN(T.IDphoto) as IDphoto
                from (SELECT
                    M.name,
                    DATE(M.datetime) as day,
                    max(M.datetime) as lunch_time,
                    MIN(M.photoID) as IDphoto
                    FROM
                        monitor as M, 
                        (SELECT
                            E.name,
                            X.start_time,
                            X.lunch_start,
                            X.lunch_end
                            FROM
                                employee as E,
                                (
                                    SELECT
                                    department.id,
                                    work_time.start_time,
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
                    WHERE
                    M.name=N.name 
                    and M.datetime >= %s
                    AND M.datetime < %s
                    and TIME(M.datetime)>=N.start_time
                    and TIME(M.datetime)<=N.lunch_start
                    and TIME(M.datetime)>=TIME('11:30:00')
                    and TIME(M.datetime)<=TIME('12:30:00')
                    group by
                    M.name,
                    DATE(M.datetime)
                ) as T
                GROUP by name
            """
            val=(sdate,edate)
            self.mycursor.execute(sql,val)
            myresult=self.mycursor.fetchall()
            return myresult

    def count_by_day(self,sdate,edate):
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
                SELECT Z.day,  K.numbers,Z.late
                from (SELECT 
                    M.day,count(M.name) as late
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
                        group by
                        name,
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
                        and ((TIME(M.gioden)> N.start_time
                        and TIME(M.gioden)<=N.lunch_start)
                        or (TIME(M.gioden)>N.lunch_end and TIME(gioden)<N.end_time))
                    GROUP by M.day
                ) as Z
                INNER JOIN
                ( SELECT 
                    X.day, COUNT(X.name) as numbers 
                    from 
                    (
                        SELECT 
                            name, DATE(datetime) as day 
                        FROM monitor 
                        WHERE 
                            datetime >= %s AND datetime < %s
                            group by name, day
                    ) as X 
                    GROUP by X.day
                ) as K
                ON Z.day = K.day
            """
            val=(sdate,edate,sdate,edate)
            self.mycursor.execute(sql,val)
            myresult=self.mycursor.fetchall()
            return myresult


