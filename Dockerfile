FROM python:3.9.12-slim

# 新增資料夾 /path/to/app
RUN mkdir /opt/app

# 把所有檔案搬進去 /path/to/app
ADD ./ /opt/app/

# 設定下面工作路徑
WORKDIR /opt/app

# 設定 pip trust 這些公開庫
RUN pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org"

# pip3 安裝 requirements 裡的套件
RUN pip install -r /opt/app/configs/Requirements

# 執行 Hypercorn 執行服務
CMD python app.py
