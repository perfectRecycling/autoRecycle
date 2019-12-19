from django.shortcuts import render
from .garbage import detect
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
import boto3
import botocore
import json
import pymysql
import datetime
import ast
import paho.mqtt.client as mqtt

# s3 information
aws_access_key_id_ = 'AKIAI7HQZG3OB2MKNE7A'
aws_secret_access_key_ = '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'

s3 = boto3.client(
    's3',
    aws_access_key_id = aws_access_key_id_,
    aws_secret_access_key = aws_secret_access_key_
)

sns = boto3.client(
    "sns",
    aws_access_key_id=aws_access_key_id_,
    aws_secret_access_key=aws_secret_access_key_,
    region_name='ap-northeast-2'
)

# mysql rds 연결
host_name = 'recycle.c3eckkjcjnp8.ap-northeast-2.rds.amazonaws.com'
username = 'user'
password = 'wjs95159^^'
db_name = 'recycle-db'

db = pymysql.connect(
    host = host_name,
    port = 3306,
    user = username,
    passwd = password,
    db = db_name,
    charset='utf8'
)
curs = db.cursor()

print(db)

# get model
print('model preparing')
model = detect.get_model()
print('model prepared')

mqttc = mqtt.Client("python_pub")
mqttc.connect("test.mosquitto.org", 1883)

@csrf_exempt
def main(request):

    if request.method == 'POST':

        data = (request.body.decode('utf-8'))
        data = eval(data)
        data = json.dumps(data)
        data = json.loads(data)

        #file download_from s3
        #여기서 라즈베리가 전송한 이미지 받게됨
        # image_sources/img_user0.jpg'
        filename = data['file']
        # raspberry_ip = data['file'].split('_')[-1].split('.')[0]

        #filename = 'image_sources/custom_plastic_00350.jpg'
        #filename = data
        #filename = 'image_sources/12_user0.jpg'
        #filename = ''

        bucket_name = 'garbage-recycle'
        dst = 'recycles/'+filename
        s3.download_file(bucket_name, filename, dst)

        #get return about image classification result
        #라즈베리 파이 결과
        #결과 이미지는 detect.py에서 저장된다.
        returns, dates, filenames = detect.recycle(model, dst)

        #file upload
        for i, filename in enumerate(filenames):
            parsed = dates[i].split(' ')[0]
            s3_dst = 'image_results/'+parsed+'/'+returns[i]+'_'+dates[i]+'_'+str(i).zfill(5)+'.jpg'
            s3.upload_file(filename, bucket_name, s3_dst, ExtraArgs={'ACL': 'public-read'})

            #db 내용 갱신
            sql = "update today set positive_wastedcount = positive_wastedcount + 1 where DATE_FORMAT(date, '%%Y-%%m-%%d')\
            = %s and garbage_type = %s"
            curs.execute(sql, (parsed, returns[i]))
            sql2 = "insert into history(garbage_type, date, image_path) values(%s, %s, %s)"
            curs.execute(sql2, (returns[i], dates[i], 'https://garbage-recycle.s3.ap-northeast-2.amazonaws.com/'+s3_dst))
            db.commit()

        print(returns)
        return_str = ''
        for return_ in returns:
            return_str = return_str + return_ + ' '
        print('return result: ', return_str)
        mqttc.publish("user/0", return_str)
        mqttc.loop(2)

        return render(request, 'main.html')

    if request.method == 'GET':
        return render(request, 'main.html')

@csrf_exempt
def today(request):

    if request.method == 'GET':
        strnow = datetime.datetime.now().strftime('%Y-%m-%d')
        sql = "select * from today where DATE_FORMAT(date, '%%Y-%%m-%%d') = '%s'" % (strnow)

        curs.execute(sql)
        rows = curs.fetchall()

        results = {
        'chart': []
        }

        for row in rows:
            temp = {}
            temp['garbage_type'] = row[1]
            temp['positive_wastedcount'] = row[2]
            temp['negetive_wastedcount'] = row[3]
            temp['date'] = row[4].strftime('%Y-%m-%d %H:%M:%S')

            results['chart'].append(temp)

        print(results)

        return JsonResponse(results, json_dumps_params = {'ensure_ascii': True})

    else:
        return render(request, 'main.html')

@csrf_exempt
def history(request):
    if request.method == 'POST':
        data = (request.body.decode('utf-8'))
        data = eval(data)
        data = json.dumps(data)
        data = json.loads(data)

        print(data)

        results = {
        'chart': [],
        'history': [],
        }


        sql = "select * from today where DATE_FORMAT(date, '%%Y-%%m-%%d') = \
        %s"
        curs.execute(sql, data['date'])
        rows = curs.fetchall()
        for row in rows:
            temp = {}
            temp['garbage_type'] = row[1]
            temp['positive_wastedcount'] = row[2]
            temp['negetive_wastedcount'] = row[3]
            temp['date'] = row[4].strftime('%Y-%m-%d %H:%M:%S')

            results['chart'].append(temp)

        if data['garbage_type'] == 'All':
            sql = "select * from history where DATE_FORMAT(date, '%%Y-%%m-%%d') = \
            %s"
            curs.execute(sql,data['date'])
            rows = curs.fetchall()
            image = None
            for row in rows:
                temp = {}
                temp['id'] = row[0]
                temp['garbage_type'] = row[1]
                temp['date'] = row[2].strftime('%Y-%m-%d %H:%M:%S')
                temp['image_path'] = row[3]
                results['history'].append(temp)

            return JsonResponse(results, json_dumps_params = {'ensure_ascii': True})

        else:
            sql = "select * from history where garbage_type = %s and DATE_FORMAT(date, '%%Y-%%m-%%d') = \
            %s"
            curs.execute(sql,(data['garbage_type'], data['date']))
            rows = curs.fetchall()
            for row in rows:
                temp = {}
                temp['id'] = row[0]
                temp['garbage_type'] = row[1]
                temp['date'] = row[2].strftime('%Y-%m-%d %H:%M:%S')
                temp['image_path'] = row[3]
                print(temp)
                results['history'].append(temp)
            print(results)

            return JsonResponse(results, json_dumps_params = {'ensure_ascii': True})
