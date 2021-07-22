# -*- coding: utf8 -*-
from classes.mysqlconnect import mysqlConnect
from modules.copy_new_photo import copy_new_photo as cnp
from modules.copy_new_photo import delete_after_copy as dac
from modules.python_mysql_dbconfig import read_directory_config
from classes.calendar import Calendar
import os
import magic
import json
import datetime
import PIL.ExifTags
from io import StringIO
# python3
import sys
# import codecs

from modules.send_mail import sendemail

# old_stdout = sys.stdout
# sys.stdout = mystdout = StringIO()

print("Upload photos " + str(datetime.datetime.now()))

# photos_directory - название сборочного каталога
rdb = read_directory_config()
photos_directory = rdb['root']

# Получаем содержимое папки Photo

list_files = os.walk(photos_directory)

for d, dirs, files in list_files:
    for f in files:
        # Проверяем наличие файла и соответствие mime-типу "image-jpeg"
        try:
            os.chmod(d + '/' + f, mode=0o777, dir_fd=None, follow_symlinks=True)
        except os.error as e:
            exit(e)
        filename, file_extension = os.path.splitext(d + '/' + f)
        if (os.path.isfile(d + '/' + f)) and (magic.from_file(d + '/' + f, mime=True) == "image/jpeg") \
                and (file_extension in ['.jpg', '.JPG']):
            # Достаем EXIF-данные
            img = PIL.Image.open(d + '/' + f)
            exif = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in img._getexif().items()
                if k in PIL.ExifTags.TAGS
            }

            print('File ' + f)
            fileSize = os.path.getsize(d + '/' + f)
            print('File size: ' + str(fileSize) + ' bytes')

            new_exif = dict.fromkeys([])
            for val in exif.items():
                # Вычищаем все бинарные элементы из данных
                if not isinstance(val[1], bytes):
                    if val[0] != 'GPSInfo':
                        # print(val)
                        new_exif.update([val])
            # Создаем JSON - массив данных EXIF
            sum = json.dumps(new_exif)

            # Извлекаем дату создания фотографии в нужном нам формате
            photo_date = datetime.datetime.strptime(new_exif['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')

            month = datetime.datetime.timetuple(photo_date).tm_mon      # Месяц в числовом формате
            year = datetime.datetime.timetuple(photo_date).tm_year      # Год

            # Подключаемся к БД
            connect = mysqlConnect()
            # Проверяем наличие дубликатов в базе
            print(new_exif['DateTimeOriginal'])
            connect.query = "SELECT * FROM photos WHERE date_exif = '" + new_exif['DateTimeOriginal'] +"' AND file_size ='" \
                            + str(fileSize) + "'"

            if connect.query_with_fetchone() is not None:
                print("File is already exists")
            else:
                print("File is not exists")
                # Форматированный массив даты необходимый для создания директорий и поддиректорий
                date_array = {'year': str(year), 'month': Calendar(month).get_month(),
                              'file_path': d + '/' + f, 'file_name': f, 'file_size': fileSize}
                copy_files = cnp(date_array, new_exif, sum)
                # print(copy_files)


# Подчищаем директорию photos
if os.listdir(photos_directory):
    dac(photos_directory)
    # sys.stdout = old_stdout
    # sendemail(message = mystdout.getvalue())
else:
    print("Folder photos is empty")
    # sys.stdout = old_stdout
    # sendemail(message = mystdout.getvalue())

