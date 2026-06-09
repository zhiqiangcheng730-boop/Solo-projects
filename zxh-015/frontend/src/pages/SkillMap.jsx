import { useState, useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
import { locationApi } from '../api'

function MapUpdater({ center }) {
  const map = useMap()
  useEffect(() => { map.setView(center, map.getZoom()) }, [center])
  return null
}

export default function SkillMap() {
  const [city, setCity] = useState('')
  const [markers, setMarkers] = useState([])
  const [center, setCenter] = useState([39.9, 116.4])
  const [loading, setLoading] = useState(false)
  const [mode, setMode] = useState('city')

  const handleCitySearch = async () => {
    if (!city.trim()) return
    setLoading(true)
    try {
      const { data } = await locationApi.citySkills(city)
      setMarkers(data.filter((m) => m.lat && m.lon))
      if (data.length > 0) {
        const lats = data.filter((m) => m.lat).map((m) => m.lat)
        const lons = data.filter((m) => m.lon).map((m) => m.lon)
        if (lats.length) setCenter([lats[0], lons[0]])
      }
    } catch { /* ignore */ }
    setLoading(false)
  }

  const handleNearby = () => {
    if (!navigator.geolocation) return
    setLoading(true)
    navigator.geolocation.getCurrentPosition(async (pos) => {
      try {
        const { lat, lon } = { lat: pos.coords.latitude, lon: pos.coords.longitude }
        const { data } = await locationApi.nearby(lat, lon, 20, 30)
        setMarkers(data)
        setCenter([lat, lon])
      } catch { /* ignore */ }
      setLoading(false)
    })
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-800 mb-4">技能地图</h2>
      <p className="text-sm text-gray-400 mb-4">
        仅显示大区域级别的位置信息，保护用户隐私
      </p>

      <div className="flex gap-3 mb-4 flex-wrap">
        <button onClick={() => setMode('city')} className={`px-3 py-1.5 rounded-lg text-sm ${mode === 'city' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-500 border'}`}>
          按城市查看
        </button>
        <button onClick={() => { setMode('nearby'); handleNearby() }} className={`px-3 py-1.5 rounded-lg text-sm ${mode === 'nearby' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-500 border'}`}>
          查看附近
        </button>
      </div>

      {mode === 'city' && (
        <div className="flex gap-2 mb-3">
          <input
            className="border border-gray-200 rounded-lg p-2 text-sm w-48"
            placeholder="输入城市名..."
            value={city}
            onChange={(e) => setCity(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleCitySearch()}
          />
          <button onClick={handleCitySearch} className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-indigo-700">
            {loading ? '搜索中...' : '搜索'}
          </button>
        </div>
      )}

      <div className="h-96 rounded-xl overflow-hidden border border-gray-200">
        <MapContainer center={center} zoom={12} style={{ height: '100%', width: '100%' }}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <MapUpdater center={center} />
          {markers.map((m, i) => (
            <Marker key={i} position={[m.lat, m.lon]}>
              <Popup>
                <div className="text-sm">
                  <strong>{m.title}</strong>
                  <br />
                  {m.category} · {m.type === 'offer' ? '提供服务' : '寻求帮助'}
                  {m.is_urgent && <span className="text-red-500 ml-1">紧急</span>}
                  {m.distance_km && <><br />距离: {m.distance_km}km</>}
                  {m.provider_credit && <><br />信用: {m.provider_credit}</>}
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>

      {markers.length > 0 && (
        <div className="mt-4 space-y-2">
          <h3 className="font-semibold text-gray-700">附近技能 ({markers.length})</h3>
          {markers.map((m, i) => (
            <div key={i} className="bg-white rounded-lg border border-gray-200 p-3 flex items-center justify-between">
              <div>
                <span className="font-medium text-gray-800 text-sm">{m.title}</span>
                <span className="text-xs text-gray-400 ml-2">{m.category}</span>
              </div>
              <div className="text-xs text-gray-400">
                {m.distance_km && <span>{m.distance_km}km</span>}
                {m.is_urgent && <span className="text-red-500 ml-2">紧急</span>}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
