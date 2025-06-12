from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import smtplib
import tempfile
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models.pop import POP
from app.schemas.pop_schema import POPCreate
from config import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def send_pop_approval_email(pop: dict, recipient_email: EmailStr, pdf_path: str):
    print("🔄 Enviando e-mail com PDF...")

    data_formatada = pop["date"].strftime("%d/%m/%Y")

    subject = "Nova solicitação de POP para aprovação"
    body = f"""
    <p>Uma nova solicitação de POP foi criada.</p>
    <ul>
        <li><strong>Curso:</strong> {pop['curso']}</li>
        <li><strong>Disciplina:</strong> {pop['disciplina']}</li>
        <li><strong>Protocolo:</strong> {pop['protocolo']}</li>
        <li><strong>Docente:</strong> {pop['docente_nome']}</li>
        <li><strong>Receita:</strong> {pop['recipe_name']}</li>
        <li><strong>Data:</strong> {data_formatada}</li>
    </ul>
    <p>Acesse o sistema para aprovar ou rejeitar.</p>
    """

    # Criar mensagem multipart
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_ADDRESS
    msg["To"] = recipient_email

    # Adiciona o corpo HTML
    msg.attach(MIMEText(body, "html"))

    # Adiciona o PDF
    try:
        with open(pdf_path, "rb") as f:
            pdf = MIMEApplication(f.read(), _subtype="pdf")
            pdf.add_header('Content-Disposition', 'attachment', filename="pop.pdf")
            msg.attach(pdf)
    except FileNotFoundError:
        print(f"❌ Arquivo PDF '{pdf_path}' não encontrado.")
        return

    # Envia o e-mail
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
            server.send_message(msg)
        print("✅ E-mail com PDF enviado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")
        
def generate_pop_pdf(pop: dict) -> str:
    if not os.path.exists("tmp"):
        os.makedirs("tmp")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir="tmp", mode="w+b") as temp_file:
        data_formatada = pop["date"].strftime("%d/%m/%Y")
        
        c = canvas.Canvas(temp_file.name, pagesize=A4)
        c.setFont("Helvetica", 12)
        c.drawString(50, 800, "Solicitação de POP")
        c.drawString(50, 780, f"Curso: {pop['curso']}")
        c.drawString(50, 760, f"Disciplina: {pop['disciplina']}")
        c.drawString(50, 740, f"Protocolo: {pop['protocolo']}")
        c.drawString(50, 720, f"Docente: {pop['docente_nome']}")
        c.drawString(50, 700, f"Receita: {pop['recipe_name']}")
        c.drawString(50, 680, f"Data: {data_formatada}")
        c.save()
        return temp_file.name


def create_pop_service(pop_data: POPCreate, db: Session) -> POP:
    """
    Create a new POP entry in the database.
    """
    new_pop = POP(**pop_data.dict())
    db.add(new_pop)
    db.commit()
    db.refresh(new_pop)
    return new_pop


def list_pops_service(db: Session):
    """
    List all POP entries in the database.
    """
    return db.query(POP).all()


# def check_pop_service(data: POPCheckRequest, db: Session) -> POPCheckResponse:
#     recipe = db.query(Recipe).filter(Recipe.id == data.recipe_id).first()
#     if not recipe:
#         return POPCheckResponse(
#             available={},
#             missing={},
#             status="recipe not found"
#         )

#     requested_quantity = data.requested_quantity or 1

#     available_items = {}
#     missing_items = {}

#     for ingredient in recipe.ingredients:
#         item = db.query(Item).filter(Item.id == ingredient["item_id"]).first()
#         if not item:
#             missing_items[f"Item ID {ingredient['item_id']}"] = float(ingredient["quantity"]) * requested_quantity
#             continue

#         required_quantity = float(ingredient["quantity"]) * requested_quantity

#         stock_sum = db.query(func.sum(Stock.quantity)).filter(Stock.item_id == item.id).scalar() or 0

#         if stock_sum >= required_quantity:
#             available_items[item.name] = required_quantity
#         else:
#             missing_items[item.name] = required_quantity - stock_sum

#     status = "valid" if not missing_items else "missing items"

#     return POPCheckResponse(
#         available=available_items,
#         missing=missing_items,
#         status=status
#     )