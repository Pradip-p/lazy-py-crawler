from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr
from lazy_crawler.api.services.email_service import send_contact_email

router = APIRouter(prefix="/contact", tags=["contact"])


class ContactForm(BaseModel):
    full_name: str
    email: EmailStr
    message: str


@router.post("")
async def submit_contact_form(form: ContactForm, background_tasks: BackgroundTasks):
    """
    Handles contact form submission and sends an email in the background.
    """
    try:
        print("Contact form submitted:", form)
        background_tasks.add_task(
            send_contact_email,
            full_name=form.full_name,
            email=form.email,
            message=form.message,
        )
        return {"message": "Thank you! Your message has been sent."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
