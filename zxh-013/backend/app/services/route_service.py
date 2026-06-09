from math import radians, cos, sin, atan2
from sqlalchemy.orm import Session
from ..models.marker import Marker
from ..utils import haversine
from ..constants import AVOID_CATEGORIES

STEP_KM = 0.5


def _interpolate_path(start_lat, start_lng, end_lat, end_lng, step_km=STEP_KM):
    dist = haversine(start_lat, start_lng, end_lat, end_lng)
    steps = max(1, int(dist / step_km))
    path = []
    for i in range(steps + 1):
        frac = i / steps
        path.append({
            "lat": start_lat + (end_lat - start_lat) * frac,
            "lng": start_lng + (end_lng - start_lng) * frac,
        })
    return path


def optimize_route(db: Session, start_lat, start_lng, end_lat, end_lng):
    direct_path = _interpolate_path(start_lat, start_lng, end_lat, end_lng)

    mid_lat = (start_lat + end_lat) / 2
    mid_lng = (start_lng + end_lng) / 2
    span = haversine(start_lat, start_lng, end_lat, end_lng) / 2 + 1

    lat_deg = span / 111
    lng_deg = span / (111 * cos(radians(mid_lat)))

    avoid_markers = (
        db.query(Marker)
        .filter(
            Marker.category.in_(AVOID_CATEGORIES),
            Marker.latitude >= mid_lat - lat_deg,
            Marker.latitude <= mid_lat + lat_deg,
            Marker.longitude >= mid_lng - lng_deg,
            Marker.longitude <= mid_lng + lng_deg,
        )
        .all()
    )

    if not avoid_markers:
        return {"direct_path": direct_path, "optimized_path": direct_path, "avoided_markers": 0}

    waypoints = []
    for m in avoid_markers:
        bearing = atan2(m.longitude - mid_lng, m.latitude - mid_lat)
        offset_lat = m.latitude + cos(bearing) * 0.005
        offset_lng = m.longitude + sin(bearing) * 0.005
        waypoints.append((offset_lat, offset_lng))

    optimized_path = []
    remaining = [start_lat, start_lng]
    for wp in waypoints:
        optimized_path.extend(_interpolate_path(remaining[0], remaining[1], wp[0], wp[1]))
        remaining = [wp[0], wp[1]]
    optimized_path.extend(_interpolate_path(remaining[0], remaining[1], end_lat, end_lng))

    return {
        "direct_path": direct_path,
        "optimized_path": optimized_path,
        "avoided_markers": len(avoid_markers),
    }
