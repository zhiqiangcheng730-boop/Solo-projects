from __future__ import annotations
from ..models.statistics import StatisticsModel


class StatisticsService:
    def __init__(self, conn):
        self.conn = conn
        self.model = StatisticsModel

    def dashboard(self):
        return self.model.dashboard(self.conn)

    def heatmap_all(self):
        return self.model.heatmap_all(self.conn)
