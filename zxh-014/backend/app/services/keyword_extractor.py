"""Simple word-bank based dream keyword extraction."""

# Curated dream symbol word bank with categories
DREAM_SYMBOLS: set[str] = {
    # 自然元素
    "水", "火", "风", "土", "雨", "雪", "雷电", "洪水", "大海", "河流",
    "湖泊", "瀑布", "沙漠", "森林", "山", "天空", "云", "星星", "月亮", "太阳",
    "黑暗", "光", "雾", "彩虹", "地震", "风暴",
    # 动物
    "蛇", "猫", "狗", "鱼", "鸟", "马", "老虎", "狮子", "狼", "蜘蛛",
    "老鼠", "蝴蝶", "龙", "兔子", "熊", "鹰", "鲨鱼", "蚂蚁", "蜜蜂",
    # 身体
    "牙齿", "眼睛", "头发", "手", "脚", "脸", "血液", "伤口", "裸体",
    # 动作/状态
    "掉落", "飞翔", "坠落", "漂浮", "奔跑", "追逐", "逃跑", "游泳",
    "爬行", "跳跃", "跌倒", "哭泣", "笑", "喊叫", "沉默", "窒息",
    "迷路", "被困", "寻找", "等待", "拥抱", "亲吻", "打架",
    # 场景/物品
    "房子", "家", "学校", "医院", "墓地", "教堂", "监狱", "桥",
    "车", "火车", "飞机", "船", "电梯", "楼梯", "门", "窗",
    "镜子", "电话", "钟表", "钥匙", "钱", "食物", "水杯", "刀",
    "书", "信件", "照片", "戒指", "衣服", "鞋", "床",
    # 人物
    "母亲", "父亲", "孩子", "伴侣", "朋友", "陌生人", "老师", "医生",
    "警察", "怪物", "鬼", "天使", "自己", "影子",
    # 情景
    "考试", "婚礼", "葬礼", "战争", "旅行", "怀孕", "重生",
    "死亡", "复活",
}


class KeywordExtractor:
    """Extract dream symbols from text using word-bank matching."""

    @staticmethod
    def extract(content: str) -> list[dict]:
        """Extract keywords from dream content. Returns list of {keyword, frequency}."""
        keyword_counts: dict[str, int] = {}
        for symbol in DREAM_SYMBOLS:
            count = content.count(symbol)
            if count > 0:
                keyword_counts[symbol] = count
        return [
            {"keyword": kw, "frequency": freq}
            for kw, freq in sorted(
                keyword_counts.items(), key=lambda x: x[1], reverse=True
            )
        ]

    @staticmethod
    def get_symbol_bank() -> list[str]:
        return sorted(DREAM_SYMBOLS)
