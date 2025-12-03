#!/Users/Jesli/opt/anaconda3/bin/python
# -*- coding: UTF-8 -*-

import json
import io
import shutil
import os
import sys
# 获取项目根目录
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# 将项目根目录添加到 sys.path
sys.path.append(project_root)

from fb_library import model, sql

# from fb_library.model import db, Emote

class toEmote:
    # def __init__(self):

    def find_index_by_key_value(obj_list, key_name, value):
        for index, obj in enumerate(obj_list):
            if obj.get(key_name) == value:
                return obj_list[index]['bundleId']
        return -1  # 如果没有找到，则返回-1
    
    def copy_file(source_folder, target_folder, filename):
        try:
            # 构建源文件路径
            source_path = os.path.join(source_folder, filename)
            # 构建目标文件路径
            target_path = os.path.join(target_folder, filename)
            
            # 复制文件
            shutil.copy(source_path, target_path)
            
            print(f"File '{filename}' copied from '{source_folder}' to '{target_folder}'.")
        
        except FileNotFoundError:
            print(f"File '{filename}' not found in '{source_folder}'.")
        
        except PermissionError:
            print(f"Permission denied while copying file '{filename}'.")
        
        except Exception as e:
            print(f"An error occurred: {e}")

def main(emote_file, base_assets_catalog):
    # 读取CARD.json文件
    with io.open(emote_file, 'r', encoding='utf-8') as file:
        dbf_emote = json.loads(file.read())

    #  # 读取base_assets_catalog.json文件
    with io.open(base_assets_catalog, 'r', encoding='utf-8') as file:
        base_assets_catalog_json = json.loads(file.read())

    # print(dbf_emote['m_Container'])
    for em in dbf_emote['m_Container']:
        # print(em[0])
        # emote_id = em[0]
        emote_id = '1cc6b65bfe961db489aac3784148c257'
        bundleId = toEmote.find_index_by_key_value(base_assets_catalog_json['m_assets'], 'guid', emote_id)

        print(emote_id, bundleId, base_assets_catalog_json['m_bundleNames'][bundleId], '<---')
        # for m_assets in base_assets_catalog_json['m_assets']:

        #     print(toEmote.find_index_by_key_value(m_assets, 'guid', em[0]), '<---')
            # if m_assets['guid'] == em[0]:
            #     print(m_assets['bundle'], '<---')
        exit()

def toBattlegroundsEmote(emote_file, base_assets_catalog):
    # 读取CARD.json文件
    with io.open(emote_file, 'r', encoding='utf-8') as file:
        dbf_emote = json.loads(file.read())

    #  # 读取base_assets_catalog.json文件
    with io.open(base_assets_catalog, 'r', encoding='utf-8') as file:
        base_assets_catalog_json = json.loads(file.read())

    # 连接数据库
    # db = model.db
    # Emote = model.Emote
    # db.connect()
    SqlConn = sql.SqlConn()
    for emote in dbf_emote['Records']:
        # 拆分字符串
        path = emote['m_animationPath'].split('.controller:')

        bundleId = toEmote.find_index_by_key_value(base_assets_catalog_json['m_assets'], 'guid', path[1])

        name = emote['m_collectionShortName']['m_locValues'][-2].replace('\"', '')
        nameEN = emote['m_collectionShortName']['m_locValues'][0].replace('\"', '')

        info = {
            'm_id': emote['m_ID'],
            'name': name,
            'nameEN': nameEN,
            # 'img': 'https://hsbga.top/file/emote/{0}.png'.format(path[0]),
            'is_default': 1 if emote['m_isDefault'] else 2,
            'is_animating': 1 if emote['m_isAnimating'] else 2,
            'guid': path[1],
            'prefab': base_assets_catalog_json['m_bundleNames'][bundleId]
        }

        if ('_512_0' in path[0]):
            img_name = ''
        elif ('_final_final' in path[0]):
            img_name = path[0].replace('_final_final', '_final')
        elif ('_final_0 1' in path[0]):
            img_name = path[0].replace('_final_0 1', '_final')
        elif ('_final_0' in path[0]):
            img_name = path[0].replace('_final_0', '_final')
        else:
            img_name = path[0]

        if ((info['is_animating'] == 1) | (img_name == '')):
            info['img'] = ''
        else:
            info['img'] = 'https://hsbga.top/file/emote/{0}.png'.format(img_name)
            # 移动文件
            source_folder = 'api/Texture2D/'
            target_folder = 'api/emote/'  # 当前路径
            filename = '{0}.png'.format(img_name)
            toEmote.copy_file(source_folder, target_folder, filename)

        # 插入数据
        # book = Emote(name=info['name'], nameEN=info['nameEN'], prefab=info['prefab'], img=info['img'], m_id=info['m_id'], guid=info['guid'], is_animating=info['is_animating'], is_default=info['is_default'])
        # book.save()
        count = SqlConn.get_count('select * from bg_emote where m_id = {0}'.format(info['m_id']))

        if count == 0:
            print('insert')
            SqlConn.insert('insert into bg_emote (name, nameEN, prefab, img, m_id, guid, is_animating, is_default) values ("{0}", "{1}", "{2}", "{3}", "{4}", "{5}", {6}, {7})'.format(info['name'], info['nameEN'], info['prefab'], info['img'], info['m_id'], info['guid'], info['is_animating'], info['is_default']))
        else:
            print('update')
            SqlConn.update('update bg_emote set name="{0}", nameEN="{1}", prefab="{2}", img="{3}", m_id="{4}", guid="{5}", is_animating={6}, is_default={7} where m_id="{8}"'.format(info['name'], info['nameEN'], info['prefab'], info['img'], info['m_id'], info['guid'], info['is_animating'], info['is_default'], info['m_id']))

        SqlConn.commit()
        # print(count,'<---')
        # print(info, count,'<---')
        # exit()

if __name__ == "__main__":
    # dbf解析出来的CARD json文件 获取卡牌id（cardId）
    # emote_file = 'api/file/initial_bgs_global-c05a2d0e-prefab-0.unity3d.json'
    # base_assets_catalog 在得到guid后，需要通过base_assets_catalog查找guid所指向的文件存储在哪个压缩包（bundle）内
    base_assets_catalog = 'api/file/base_assets_catalog.json'

    # main(emote_file, base_assets_catalog)
    emote_file = 'api/file/BATTLEGROUNDS_EMOTE.json'
    toBattlegroundsEmote(emote_file, base_assets_catalog)

