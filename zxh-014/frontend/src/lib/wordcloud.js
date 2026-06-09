import cloud from "d3-cloud";

/**
 * Render a word cloud onto a canvas element.
 * @param {HTMLCanvasElement} canvas
 * @param {Array<{keyword: string, count: number}>} words
 */
export function renderWordCloud(canvas, words) {
  if (!words || words.length === 0) return;

  const width = canvas.parentElement?.clientWidth || 600;
  const height = 400;
  canvas.width = width;
  canvas.height = height;

  const maxCount = Math.max(...words.map((w) => w.count), 1);
  const minCount = Math.min(...words.map((w) => w.count), 1);

  const fontSize = (count) => {
    const ratio = (count - minCount) / (maxCount - minCount || 1);
    return 14 + ratio * 36;
  };

  const layout = cloud()
    .size([width, height])
    .words(
      words.map((w) => ({
        text: w.keyword,
        size: fontSize(w.count),
        count: w.count,
      }))
    )
    .padding(4)
    .rotate(() => 0)
    .font("PingFang SC, Microsoft YaHei, sans-serif")
    .fontSize((d) => d.size)
    .on("end", draw);

  layout.start();

  function draw(layoutWords) {
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, width, height);

    const colors = [
      "#1e3a5f", "#2d6a4f", "#6b4c8a", "#b91c1c",
      "#92400e", "#0f766e", "#7c3aed", "#db2777",
    ];

    layoutWords.forEach((w, i) => {
      ctx.fillStyle = colors[i % colors.length];
      ctx.font = `${w.size}px PingFang SC, Microsoft YaHei, sans-serif`;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(w.text, w.x + width / 2, w.y + height / 2);
    });
  }
}
