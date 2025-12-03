#!/Users/Jesli/opt/anaconda3/bin/python
# -*- coding: UTF-8 -*-

import json
import io

class toBattlegroundsCard:
    def __init__(self, inFile, outDir):
        self.inFile = inFile
        self.outDir = outDir

def main(dbf_CARD, cards_map, base_assets_catalog):
    # 读取CARD.json文件
    with io.open(dbf_CARD, 'r', encoding='utf-8') as file:
        dbf_CARD_json = json.loads(file.read())
        
    # 读取cards_map.json文件
    # with io.open(cards_map, 'r', encoding='utf-8') as file:
    #     cards_map_json = file.read()
    
    #  # 读取base_assets_catalog.json文件
    # with io.open(base_assets_catalog, 'r', encoding='utf-8') as file:
    #     base_assets_catalog_json = file.read()

    # print(dbf_CARD_json['Records'])
    for card in dbf_CARD_json['Records']:
        if 'BG' in card['m_noteMiniGuid']:
            # dbfid（m_ID, 100)和卡牌id（m_noteMiniGuid, NEW1_034）
            dbf_id  = card['m_ID']
            strId   = card['m_noteMiniGuid']
            nameCn  = card['m_name']['m_locValues'][-2]
            text    = card['m_textInHand']['m_locValues'][-2]
            print(dbf_id, strId, nameCn, text)
            exit()

    
if __name__ == "__main__":
    # dbf解析出来的CARD json文件 获取卡牌id（cardId）
    dbf_CARD = 'api/file/CARD.json'
    # asset_manifest 里面是一系列资源文件的目录/映射
    # cards_map 在asset_manifest中能找到这个cards_map，这是所有卡牌的定义文件（cardDef）的索引。cards_map也分为两部分，一是key，这里记录的是每张卡的卡牌id（cardId）
    cards_map = 'api/file/cards_map.json'
    # base_assets_catalog 在得到guid后，需要通过base_assets_catalog查找guid所指向的文件存储在哪个压缩包（bundle）内
    base_assets_catalog = 'api/file/base_assets_catalog.json'

    main(dbf_CARD, cards_map, base_assets_catalog)

