# -*- coding: utf8 -*-
import os
import shutil
import PIL.Image as Image
from os import error
from classes.mysqlconnect import MysqlConnect
import datetime
from modules.python_mysql_dbconfig import read_directory_config as rdc


def copy_new_photo(date_array={'year': 0000, 'month': 'Без даты', 'file_name': 'noname'}, new_exif={}, sum=""):
    path = {'source': '', 'original': '', 'thumbnails': ''}
    photos_directory = rdc()
    path['source'] = date_array['file_path']
    path['original'] = photos_directory['destination'] + '/' \
                       + str(date_array['year']) + '/' + date_array['month'] + '/' + 'original' + '/'
    path['thumbnails'] = photos_directory['destination'] + '/' \
                         + str(date_array['year']) + '/' + date_array['month'] + '/' + 'thumbnails' + '/'

    date_array.update({'original_path': '/' + str(date_array['year']) + '/'
                                        + date_array['month'] + '/' + 'original' + '/'})

    timestamp = str(datetime.datetime.timestamp(datetime.datetime.now()))
    timestamp = timestamp.replace('.', '')

    try:
        os.makedirs(path['thumbnails'] + 'small/', mode=0o777, exist_ok=True)
        os.makedirs(path['thumbnails'] + 'big/', mode=0o777, exist_ok=True)
        os.makedirs(path['original'], mode=0o777, exist_ok=True)
    except error as e:
        print("Cannot create a directory")
        print(e)

    if os.path.isdir(path['original']) is True and os.path.isdir(path['thumbnails']) is True:
        print('File will be copied here: ' + path['original'])

        try:
            file_name = os.path.basename(path['source'])
            file_path = shutil.copy2(path['source'], path['original'] + '/' + timestamp + '_' + file_name,
                                     follow_symlinks=True)

            scale_image(path['source'], path['thumbnails'] + 'big/' + timestamp + '_' + file_name, width=1000)
            scale_image(path['source'], path['thumbnails'] + 'small/' + timestamp + '_' + file_name, width=400)
            new_exif['file_name'] = file_name
            new_exif['file_x'] = file_name
            date_array['file_name'] = timestamp + '_' + file_name
            w, h = Image.open(path['source']).size

            try:
                new_exif['ExifImageWidth']
            except:
                print('Отсутствует параметр ExifImageWidth')
                new_exif['ExifImageWidth'] = w

            try:
                new_exif['ExifImageHeight']
            except:
                print('Отсутствует параметр ExifImageHeight')
                new_exif['ExifImageHeight'] = h

            insert_photo_db(date_array, new_exif, sum)

        except error as ef:
            print("Cannot copy file for this root")
            print(ef)

        print('Path to main file: ' + path['source'])
        # print('Путь назначения для копирования оригинала: ' + path['original'])
        # print('Путь назначения для копирования уменьшенных копий: ' + path['thumbnails'])

    else:
        print("There is no those directories!")
    return path


def scale_image(input_image_path,
                output_image_path,
                width=None,
                height=None
                ):
    original_image = Image.open(input_image_path)
    orientation = original_image._getexif().get(0x112)
    print("Orientation:" + str(orientation))
    rotate_values = {3: Image.ROTATE_180, 6: Image.ROTATE_270, 8: Image.ROTATE_90}
    rotate_deegrees = {3: 180, 6: 270, 8: 90}

    if orientation in rotate_values:
        original_image = original_image.transpose(rotate_values[orientation])
        print("Photo has been rotates on " + str(rotate_deegrees[orientation]) + ' degrees.')
    w, h = original_image.size
    print('Original photo size {wide} x {height} '.format(wide=w, height=h))

    if width and height:
        max_size = (width, height)
    elif width:
        max_size = (width, h)
    elif height:
        max_size = (w, height)
    else:
        # No width or height specified
        raise RuntimeError('Need parameters Height or Width!')
    original_image.thumbnail(max_size, Image.ANTIALIAS)
    original_image.save(output_image_path, quality=100)

    scaled_image = Image.open(output_image_path)
    width, height = scaled_image.size
    print('New photo size: {wide} x {height} '.format(wide=width, height=height))


def insert_photo_db(data, exif, sum):
    connect = MysqlConnect()

    connect.query = "INSERT INTO photos(`photo_name`, `file_name`, `date_exif`, `description`, `exif_image_width`, " \
                    "`exif_image_height`, `file_size`, `url`, `exif_content`, `created_at`, `updated_at`)" \
                    " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())"
    connect.args = (exif['file_name'], data['file_name'], exif['DateTimeOriginal'], 'Описание отсутствует',
                    str(exif['ExifImageWidth']), str(exif['ExifImageHeight']), str(data['file_size']),
                    str(data['original_path']), sum)
    try:
        if connect.query_with_insert() is not None:
            print("Saving record in DB is success!")
    except error as e:
        print("Cannot save record in DB!")
        print(e)
    return True


def delete_after_copy(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    print("Content of folder `" + folder + "` was deleted success!s")

# print(copy_new_photo())
# os.makedirs(path,exist_ok=True)
