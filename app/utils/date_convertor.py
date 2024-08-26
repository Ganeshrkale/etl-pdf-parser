from datetime import datetime

class Date_convertor:
    def __init__(self) -> None:        
        self._date_formats =["%d/%m/%Y"
        ,"%Y-%m-%d"
        ,"%d-%m-%Y"
        ,"%d/%m/%Y"
        ,"%d/%m/%y"
        ,"%d/%b/%Y"
        ,"%d-%m-%Y %H:%M:%S"
        ,"%d-%m-%Y %I:%M:%S"
        ,"%d-%m-%Y %H:%M"
        ,"%Y-%m-%d %H:%M:%S"
        ,'%d.%m.%Y'
        ,'%d-%b-%y'
        ,'%w-%b-%y'
        ,'%d-%b-%Y'
        ,'%d-%m-%y'
        ,'%d/%b/%y'
        , '%b-%y'
        , '%b-%Y'
        , '%m/%Y'
        , '%m/%y'
        ,'%d.%m.%y'
        , '%m.%y'
        , '%m.%Y'
        , '%Y%m'
        , '%m/ %y'
        , '%b/%y'
        , '%b.%Y'
        , '%b %Y'
        , '%m-%y'
        , '%b %y'
        , ' %m-%y'
        , '%b-%Y '
        , '%B %d, %Y'
        , '%b %d, %Y '
        , '%b, %Y'
        ,'%b %d, %Y'
        ,'  %b %y  '
        ,'%d %b %Y'
        ,'%d.%b.%Y']

    def ConvertDate(self,dateString):
        for format in self._date_formats:
            try:                            
                convert_datetime=datetime.strptime(dateString, format)
                return convert_datetime.strftime("%Y-%m-%d")
            except Exception:
                continue
        
        return ""

    def ConvertInvoiceDate(self,dateString):
        for format in self._date_formats:
            try:                          
                convert_datetime=datetime.strptime(dateString, format)
                return convert_datetime.strftime("%d%m%Y")
            except Exception:
                continue
        
        return ""