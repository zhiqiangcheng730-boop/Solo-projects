const CHINA_PROVINCE_COORDS = {
  '北京': [116.46, 39.92], '天津': [117.20, 39.13], '上海': [121.47, 31.23],
  '重庆': [106.55, 29.57], '河北': [114.47, 38.03], '山西': [112.53, 37.87],
  '辽宁': [123.43, 41.80], '吉林': [125.32, 43.90], '黑龙江': [126.53, 45.80],
  '江苏': [118.78, 32.06], '浙江': [120.15, 30.28], '安徽': [117.28, 31.86],
  '福建': [119.30, 26.07], '江西': [115.90, 28.68], '山东': [117.00, 36.67],
  '河南': [113.65, 34.76], '湖北': [114.30, 30.60], '湖南': [112.97, 28.23],
  '广东': [113.27, 23.13], '海南': [110.35, 20.02], '四川': [104.07, 30.67],
  '贵州': [106.72, 26.57], '云南': [102.72, 25.05], '陕西': [108.95, 34.27],
  '甘肃': [103.73, 36.03], '青海': [101.74, 36.56], '台湾': [121.50, 25.05],
  '内蒙古': [111.67, 40.82], '广西': [108.33, 22.84], '西藏': [91.17, 29.65],
  '宁夏': [106.27, 38.47], '新疆': [87.62, 43.79], '香港': [114.17, 22.28],
  '澳门': [113.55, 22.19],
}

export function useMap() {
  function getCoord(province) {
    for (const [key, coord] of Object.entries(CHINA_PROVINCE_COORDS)) {
      if (province.includes(key) || key.includes(province)) return coord
    }
    return [113, 35]
  }

  function buildHeatmapData(stats) {
    if (!Array.isArray(stats)) return []
    return stats
      .filter(s => s.total > 0)
      .map(s => {
        const coord = getCoord(s.province)
        return {
          name: s.province,
          value: [...coord, Math.max(s.ratio * 100, 1)],
          ratio: s.ratio,
          total: s.total,
          understood: s.understood,
        }
      })
  }

  return { getCoord, buildHeatmapData, CHINA_PROVINCE_COORDS }
}
