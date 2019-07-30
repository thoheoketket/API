import mysql.connector
from datetime import datetime
from .checkinput import *

mydb=mysql.connector.connect(
    host="192.168.51.28",
    user="hiface",
    passwd="Tinhvan@123",
    database="faceid"
)
mycursor = mydb.cursor() 


class general_query:


    @staticmethod
    def count_all_workdays(sdate,edate):
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
                    max(photoID) as IDphoto 
                    from 
                    monitor 
                    GROUP by 
                    name
                ) as N 
                where 
                M.name = N.name
            """
            val=(sdate,edate)
            mycursor.execute(sql,val)
            myresult=mycursor.fetchall()
            return myresult

    @staticmethod
    def count_all_absences(sdate,edate):
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
                    max(photoID) as IDphoto 
                    from 
                    monitor
                    group by name
                ) as N 
                where 
                M.name = N.name
            """
            val=(sdate,edate,sdate,edate,sdate,edate)
            mycursor.execute(sql,val)
            myresult=mycursor.fetchall()
            return myresult
        
    @staticmethod        
    def show_days_of_absences(sdate,edate):
        '''in ra các ngày vắng mặt của từng người kèm theo thứ của ngày hôm đó'''
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
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
                """
            val=(sdate,edate,sdate,edate,sdate,edate)
            mycursor.execute(sql,val)
            myresult=mycursor.fetchall()
            return myresult

    @staticmethod
    def count_OTdays(sdate,edate):
        sql="""
            SELECT 
            Z.name, 
            Z.day, 
            monitor.photoID 
            from 
            (
                SELECT 
                X.name, 
                X.day, 
                X.gioden, 
                X.giove 
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
                    group by 
                    name, 
                    day
                ) As X 
                where 
                (
                    (
                    DAYOFWEEK(X.day)<> 1 
                    and DAYOFWEEK(X.day)<> 7
                    ) 
                    and (
                    HOUR(X.giove)> 17 
                    OR (
                        MINUTE(X.giove)> 30 
                        AND HOUR(X.giove)= 17
                    )
                    )
                ) 
                OR DAYOFWEEK(X.day)= 1 
                OR DAYOFWEEK(X.day)= 7
            ) as Z, 
            monitor 
            WHERE 
            Z.name = monitor.name
        """
        val=(sdate,edate)
        mycursor.execute(sql,val)
        myresult=mycursor.fetchall()
        return myresult

       




