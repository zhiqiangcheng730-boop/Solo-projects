const MAX_DIM = 800

/**
 * Convert an HTMLImageElement to a black/white silhouette data URL.
 * @param {HTMLImageElement} img
 * @param {number} threshold - 0..255, pixels above this become white, below become black
 * @returns {string} base64 data URL
 */
export function imageToSilhouette(img, threshold) {
  const { width, height } = fitDimensions(img.naturalWidth, img.naturalHeight, MAX_DIM)
  const canvas = document.createElement('canvas')
  canvas.width = width
  canvas.height = height

  const ctx = canvas.getContext('2d')
  ctx.drawImage(img, 0, 0, width, height)

  const imageData = ctx.getImageData(0, 0, width, height)
  const data = imageData.data

  for (let i = 0; i < data.length; i += 4) {
    const gray = 0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2]
    const value = gray > threshold ? 255 : 0
    data[i] = value
    data[i + 1] = value
    data[i + 2] = value
  }

  ctx.putImageData(imageData, 0, 0)
  return canvas.toDataURL('image/png')
}

export function imageToBase64(img) {
  const { width, height } = fitDimensions(img.naturalWidth, img.naturalHeight, MAX_DIM)
  const canvas = document.createElement('canvas')
  canvas.width = width
  canvas.height = height
  const ctx = canvas.getContext('2d')
  ctx.drawImage(img, 0, 0, width, height)
  return canvas.toDataURL('image/png')
}

function fitDimensions(nw, nh, max) {
  if (nw <= max && nh <= max) return { width: nw, height: nh }
  const ratio = max / Math.max(nw, nh)
  return { width: Math.round(nw * ratio), height: Math.round(nh * ratio) }
}

export function loadImageFromFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      const img = new Image()
      img.onload = () => resolve(img)
      img.onerror = () => reject(new Error('图片加载失败'))
      img.src = e.target.result
    }
    reader.onerror = () => reject(new Error('文件读取失败'))
    reader.readAsDataURL(file)
  })
}

export function loadImageFromBase64(base64) {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.onload = () => resolve(img)
    img.onerror = () => reject(new Error('图片加载失败'))
    img.src = base64
  })
}
