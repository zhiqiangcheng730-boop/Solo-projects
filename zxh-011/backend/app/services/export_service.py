from io import BytesIO

from sqlalchemy.orm import Session
from fpdf import FPDF
from ..models import Item, RenovationPlan, ProgressStep


class ExportService:
    def __init__(self, db: Session):
        self.db = db

    def export_plan_pdf(self, plan_id: int) -> BytesIO | None:
        plan = self.db.query(RenovationPlan).filter(RenovationPlan.id == plan_id).first()
        if not plan:
            return None
        item = self.db.query(Item).filter(Item.id == plan.item_id).first()
        steps = self.db.query(ProgressStep).filter(
            ProgressStep.item_id == plan.item_id
        ).order_by(ProgressStep.step_order).all()

        pdf = FPDF()
        pdf.add_page()
        # Use built-in font that supports CJK or fall back
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVu", "", 16)
        pdf.cell(0, 10, plan.title, ln=True)
        pdf.set_font("DejaVu", "", 12)
        pdf.cell(0, 10, f"Original item: {item.title if item else 'N/A'}", ln=True)
        pdf.ln(5)
        pdf.set_font("DejaVu", "", 11)
        pdf.multi_cell(0, 8, plan.content)
        pdf.ln(5)
        pdf.cell(0, 10, f"Progress steps: {len(steps)}", ln=True)
        buf = BytesIO()
        pdf.output(buf)
        buf.seek(0)
        return buf
