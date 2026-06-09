from collections import defaultdict
from sqlalchemy.orm import Session
from ..models.marker import Marker


def generate_heatmap(
    db: Session,
    south: float,
    north: float,
    east: float,
    west: float,
    grid_size: float = 0.01,
    category: str | None = None,
) -> list[dict]:
    q = db.query(Marker).filter(
        Marker.latitude >= south,
        Marker.latitude <= north,
        Marker.longitude >= west,
        Marker.longitude <= east,
    )
    if category:
        q = q.filter(Marker.category == category)

    markers = q.all()
    grid: dict[tuple[int, int], float] = defaultdict(float)

    for m in markers:
        row = int((m.latitude - south) / grid_size)
        col = int((m.longitude - west) / grid_size)
        grid[(row, col)] += 1 + m.vote_count * 0.5

    return [
        {
            "lat": south + r * grid_size + grid_size / 2,
            "lng": west + c * grid_size + grid_size / 2,
            "weight": min(weight, 50),
        }
        for (r, c), weight in grid.items()
    ]
