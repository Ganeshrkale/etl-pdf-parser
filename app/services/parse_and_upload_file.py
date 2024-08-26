import json
import app.services.parser_service as pt
from app.utils.const import *
import pandas as pd

class Parse_and_upload_file:
    def parse_file(self,template_detail,destination_file_name,parserType,is_auto=False):
        template_details = json.loads(template_detail)
        companyRegex=""
        ordernumber_Regex=""
        invoice_Regex=""
        invoice_DateRegex=""
        invoice_NumberRegex=""
        invoice_LocRegex=""
        invoice_Double_Lined=""
        invoice_Last_Line=""
        invoice_Gross_Amt = ""
        invoice_PtrDisc_Amt_Total = ""
        invoice_SpDisc_Amt_Total = ""
        invoice_Cgst_Amt_Total = ""
        invoice_Sgst_Amt_Total = ""
        invoice_Igst_Amt_Total = ""
        invoice_Ugst_Amt_Total = ""
        invoice_Due_Date = ""
        c2dReturnsRegex = ""
        erp_Number = ""
        
        stockandsale_order=template_details.get("StockandSaleRegex","")
        dateRegex=template_details.get("DateRegex","")
        supplierRegex=template_details.get("SupplierName","")
        doubleRegex=template_details.get("DoubleRegex",None)
        
        if doubleRegex == None:
            doubleRegex = ""
        
        if parserType == "C2D_INVOICE":
            invoice_Regex = template_details.get("InvoiceRegex","")
            invoice_DateRegex = template_details.get("InvoiceDateRegex","")
            invoice_NumberRegex = template_details.get("InvoiceNumberRegex","")
            invoice_LocRegex = template_details.get("InvoiceLocation","")
            invoice_Double_Lined = template_details.get("InvoiceDoubleLine","")
            invoice_Last_Line = template_details.get("InvoiceLastLine","")
            invoice_Gross_Amt = template_details.get("GrossAmtRegex")
            invoice_PtrDisc_Amt_Total = template_details.get("PTRDiscAmtTotalRegex")
            invoice_SpDisc_Amt_Total = template_details.get("SPDiscAmtPTSTotalRegex")
            invoice_Cgst_Amt_Total = template_details.get("CGSTAmtTotalRegex")
            invoice_Sgst_Amt_Total = template_details.get("SGSTAmtTotalRegex")
            invoice_Igst_Amt_Total = template_details.get("IGSTAmtTotalRegex")
            invoice_Ugst_Amt_Total = template_details.get("UGSTAmtTotalRegex")
            invoice_Due_Date = template_details.get("DueDateRegex")

        parse_temp_df = pd.DataFrame()
        non_parse_temp_df = pd.DataFrame()
        
        check_file_name=destination_file_name.split('.')[-1].lower()
        
        if check_file_name == 'pdf':            
            if template_details.get("Parser","") == "Plumber":
                pdf_parser = pt.PdfParser()
                parse_temp_df, non_parse_temp_df = pdf_parser.plumber_parser(
                    destination_file_name, companyRegex, ordernumber_Regex, stockandsale_order, dateRegex,supplierRegex,parserType,double_regex=doubleRegex.replace("^", "'"),order_returns=c2dReturnsRegex,invoice=invoice_Regex,inv_date=invoice_DateRegex,inv_num=invoice_NumberRegex, inv_loc=invoice_LocRegex, inv_double_line=invoice_Double_Lined, inv_last_line=invoice_Last_Line, gross_amt_regex=invoice_Gross_Amt, ptr_dis_amt_total_regex=invoice_PtrDisc_Amt_Total, sp_dis_amt_pts_total_regex=invoice_SpDisc_Amt_Total,cgst_amt_regex=invoice_Cgst_Amt_Total, sgst_amt_regex=invoice_Sgst_Amt_Total, igst_amt_regex=invoice_Igst_Amt_Total, ugst_amt_regex=invoice_Ugst_Amt_Total,due_date_regex=invoice_Due_Date, erp_number_regex=erp_Number, is_auto=is_auto)
            
        return parse_temp_df,non_parse_temp_df
