import os
import pandas as pd
import re
import uuid
import pdfplumber
from app.utils.date_convertor import *
from app.logger.log import logger

class PdfParser:
    def __init__(self) -> None:
        self.__inv_date = ""
        self.__inv_number = ""
        self.__inv_loc = ""
        self.__gross_amt_regex = ""
        self.__ptr_dis_amt_total_regex = ""
        self.__sp_dis_amt_pts_total_regex = ""
        self.__cgst_amt_regex = ""
        self.__sgst_amt_regex = ""
        self.__igst_amt_regex = ""
        self.__ugst_amt_regex = ""
        self.__due_date_regex = ""
        self.name = None
        self._c2d_invoice_columns = ["PRODUCT_NAME","PRODUCT_CODE","BATCH_NUMBER","MANU_NAME","HSN_CODE","QTY","MRP","PTR","PTS","UPC_CODE", "PACK", "EXPIRY_DATE", "FREE_QTY", "PTR_DIS_PERC", "PTR_DIS_AMT", "SP_DISC_PERC_PTS", "SP_DISC_AMT_PTS", "TAXABLE_AMT", "CGST_PERC", "CGST_AMT", "SGST_PERC", "SGST_AMT", "IGST_PERC", "IGST_AMT", "UGST_PERC", "UGST_AMT", "DUEDATE"]      
        self._jsonNonparsed = dict()
        self._jsonDict = dict()
    # check file is parse using Plumber
    def PDFPlumber_Parsercheck(self, fileName):
        if os.path.isfile(fileName):
            list_to_df = pd.DataFrame()
            sourse_file = str(uuid.uuid1()) + ".csv"
            pdf_to_df = pdfplumber.open(fileName)

            for pdf in pdf_to_df.pages:
                extract_data = pdf.extract_text()
                if len(list_to_df) < 1:
                    list_to_df = pd.DataFrame([extract_data])
                else:
                    list_to_df = pd.concat([list_to_df,pd.DataFrame([extract_data])])

            list_to_df.to_csv(sourse_file)
            read_data = pd.read_csv(sourse_file)

            if os.path.isfile(sourse_file):
                os.remove(sourse_file)

            pdf_to_df.close()
            return read_data
    
    def plumber_parser(self, filename, companyRegex, ordernumber_Regex, stockandsales_order_Regex, dateRegex, supplier_regex, type, double_regex,order_returns,invoice=None, inv_date=None, inv_num=None, inv_loc=None, inv_double_line=None, inv_last_line=None, gross_amt_regex=None, ptr_dis_amt_total_regex=None, sp_dis_amt_pts_total_regex=None, cgst_amt_regex=None, sgst_amt_regex=None, igst_amt_regex=None, ugst_amt_regex=None, due_date_regex=None, erp_number_regex=None, is_auto=False):
        pdf_to_df = pdfplumber.open(filename)
        if(type == "C2D_INVOICE"):
            for lines in pdf_to_df.pages:
                if lines.extract_text() != None: 
                    self.parse_c2d_invoice(lines.extract_text(), "Plumber", "",dateRegex, invoice, filename, inv_num, inv_date, inv_loc, inv_double_line, inv_last_line, gross_amt_regex, ptr_dis_amt_total_regex, sp_dis_amt_pts_total_regex, cgst_amt_regex, sgst_amt_regex, igst_amt_regex, ugst_amt_regex, due_date_regex)

        parse_df = pd.DataFrame.from_dict(self._jsonDict)
        non_parse_df = pd.DataFrame.from_dict(self._jsonNonparsed)

        # pdf_to_df.close_file()
        pdf_to_df.close()
        if(type == "C2D_INVOICE"):
            parse_df.replace(to_replace='GROSS_AMT', value=str(self.__gross_amt_regex), inplace=True)
            parse_df.replace(to_replace='PTR_DIS_AMT_TOTAL', value=str(self.__ptr_dis_amt_total_regex), inplace=True)
            parse_df.replace(to_replace='SP_DISC_AMT_PTS_TOTAL', value=str(self.__sp_dis_amt_pts_total_regex), inplace=True)
            parse_df.replace(to_replace='CGST_AMT_TOTAL', value=str(self.__cgst_amt_regex), inplace=True)
            parse_df.replace(to_replace='SGST_AMT_TOTAL', value=str(self.__sgst_amt_regex), inplace=True)
            parse_df.replace(to_replace='IGST_AMT_TOTAL', value=str(self.__igst_amt_regex), inplace=True)
            parse_df.replace(to_replace='UGST_AMT_TOTAL', value=str(self.__ugst_amt_regex), inplace=True)
            parse_df.replace(to_replace='DUE_DATE', value=str(self.__due_date_regex), inplace=True)
        return parse_df,  non_parse_df

    
    def parse_c2d_invoice(self, pdf_to_df, parser, companyRegx, datesRegx, invoiceRegex, filename, invNumberRegex, invDateRegex, invoiceLocRegx, invoiceDoubleLine, invoiceLastLine, gross_amt_regex, ptr_dis_amt_total_regex, sp_dis_amt_pts_total_regex, cgst_amt_regex, sgst_amt_regex, igst_amt_regex, ugst_amt_regex, due_date_regex):   
        try:
            if invoiceRegex:
                main_line_cnt = 1
                double_line_cnt = 0
                companyReg = re.compile(companyRegx.strip(), re.IGNORECASE)
                invoiceReg = re.compile(invoiceRegex.strip(), re.IGNORECASE)
                invoiceNumberReg = re.compile(invNumberRegex.strip(), re.IGNORECASE)
                invoiceDateReg = re.compile(invDateRegex.strip(), re.IGNORECASE)
                invoiceLocReg = re.compile(invoiceLocRegx.strip(), re.IGNORECASE)
                gross_amtReg = re.compile(gross_amt_regex.strip(), re.IGNORECASE)
                ptr_dis_amt_totalReg = re.compile(ptr_dis_amt_total_regex.strip(), re.IGNORECASE)
                sp_dis_amt_pts_totalReg = re.compile(sp_dis_amt_pts_total_regex.strip(), re.IGNORECASE)
                cgst_amtReg = re.compile(cgst_amt_regex.strip(), re.IGNORECASE)
                sgst_amtReg = re.compile(sgst_amt_regex.strip(), re.IGNORECASE)
                igst_amtReg = re.compile(igst_amt_regex.strip(), re.IGNORECASE)
                ugst_amtReg = re.compile(ugst_amt_regex.strip(), re.IGNORECASE)
                due_dateReg = re.compile(due_date_regex.strip(), re.IGNORECASE)
                if invoiceDoubleLine:
                    invoiceDoubleLineReg = re.compile(invoiceDoubleLine.strip(), re.IGNORECASE)
                    invoiceLastLineReg = re.compile(invoiceLastLine.strip(), re.IGNORECASE)
                
                tempfile_name = filename.split('/')[-1]
                
                # self.get_distributor_company(tempfile_name)

                dateconversion= Date_convertor()
                
                if pdf_to_df != None:
                    for line in pdf_to_df if parser != "Plumber" else pdf_to_df.split("\n"):
                        if parser == "Fitz" or parser == "Tabula" or parser == "Mupdf":
                            line = line[0]
                        # Check if company regex
                        if companyRegx.strip() != "":
                            match_company_regex = companyReg.match(line)
                            if match_company_regex:
                                self.__com = match_company_regex.group("COMPANY")
                                # continue
                        
                        # Check if inv date regex
                        if invDateRegex.strip() != "":                        
                            match_date_regex = invoiceDateReg.match(line)
                            if match_date_regex:
                                if self.__inv_date == "":
                                    if "INVOICE_DATE" in match_date_regex.groupdict(): 
                                        self.__inv_date =dateconversion.ConvertInvoiceDate(match_date_regex.group("INVOICE_DATE"))                               

                        # Check if inv number regex 
                        if invNumberRegex.strip() != "":                        
                            match_number_regex = invoiceNumberReg.match(line)
                            if match_number_regex:
                                if self.__inv_number == "":
                                    if "INVOICE_NUMBER" in match_number_regex.groupdict():
                                        self.__inv_number =match_number_regex.group("INVOICE_NUMBER") 

                        # Check if inv loc regex 
                        if invoiceLocRegx.strip() != "":                        
                            match_loc_regex = invoiceLocReg.match(line)
                            if match_loc_regex:
                                if self.__inv_loc == "":
                                    if "LOCATION" in match_loc_regex.groupdict():                                
                                        self.__inv_loc =match_loc_regex.group("LOCATION")   

                        if gross_amt_regex.strip() != "":
                            match_gross_amt_regex = gross_amtReg.match(line)
                            if match_gross_amt_regex:
                                if self.__gross_amt_regex == "":
                                    # print("HERE 2", match_gross_amt_regex.group("GROSS_AMT"))
                                    if "GROSS_AMT" in match_gross_amt_regex.groupdict():
                                        self.__gross_amt_regex = match_gross_amt_regex.group("GROSS_AMT")
                        
                        if ptr_dis_amt_total_regex.strip() != "":
                            match_ptr_dis_amt_total_regex = ptr_dis_amt_totalReg.match(line)
                            if match_ptr_dis_amt_total_regex:
                                if self.__ptr_dis_amt_total_regex == "":
                                    if "PTR_DIS_AMT_TOTAL" in match_ptr_dis_amt_total_regex.groupdict():
                                        self.__ptr_dis_amt_total_regex = match_ptr_dis_amt_total_regex.group("PTR_DIS_AMT_TOTAL")
                        if sp_dis_amt_pts_total_regex.strip() != "":
                            match_sp_dis_amt_pts_total_regex = sp_dis_amt_pts_totalReg.match(line)
                            if match_sp_dis_amt_pts_total_regex:
                                if self.__sp_dis_amt_pts_total_regex == "":
                                    if "SP_DISC_AMT_PTS_TOTAL" in match_sp_dis_amt_pts_total_regex.groupdict():
                                        self.__sp_dis_amt_pts_total_regex = match_sp_dis_amt_pts_total_regex.group("SP_DISC_AMT_PTS_TOTAL")
                        if cgst_amt_regex.strip() != "":
                            match_cgst_amt_regex = cgst_amtReg.match(line)
                            if match_cgst_amt_regex:
                                if self.__cgst_amt_regex == "":
                                    if "CGST_AMT_TOTAL" in match_cgst_amt_regex.groupdict():
                                        self.__cgst_amt_regex = match_cgst_amt_regex.group("CGST_AMT_TOTAL")
                        if sgst_amt_regex.strip() != "":
                            match_sgst_amt_regex = sgst_amtReg.match(line)
                            if match_sgst_amt_regex:
                                if self.__sgst_amt_regex == "":
                                    if "SGST_AMT_TOTAL" in match_sgst_amt_regex.groupdict():
                                        self.__sgst_amt_regex = match_sgst_amt_regex.group("SGST_AMT_TOTAL")
                        if igst_amt_regex.strip() != "":
                            match_igst_amt_regex = igst_amtReg.match(line)
                            if match_igst_amt_regex:
                                if self.__igst_amt_regex == "":
                                    if "IGST_AMT_TOTAL" in match_igst_amt_regex.groupdict():
                                        self.__igst_amt_regex = match_igst_amt_regex.group("IGST_AMT_TOTAL")
                        if ugst_amt_regex.strip() != "":
                            match_ugst_amt_regex = ugst_amtReg.match(line)
                            if match_ugst_amt_regex:
                                if self.__ugst_amt_regex == "":
                                    if "UGST_AMT_TOTAL" in match_ugst_amt_regex.groupdict():
                                        self.__ugst_amt_regex = match_ugst_amt_regex.group("UGST_AMT_TOTAL")
                        if due_date_regex.strip() != "":
                            match_due_date_regex = due_dateReg.match(line)
                            if match_due_date_regex:
                                if self.__due_date_regex == "":
                                    if "DUE_DATE" in match_due_date_regex.groupdict():
                                        self.__due_date_regex =dateconversion.ConvertInvoiceDate(match_due_date_regex.group("DUE_DATE"))

                        # Check if stock and sale regex
                        if invoiceRegex.strip() != "":
                            match_invoice_regex = invoiceReg.match(line)

                            if match_invoice_regex:
                                # main_line_cnt = main_line_cnt + 1
                                main_line_cnt = 0
                                # Checking for line is not the last line
                                # if str.__contains__(line.upper(), "QUANTITY") != True and str.__contains__(line.upper(), "TOTAL") != True:
                                if True:
                                    # "COMPANY_CODE","COMPANY_NAME",
                                    if "COMPANY_CODE" not in self._jsonDict:
                                        self._jsonDict["COMPANY_CODE"] = list()
                                    # self._jsonDict["COMPANY_CODE"].append(self.__com)
                                    self._jsonDict["COMPANY_CODE"].append("short code")

                                    if "COMPANY_NAME" not in self._jsonDict:
                                        self._jsonDict["COMPANY_NAME"] = list()
                                    self._jsonDict["COMPANY_NAME"].append("company name")

                                    if "INVOICE_DATE" not in self._jsonDict:
                                        self._jsonDict["INVOICE_DATE"] = list()
                                    self._jsonDict["INVOICE_DATE"].append(self.__inv_date)

                                    if "INVOICE_NUMBER" not in self._jsonDict:
                                        self._jsonDict["INVOICE_NUMBER"] = list()
                                    self._jsonDict["INVOICE_NUMBER"].append(self.__inv_number)

                                    if "INVOICE_LOCATION" not in self._jsonDict:
                                        self._jsonDict["INVOICE_LOCATION"] = list()
                                    self._jsonDict["INVOICE_LOCATION"].append(self.__inv_loc)

                                    if "GROSS_AMT" not in self._jsonDict:
                                        self._jsonDict["GROSS_AMT"] = list()
                                    self._jsonDict["GROSS_AMT"].append("GROSS_AMT")
                                    
                                    if "PTR_DIS_AMT_TOTAL" not in self._jsonDict:
                                        self._jsonDict["PTR_DIS_AMT_TOTAL"] = list()
                                    self._jsonDict["PTR_DIS_AMT_TOTAL"].append("PTR_DIS_AMT_TOTAL")
                                    
                                    if "SP_DISC_AMT_PTS_TOTAL" not in self._jsonDict:
                                        self._jsonDict["SP_DISC_AMT_PTS_TOTAL"] = list()
                                    self._jsonDict["SP_DISC_AMT_PTS_TOTAL"].append("SP_DISC_AMT_PTS_TOTAL")
                                    
                                    if "CGST_AMT_TOTAL" not in self._jsonDict:
                                        self._jsonDict["CGST_AMT_TOTAL"] = list()
                                    self._jsonDict["CGST_AMT_TOTAL"].append("CGST_AMT_TOTAL")
                                    
                                    if "SGST_AMT_TOTAL" not in self._jsonDict:
                                        self._jsonDict["SGST_AMT_TOTAL"] = list()
                                    self._jsonDict["SGST_AMT_TOTAL"].append("SGST_AMT_TOTAL")
                                    
                                    if "IGST_AMT_TOTAL" not in self._jsonDict:
                                        self._jsonDict["IGST_AMT_TOTAL"] = list()
                                    self._jsonDict["IGST_AMT_TOTAL"].append("IGST_AMT_TOTAL")
                                    
                                    if "UGST_AMT_TOTAL" not in self._jsonDict:
                                        self._jsonDict["UGST_AMT_TOTAL"] = list()
                                    self._jsonDict["UGST_AMT_TOTAL"].append("UGST_AMT_TOTAL")

                                    if "DUE_DATE" not in self._jsonDict:
                                        self._jsonDict["DUE_DATE"] = list()
                                    self._jsonDict["DUE_DATE"].append("DUE_DATE")
                                    

                                    # if "H" not in self._jsonDict:
                                    #     self._jsonDict["H"] = list()
                                    # self._jsonDict["H"].append("T")

                                    for x in self._c2d_invoice_columns:
                                        # x = x['Name']
                                        try:
                                            if x.strip() not in self._jsonDict:
                                                self._jsonDict[x.strip()] = list()
                                            if x.strip() == "EXPIRY_DATE":
                                                self._jsonDict[x].append(dateconversion.ConvertInvoiceDate(match_invoice_regex.group(x.strip())))
                                            else:
                                                self._jsonDict[x].append(match_invoice_regex.group(x.strip()))
                                        except IndexError:
                                            if x.strip() not in self._jsonDict:
                                                self._jsonDict[x.strip()] = list()
                                            self._jsonDict[x].append('')

                                    continue
                                continue
                            elif invoiceDoubleLine:
                                if invoiceDoubleLine.strip() != "":                                    
                                    match_duble_line = invoiceDoubleLineReg.match(line)
                                    if match_duble_line:
                                        if invoiceLastLine:
                                            if invoiceLastLine.strip() != "":
                                                try:
                                                    match_last_line = invoiceLastLineReg.match(line)
                                                    if match_last_line:
                                                        main_line_cnt=1
                                                except Exception as e:
                                                    print(e)
                                        if main_line_cnt == 0 :
                                            for x in match_duble_line.groupdict().keys():
                                                if x in self._jsonDict:
                                                    dict_len = len(self._jsonDict["PRODUCT_NAME"]) - 1
                                                    if x.strip() == "EXPIRY_DATE":
                                                        self._jsonDict[x][dict_len] = self._jsonDict[x][dict_len] + "" + dateconversion.ConvertInvoiceDate(match_duble_line.group(x.strip()))
                                                    else:
                                                        # print(self._jsonDict["PRODUCT_NAME"][dict_len], match_duble_line.group("PRODUCT_NAME"))
                                                        self._jsonDict[x][dict_len] = self._jsonDict[x][dict_len] + "" + match_duble_line.group(x)
                                    else:
                                        main_line_cnt = 1
                                    # continue

                        # non_parse_regex = re.compile("(?P<NON_PARSE>[\-]*[A-Z0-9\~\#\*\s]+).*", re.IGNORECASE)
                        
                        # match_non_parse_regex = non_parse_regex.match(line)
                        # if match_non_parse_regex:
                        
                        if "NON_PARSE" not in self._jsonNonparsed:
                            self._jsonNonparsed["NON_PARSE"] = list()
                        self._jsonNonparsed['NON_PARSE'].append(line)
            
        except Exception as e:
            logger.error(e)
            
            
    