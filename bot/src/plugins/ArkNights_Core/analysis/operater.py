def get_operators(character_table: dict, char_patch_table: dict = None) -> dict:
    '''
        为插入operator数据库整合数据
        retrun: 干员
    '''
    operators = {k:v for k, v in character_table.items() if v['itemObtainApproach'] is not None}
    if char_patch_table is not None:
        sword_amiya = char_patch_table['patchChars']
        sword_amiya['char_1001_amiya2']['name'] = '阿米娅(近卫)'
        operators.update(char_patch_table['patchChars'])
    return operators