# coding = utf-8
import json
import cv2
from fastapi import FastAPI, UploadFile
import numpy as np
from handler.http_handler import init_http_exception_handler
from models.captcha_models import *
from models.response_models import captcha_response

from hypercorn.asyncio import serve
from hypercorn import Config
import asyncio


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'JPG', 'JPEG', 'PNG'])

app = FastAPI(
    title="圖片驗證API",
    description='',
    version="0.0.1",
    terms_of_service="",
)

init_http_exception_handler(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.get("/")
def index():
    return "HI, 歡迎使用圖形驗證碼API，若要看相關文件請至 /docs"


@app.post("/api/captcha_id", response_model= captcha_response)
async def captcha_id(file: UploadFile):
    """
    圖形驗證碼
    
    - **tags**: 圖片驗證碼五碼六碼通用
    - **consumes**: ["multipart/form-data"]
    - **parameters**:
        - name: file
        - in: formData
        - type: file
        - required: true
    - **responses**:
        - status:
            - 200: 回傳運算結果
            - 400: 檔案上傳不成功 / 檔案格式不符
            - 404: 更版或維修中，請通知數數部
            - 500: 服務機出現異常，請通知數數部
        - res: 運算結果或錯誤資訊
    """
    
    if not file:
        return captcha_response(status = 400, res = '檔案上傳不成功')
    else:
        if allowed_file(file.filename):
            try:
                contents = await file.read()
                image_bytes = np.frombuffer(contents, np.uint8)
                image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
                image = cv2.resize(image, (200, 60), interpolation=cv2.INTER_AREA)
                model = captcha_model_id()
                model.load_weights('./checkpoints/verificatioin_code-1118-id.h5')
                captcha_text = model.predict(image)
                # return captcha text
                return captcha_response(status = 200, res = captcha_text)
            except:
                return captcha_response(status = 500, res = '服務機出現異常，請通知數數部')
        else:
            return  captcha_response(status = 400, res = '檔案格式不符')


if __name__ == "__main__":
    file = open("./configs/hypercorn_config.json")
    config = json.load(file)
    
    hc_config = Config()
    hc_config.worker_class = config["worker_class"]
    hc_config.workers = config["workers"]
    hc_config.keep_alive_timeout = config["keep_alive_timeout"]


    if config['https']:
        hc_config.bind = [config['ip'] + ':443']
        hc_config.certfile = config['certfile']
        hc_config.keyfile = config['keyfile']
        hc_config.insecure_bind = [config['ip'] + ":" + config['port']]
    else:
        hc_config.bind = [config['ip'] + ":" + config['port']]
    
    # config定義在 ./config/hypercorn_config
    asyncio.run(serve(app, hc_config))