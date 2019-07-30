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


class specific_query:
    
    
    @staticmethod
    def show_workdays(name,sdate,edate):
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
            mycursor.execute(sql,val)
            myresult=mycursor.fetchall()
            for i in myresult:
                print(i)
            return myresult

    @staticmethod
    def count_lateworking_days(name,sdate,edate):
        '''đếm các ngày đến muộn sau thời gian quy định'''
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
                SELECT 
                    X.name, 
                    count(day) as latearrivaldays
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
                    HOUR(X.arrivaltime)> 9 
                    OR (
                        MINUTE(X.arrivaltime)> 5 
                        AND HOUR(X.arrivaltime)= 9
                    ) 
                GROUP by 
                    name
                """
            val=(sdate,edate,name)
            mycursor.execute(sql,val)
            myresult=mycursor.fetchall()
            return myresult
        
    @staticmethod
    def count_earlyworking_days(name,sdate,edate):
        '''đếm các ngày đến sớm trước thời gian quy định'''
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
            mycursor.execute(sql,val)
            myresult=mycursor.fetchall()
            return myresult    

    @staticmethod
    def count_absent_days(name,sdate,edate):
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
            mycursor.execute(sql,val)
            myresult=mycursor.fetchall()
            return myresult    

    @staticmethod
    def count_working_days(name,sdate,edate):
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
            mycursor.execute(sql,val)
            myresult=mycursor.fetchall()
            return myresult    

    @staticmethod
    def count_ot_days(name,sdate,edate):
        '''đếm các ngày làm thêm giờ tính thứ 7, chủ nhật'''
        if DateChecker.check_logic_date(sdate,edate):
            sql="""
                SELECT
                    X.name,
                    count(X.day) as otdays
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
                    (
                        DAYOFWEEK(X.day)<> 1
                        and DAYOFWEEK(X.day)<> 7
                        )
                        and (
                        HOUR(X.closingtime)> 17
                        OR (
                            MINUTE(X.closingtime)> 30
                            AND HOUR(X.closingtime)= 17
                        )
                    )
                    OR DAYOFWEEK(X.day)= 1
                    OR DAYOFWEEK(X.day)= 7
                group by name
                """
            val=(sdate,edate,name)
            mycursor.execute(sql,val)
            myresult=mycursor.fetchall()
            return myresult    

    @staticmethod
    def count_ot_hours(name,sdate,edate):
        '''số giờ làm thêm với ngày thường và thứ 7 chủ nhật tách riêng'''
        sql="""
            SELECT
            Y.name,
            sum(Y.otminutes)/ 60 as totalOThour,
            'Weekend' as dayofweek
            from
            (
                SELECT
                X.name,
                X.day,
                X.arrivaltime,
                X.closingtime,
                (
                    (
                    HOUR(X.closingtime)- HOUR(X.arrivaltime)
                    )* 60 + (
                    MINUTE(X.closingtime)- MINUTE(X.arrivaltime)
                    )
                ) as otminutes
                FROM
                (
                    select
                    name,
                    DATE(datetime) as day,
                    min(datetime) as arrivaltime,
                    max(datetime) as closingtime
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
                OR DAYOFWEEK(X.day)= 7
            ) as Y
            GROUP by
            Y.name
            UNION
            select
            Y.name,
            sum(Y.otminutes)/ 60 as otminutes,
            'Weekday' as dayofweek
            from
            (
                SELECT
                X.name,
                X.day,
                X.arrivaltime,
                X.closingtime,
                (
                    HOUR(X.closingtime)-17
                )* 60 + MINUTE(X.closingtime)-30 as otminutes
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
                    name,
                    day
                ) As X
                where
                DAYOFWEEK(X.day)<> 1
                and DAYOFWEEK(X.day)<> 7
                and (
                    (
                    HOUR(X.closingtime)> 17
                    OR (
                        MINUTE(X.closingtime)> 30
                        AND HOUR(X.closingtime)= 17
                    )
                    )
                    and (
                    (
                        HOUR(X.arrivaltime)< 17
                    )
                    or (
                        MINUTE(X.arrivaltime)< 30
                        and HOUR(X.arrivaltime)= 17
                    )
                    )
                )
                UNION
                SELECT
                X.name,
                X.day,
                X.arrivaltime,
                X.closingtime,
                (
                    HOUR(X.closingtime)- HOUR(X.arrivaltime)
                )* 60 + MINUTE(X.closingtime)- MINUTE(X.arrivaltime) as otminutes
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
                    name,
                    day
                ) As X
                where
                DAYOFWEEK(X.day)<> 1
                and DAYOFWEEK(X.day)<> 7
                and (
                    (
                    HOUR(X.closingtime)> 17
                    OR (
                        MINUTE(X.closingtime)> 30
                        AND HOUR(X.closingtime)= 17
                    )
                    )
                    and (
                    (
                        HOUR(X.arrivaltime)> 17
                    )
                    or (
                        MINUTE(X.arrivaltime)> 30
                        and HOUR(X.arrivaltime)= 17
                    )
                    )
                )
            ) as Y
            group by
            name
        """
        val=(sdate,edate,name,sdate,edate,name,sdate,edate,name)
        mycursor.execute(sql,val)
        myresult=mycursor.fetchall()
        return myresult


    @staticmethod
    def show_ot_days(name,sdate,edate):
        '''in ra những ngày làm thêm giờ tính thứ 7, CN'''
        sql="""
            SELECT
            X.name,
            X.day
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
            (
                (
                DAYOFWEEK(X.day)<> 1
                and DAYOFWEEK(X.day)<> 7
                )
                and (
                HOUR(X.closingtime)> 17
                OR (
                    MINUTE(X.closingtime)> 30
                    AND HOUR(X.closingtime)= 17
                )
                )
            )
            OR DAYOFWEEK(X.day)= 1
            OR DAYOFWEEK(X.day)= 7   
        """       
        val=(sdate,edate,name)
        mycursor.execute(sql,val)
        myresult=mycursor.fetchall()
        return myresult 