from enum import Enum, auto

class Resource(Enum):
    QI = "Qi"
    SHIELD = "Shield"
    SPARK = "Spark"
    BATTERY = "Battery"
    DUCK = "Duck"

class Move(Enum):
    # Basic
    QI = "气"
    SHIELD = "盾"
    
    # Qi Attacks
    GI = "gi"
    PO = "破"
    LENG_FENG = "冷风"
    RU_LAI = "如来"
    HEI_DONG = "黑洞"
    
    # Element Attacks
    XIAO_HUO = "小火"
    SHAN_DIAN = "闪电"
    DA_HUO = "大火"
    SHINING = "Shining"
    
    # Special Defense/Counter
    SHAN = "闪"
    CHI = "吃"
    SHUANG_CHI = "双吃"
    SHI_ZI_FANG = "十字防"

# Resource Costs
MOVE_COSTS = {
    Move.QI: {},
    Move.SHIELD: {},
    Move.GI: {Resource.QI: 1},
    Move.PO: {Resource.QI: 2},
    Move.LENG_FENG: {Resource.QI: 3},
    Move.RU_LAI: {Resource.QI: 5},
    Move.HEI_DONG: {Resource.QI: 8},
    Move.XIAO_HUO: {Resource.SHIELD: 2},
    Move.SHAN_DIAN: {Resource.SHIELD: 3},
    Move.DA_HUO: {Resource.SHIELD: 4},  # Or 2 Sparks
    Move.SHINING: {Resource.SHIELD: 6}, # Or 2 Batteries
    Move.SHAN: {Resource.DUCK: 1},
    Move.CHI: {Resource.QI: 1},
    Move.SHUANG_CHI: {Resource.QI: 2},
    Move.SHI_ZI_FANG: {Resource.QI: 2},
}

# Attack Power Ranking (Higher is better)
# 黑洞 > Shining = 如来 > 大火 = 冷风 > 闪电 = 破 > 小火 > gi
ATTACK_POWER = {
    Move.HEI_DONG: 90,
    Move.SHINING: 80,
    Move.RU_LAI: 80,
    Move.DA_HUO: 70,
    Move.LENG_FENG: 70,
    Move.SHAN_DIAN: 60,
    Move.PO: 60,
    Move.XIAO_HUO: 50,
    Move.GI: 40,
}

ATTACK_MOVES = set(ATTACK_POWER.keys())

# Moves that kill Shield (Stronger or equal to Po)
# 破(60), 闪电(60), ...
SHIELD_KILLERS = {m for m, p in ATTACK_POWER.items() if p >= ATTACK_POWER[Move.PO]}

# Moves that kill ShiZiFang (Stronger or equal to RuLai)
# 如来(80), Shining(80), 黑洞(90)
SHI_ZI_FANG_KILLERS = {m for m, p in ATTACK_POWER.items() if p >= ATTACK_POWER[Move.RU_LAI]}
