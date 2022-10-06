def get_teams(handbook_team_table: dict) -> dict:
    return handbook_team_table

def get_professions() -> dict:
    return {
        'CASTER': {
            'professionId': 'CASTER',
            'professionName': '术师'
        },
        'MEDIC': {
            'professionId': 'MEDIC',
            'professionName': '医疗'
        },
        'PIONEER': {
            'professionId': 'PIONEER',
            'professionName': '先锋'
        },
        'SNIPER': {
            'professionId': 'SNIPER',
            'professionName': '狙击'
        },
        'SPECIAL': {
            'professionId': 'SPECIAL',
            'professionName': '特种'
        },
        'SUPPORT': {
            'professionId': 'SUPPORT',
            'professionName': '辅助'
        },
        'TANK': {
            'professionId': 'TANK',
            'professionName': '先锋'
        },
        'WARRIOR': {
            'professionId': 'WARRIOR',
            'professionName': '近卫'
        }
    }


def get_subprofessions(uniequip_table: dict) -> dict:
    return uniequip_table['subProfDict']
