from flask import request, jsonify
from app import app
from flask_cors import cross_origin
from app.services import parser_service, parse_and_upload_file
from app.utils.const import HttpStatus
from app.utils.exception_log import *
import os
import gc
import uuid


@app.route("/GetFileByPlumber", methods=["POST"])
@cross_origin()
def getFileByPlumber():
    if request.method == "POST":
        try:
            if os.path.isdir("/Plumbers/") == False:
                os.mkdir("/Plumbers")
            file_details = request.files["file"]
            FilePath = "/Plumbers/" + file_details.filename
            file_details.save(FilePath)

            pdf_parser = parser_service.PdfParser()
            pdf_plumber_df = pdf_parser.PDFPlumber_Parsercheck(FilePath)

            if os.path.isfile(FilePath):
                os.remove(FilePath)
            construct = {
                "plumber": pdf_plumber_df.to_json(orient="index")
            }

            response = jsonify(construct)
            response.status_code = HttpStatus.OK

        except Exception as e:
            response = ExceptionLog.ExceptionResponse(
                e, "/GetFileByPlumber", file_details.filename)

    gc.collect(generation=2)
    return response


@app.route("/ParseFileByPlumber", methods=["POST"])
@cross_origin()
def parseFileByPlumber():
    if request.method == "POST":
        request_data = request.form.to_dict()
        try:
            if os.path.isdir("/Plumbers/") == False:
                os.mkdir("/Plumbers")
            file_details = request.files["file"]
            file_extension = os.path.splitext(file_details.filename)[1]
            file_uuid = str(uuid.uuid4())
            file_path = os.path.join("/Plumbers/", file_uuid + file_extension)
            file_details.save(file_path)
            template_data = request_data.get("TEMPLATE_DETAILS", "")
            parserType = request_data.get("PARSER_TYPE", "")

            pdf_parser = parse_and_upload_file.Parse_and_upload_file()
            parse_temp_df, non_parse_temp_df = pdf_parser.parse_file(
                template_data, file_path, parserType)

            if os.path.isfile(file_path):
                os.remove(file_path)
            construct = {
                "parse_temp_df": parse_temp_df.to_json(orient="index"),
                "non_parse_temp_df": non_parse_temp_df.to_json(orient="index")
            }

            response = jsonify(construct)
            response.status_code = HttpStatus.OK

        except Exception as e:
            response = ExceptionLog.ExceptionResponse(
                e, "/ParseFileByPlumber", file_details.filename)

    gc.collect(generation=2)
    return response


@app.route("/EtlParseFileByPlumber", methods=["POST"])
@cross_origin()
def etlparseFileByPlumber():
    if request.method == "POST":
        request_data = request.form.to_dict()
        try:
            if os.path.isdir("/Plumbers/") == False:
                os.mkdir("/Plumbers")
            file_details = request.files["file"]
            file_extension = os.path.splitext(file_details.filename)[1]
            file_uuid = str(uuid.uuid4())
            file_path = os.path.join("/Plumbers/", file_uuid + file_extension)
            file_details.save(file_path)
            invoice = request_data.get("invoice", "")
            inv_num = request_data.get("inv_num", "")
            inv_date = request_data.get("inv_date", "")
            inv_loc = request_data.get("inv_loc", "")
            inv_double_line = request_data.get("inv_double_line", "")
            inv_last_line = request_data.get("inv_last_line", "")
            gross_amt_regex = request_data.get("gross_amt_regex", "")
            ptr_dis_amt_total_regex = request_data.get(
                "ptr_dis_amt_total_regex", "")
            sp_dis_amt_pts_total_regex = request_data.get(
                "sp_dis_amt_pts_total_regex", "")
            cgst_amt_regex = request_data.get("cgst_amt_regex", "")
            sgst_amt_regex = request_data.get("sgst_amt_regex", "")
            igst_amt_regex = request_data.get("igst_amt_regex", "")
            ugst_amt_regex = request_data.get("ugst_amt_regex", "")
            due_date_regex = request_data.get("due_date_regex", "")

            pdf_parser = parser_service.PdfParser()
            parse_temp_df, non_parse_temp_df = pdf_parser.plumber_parser(file_path, "", "", "", "", "", "C2D_INVOICE", "", "", invoice,
                                                                         inv_date, inv_num, inv_loc, inv_double_line, inv_last_line, gross_amt_regex,
                                                                         ptr_dis_amt_total_regex, sp_dis_amt_pts_total_regex, cgst_amt_regex,
                                                                         sgst_amt_regex, igst_amt_regex, ugst_amt_regex, due_date_regex)

            if os.path.isfile(file_path):
                os.remove(file_path)
            construct = {
                "parse_temp_df": parse_temp_df.to_json(orient="index"),
                "non_parse_temp_df": non_parse_temp_df.to_json(orient="index")
            }

            response = jsonify(construct)
            response.status_code = HttpStatus.OK

        except Exception as e:
            response = ExceptionLog.ExceptionResponse(
                e, "/EtlParseFileByPlumber", file_details.filename)

    gc.collect(generation=2)
    return response
