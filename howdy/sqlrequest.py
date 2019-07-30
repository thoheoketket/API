from .jsontranform import *
from .generalquery import *
from .checkinput import *
from .specquery import *
# from generalquery import *
class SqlRequest:

    @staticmethod
    def reconnect():
        global mydb, mycursor
        mydb=mysql.connector.connect(
            host="192.168.51.28",
            user="hiface",
            passwd="Tinhvan@123",
            database="faceid"
        )
        mycursor = mydb.cursor() 

    @staticmethod
    def request_all(request_data):
        kind=request_data['kind']
        sdate= request_data['start_date']
        edate=request_data['end_date']
        if not DateChecker.check_logic_date(sdate,edate):
            return False, None
        kindof=int(kind)
        myresult=[]
        stringkey=''
        if kindof==1:
            x=general_query.count_all_workdays(sdate,edate)
            myresult=JsonTranform.transfrom(x,['name','appearances','photoID'],3)
        elif kindof==2:
            x=general_query.count_all_absences(sdate,edate)
            myresult=JsonTranform.transfrom(x,['name','absences','photoID'],3)
        else: 
            x=general_query.show_days_of_absences(sdate,edate)
            myresult=JsonTranform.transfrom(x,['name','absentday','dayofweek'],3)
        # else:
        #     x=general_query.count_OTdays(sdate,edate)
        #     myresult=JsonTranform.transfrom(x,['name','day','photoID'],3)
        return True, myresult
    
    @staticmethod
    def request_one(request_data):
        kind=request_data['kind']
        name = request_data['name']
        sdate= request_data['start_date']
        edate=request_data['end_date']
        if not DateChecker.check_logic_date(sdate,edate):
            return False, None
        results=[]
        kindof=int(kind)
        if kindof==1:
            y=specific_query.show_workdays(name,sdate,edate)
            listkey=['name','day','arrival_time','closing_time']
            results=JsonTranform.transfrom(y,listkey,len(listkey))   
        elif kindof==2 or kindof==3 or kindof==4 or kindof==5 or kindof==6:
            if kindof==2:
                y=specific_query.count_earlyworking_days(name,sdate,edate)
                stringkey='earlyworking_days'
            elif kindof==3:
                y=specific_query.count_lateworking_days(name,sdate,edate)
                stringkey='lateworking_days'
            elif kindof==4:
                y=specific_query.count_absent_days(name,sdate,edate)
                stringkey='absent_days'
            elif kindof==5:
                y=specific_query.count_working_days(name,sdate,edate)
                stringkey='working_days'
            elif kindof==6:
                y=specific_query.count_ot_days(name,sdate,edate)
                stringkey='OT_days'
            listkey=['name',stringkey]
            results=JsonTranform.transfrom(y,listkey,len(listkey))   
        elif kindof==7:
            y=specific_query.count_ot_hours(name,sdate,edate)
            for i in y:
                data['name']=i[0]
                data["OThoursof"+str(i[2])]=str(i[1])
            json_data=json.dumps(data,ensure_ascii=False)
            json_data_json=json.loads(json_data)
            results.append(json_data_json)
        else:
            y=specific_query.show_ot_days(name,sdate,edate)
            listkey=['name','OTday']
            results=JsonTranform.transfrom(y,listkey,len(listkey))   
        return True, results
       