
import json

class JsonTranform:

    @staticmethod
    def transfrom(x,lskey,numbers,IDphoto=''):
        data={}
        json_data_list=[] 
        for i in x:
            data.clear()
            #enumerate: thêm số đếm chạy vào trước
            for k, key in enumerate(lskey):
                data[key]=str(i[k])
                if (IDphoto!=''):
                    data['IDphoto']=IDphoto
            json_data=json.dumps(data,ensure_ascii=False)
            json_data_json=json.loads(json_data)
            json_data_list.append(json_data_json)
        return json_data_list