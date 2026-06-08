/**
 * 心情与推荐字体映射配置
 * 每个心情对应 3 款 Google Fonts 推荐字体及其备选回退字体
 */
export const MOODS = [
  { id: 'happy',   label: '开心', emoji: '😊' },
  { id: 'sad',     label: '悲伤', emoji: '😢' },
  { id: 'angry',   label: '愤怒', emoji: '😠' },
  { id: 'calm',    label: '平静', emoji: '😌' },
]

export const MOOD_FONT_MAP = {
  happy: [
    { family: 'ZCOOL KuaiLe',   fallback: 'cursive',    label: '站酷快乐体',   tag: '圆润可爱' },
    { family: 'Liu Jian Mao Cao', fallback: 'cursive',   label: '刘健毛草体',   tag: '洒脱手写' },
    { family: 'Zhi Mang Xing',  fallback: 'cursive',     label: '逐浪行楷',     tag: '灵动活泼' },
  ],
  sad: [
    { family: 'Noto Serif SC',  fallback: 'serif',       label: '思源宋体',     tag: '沉静衬线' },
    { family: 'Ma Shan Zheng',  fallback: 'serif',        label: '马山正体',     tag: '清瘦细长' },
    { family: 'Long Cang',      fallback: 'serif',        label: '龙藏体',       tag: '素雅纤细' },
  ],
  angry: [
    { family: 'ZCOOL QingKe HuangYou', fallback: 'sans-serif', label: '站酷庆科黄油体', tag: '厚重刚硬' },
    { family: 'Ma Shan Zheng',  fallback: 'serif',        label: '马山正体',     tag: '粗犷有力' },
    { family: 'Noto Sans SC',   fallback: 'sans-serif',   label: '思源黑体',     tag: '锐利直接' },
  ],
  calm: [
    { family: 'ZCOOL XiaoWei',  fallback: 'sans-serif',   label: '站酷小微体',   tag: '柔和简洁' },
    { family: 'Noto Sans SC',   fallback: 'sans-serif',    label: '思源黑体',     tag: '平稳中性' },
    { family: 'Liu Jian Mao Cao', fallback: 'cursive',     label: '刘健毛草体',   tag: '淡然写意' },
  ],
}
