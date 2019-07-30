import datetime
class DateChecker:

    @staticmethod
    def check_date(time_date):
        try:
            day,month,year=time_date.split("-")
        except:
            return False
        isvalidDate=True
        try:
            datetime.date(int(year),int(month),int(year))
        except ValueError:
            isvalidDate=False
        return isvalidDate

    @staticmethod
    def check_logic_date(start_date,end_date):
        isValid=True
        if not (DateChecker.check_date(start_date) and DateChecker.check_date(end_date)): isValid=False
        if start_date>end_date:
            isValid=False
        return isValid

    