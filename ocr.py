from constants.http_statscode import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from flask import Blueprint, request
from flask.json import jsonify
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required
from database import *
#import boto3 

#textractclient = boto3.client("textract", aws_access_key_id="AKIA3DTED6HGHGPOTTXJ",
#                              aws_secret_access_key="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")


ocr_app = Blueprint('ocrresult', __name__, url_prefix="/api/v1/ocrresult")



@ocr_app.get('/ocr')
def ocr():
    return jsonify({"msg":"work in progress"})