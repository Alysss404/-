import streamlit as st
import pymysql
import pandas as pd

# import numpy as np
# import datetime
from sqlalchemy import create_engine
# DB_STRING = 'mysql+mysqlconnector://user:passwd@localhost/database?charset=utf8'
st.title("生态驾驶评分系统")
# st.header("范例")

db = pymysql.connect(host='%',  # host属性
                     user='eco',  # 用户名
                     password='123456',  # 此处填登录数据库的密码
                     db='new_demo1'  # 数据库名
                     )

cursor = db.cursor()


sql = "SELECT DISTINCT vehid FROM sample1 UNION SELECT DISTINCT vehid FROM upload;"
cursor.execute(sql)
pdate = pd.read_sql(sql, db)  # 以DataFrame格式读取显示

vid_option = st.sidebar.selectbox('choose the vehicle_id:', pdate)
# sql = "select  * from sample1,upload where vehid='{}';".format(vid_option)
cursor.execute(sql)
#
sql = "SELECT DISTINCT orderid FROM sample1 where vehid ='{}' UNION SELECT DISTINCT orderid FROM upload where vehid ='{}';".format(vid_option,vid_option)
cursor.execute(sql)
pdate = pd.read_sql(sql, db)  # 以DataFrame格式读取显示
# st.write(pdate)

oid_option = st.sidebar.selectbox('choose the order_id:', pdate)
sql = "select  * from sample1 where orderid='{}' UNION select  * from upload where orderid='{}';".format(oid_option,oid_option)
cursor.execute(sql)

pdate = pd.read_sql(sql, db)  # 以DataFrame格式读取显示


st.write(pdate)
st.map(pdate)

st.header("评分")
st.text("该车辆对应订单驾驶行为分析及其分数：")
sql = "select  * from score where orderid='{}';".format(oid_option)
cursor.execute(sql)

pdate = pd.read_sql(sql, db)  # 以DataFrame格式读取显示

st.write(pdate)


expander = st.expander("添加新的数据")
with expander:
    # st.header("添加新的数据")
    uploaded_files = st.file_uploader("请选择一个CSV文件", accept_multiple_files=True)
    uploaddf = pd.DataFrame()
    for uploaded_file in uploaded_files:
        uploaddf = pd.read_csv(uploaded_file)
        # otherStyleTime = uploaddf.strftime("%Y-%m-%d %H:%M:%S")
        st.write(uploaddf)
    #index =false 是不展示dataframe的index列  if_exists ‘append’代表 表存在即追加，‘replace’代表重建
    if st.button('上传到数据库'):
        engine = create_engine('mysql+pymysql://eco:123456@%/new_demo1?charset=utf8')
        uploaddf.to_sql('upload', engine, index=False, if_exists='append')
        st.success("上传成功!")




cursor.close()

db.close()
