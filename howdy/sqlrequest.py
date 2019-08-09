from .jsontranform import *
from .generalquery import *
from .checkinput import *
from .specquery import *
# from query_general import *
class SqlRequest:

    # def __init__(self):
    #     mydb=mysql.connector.connect(
    #         host="192.168.51.28",
    #         user="hiface",
    #         passwd="Tinhvan@123",
    #         database="faceid"
    #     )
    #     mycursor = mydb.cursor() 

    # @staticmethod
    # def reconnect():
    #     global mydb, mycursor
    #     mydb=mysql.connector.connect(
    #         host="192.168.51.28",
    #         user="hiface",
    #         passwd="Tinhvan@123",
    #         database="faceid"
    #     )
    #     mycursor = mydb.cursor() 

    def request_all(self,request_data):
        kind=request_data['kind']
        sdate= request_data['start_date']
        edate=request_data['end_date']
        if not DateChecker.check_logic_date(sdate,edate):
            return False, None
        kindof=int(kind)
        myresult=[]
        try:
            query_general=GeneralQuery()
        except:
            query_general.__init__()
        if kindof==1:
            x=query_general.count_all_workdays(sdate,edate)
            myresult=JsonTranform.transfrom(x,['name','appearances','photoID'],3)
        elif kindof==2:
            x=query_general.count_all_absences(sdate,edate)
            myresult=JsonTranform.transfrom(x,['name','absences','photoID'],3)
        elif kindof==3:
            x=query_general.count_OTdays(sdate,edate)
            myresult=JsonTranform.transfrom(x,['name','OT_days','photoID'],3)
        elif kindof==4:
            x=query_general.count_latedays(sdate,edate)
            myresult=JsonTranform.transfrom(x,['name','late_days','photoID'],3)
        else:
            x=query_general.count_by_day(sdate,edate)
            myresult=JsonTranform.transfrom(x,['day','numbers','late'],3)
        return True, myresult
    
    def request_one(self,request_data):
        kind=request_data['kind']
        name = request_data['name']
        sdate= request_data['start_date']
        edate=request_data['end_date']
        if not DateChecker.check_logic_date(sdate,edate):
            return False, None
        kindof=int(kind)
        string_key=''
        try:
            specific_query=SpecificQuery()
        except:
            specific_query.__init__()
        IDphoto=specific_query.get_photoID(name,sdate,edate)
        if kindof==1:
            y=specific_query.show_workdays(name,sdate,edate)
            listkey=['name','day','arrival_time','closing_time']
            results=JsonTranform.transfrom(y,listkey,len(listkey),IDphoto)   
        elif kindof==2 or kindof==3 or kindof==4 or kindof==5 or kindof==6:
            if kindof==2:
                y=specific_query.count_earlyworking_days(name,sdate,edate)
                string_key='earlyworking_days'
            elif kindof==3:
                y=specific_query.count_lateworking_days(name,sdate,edate)
                string_key='lateworking_days'
            elif kindof==4:
                y=specific_query.count_absent_days(name,sdate,edate)
                string_key='absent_days'
            elif kindof==5:
                y=specific_query.count_working_days(name,sdate,edate)
                string_key='working_days'
            elif kindof==6:
                y=specific_query.count_ot_days(name,sdate,edate)
                string_key='OT_days'
            listkey=['name',string_key]
            results=JsonTranform.transfrom(y,listkey,len(listkey),IDphoto)    
        elif kindof==7:
            y=specific_query.show_ot_days(name,sdate,edate)
            listkey=['name','OTday']
            results=JsonTranform.transfrom(y,listkey,len(listkey),IDphoto)    
        else:
            data={}
            results=[]
            y=specific_query.count_ot_hours(name,sdate,edate)
            for i in y:
                data['name']=i[0]
                data["OThoursof"+str(i[2])]=str(i[1])
            data['IDphoto']=IDphoto
            json_data=json.dumps(data,ensure_ascii=False)
            json_data_json=json.loads(json_data)
            results.append(json_data_json)  
        return True, results