from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, Request, WebSocket, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .database import get_db, engine
from . import crud, models, schemas
import datetime

templates = Jinja2Templates(directory="templates")

router = APIRouter(tags=['APIs User'])

# models.Base.metadata.create_all(bind=engine)


@router.get('/', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def get_page_home(request: Request, db: Session = Depends(get_db)):
    """page home"""
    return templates.TemplateResponse('home.html', {"request": request})


@router.get('/users', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def get_page_users(request: Request, db: Session = Depends(get_db)):
    """page users"""
    users = crud.get_users(db=db)
    return templates.TemplateResponse('users.html', {"request": request, 'users': users})


@router.post('/registration', response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
async def create_new_user(request: Request, db: Session = Depends(get_db)):
    """register new user"""
    form_create_user = schemas.FormCreateUser(request=request)
    await form_create_user.load_data()
    new_user = schemas.User(**form_create_user.__dict__)
    new_user = crud.create_user(db=db, user=new_user)
    return '/users'


@router.get('/user-logs', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def get_page_user_logs(request: Request, db: Session = Depends(get_db)):
    """page user logs"""
    user_logs = crud.get_user_logs(db=db)
    return templates.TemplateResponse('users-log.html', {"request": request, 'user_logs': user_logs})


@router.get('/read-card', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def get_page_read_card(request: Request, db: Session = Depends(get_db)):
    """page read card"""
    return templates.TemplateResponse('read-card.html', {"request": request})


@router.post('/send-card-id/{card_id}', status_code=status.HTTP_200_OK)
async def send_card_id(card_id: str, db: Session = Depends(get_db)):
    """retrive card id from client"""
    card_id = card_id.replace('_', ' ')
    for client in waiting_clients_for_fil_card_id:
        print(client.url)
        await client.send_text(card_id)
    # Check user is already exist
    check_user = crud.get_user_by_card_id(db=db, card_id=card_id)
    print("check user: ", check_user)
    if check_user is None:
        raise HTTPException(
            status_code=403, detail="User is not already exists.")
    print("next")
    # Check card in user logs
    check_card = crud.check_card_in_user_logs(db=db, user_id=check_user.id)
    print("check card: ", check_card)
    if check_card is None:
        new_user_checkin = schemas.UserCheckin(
            user_id=check_user.id,
            checkin_date=datetime.datetime.now().strftime('%Y-%m-%d'),
            time_in=datetime.datetime.now().strftime('%H:%M:%S')
        )
        payload = crud.checkin_user(
            db=db, user_checkin=new_user_checkin)
    else:
        payload = crud.checkout_user(db=db, id=check_card.id)

    for client in waiting_clients_for_read_card:
        await client.send_json(payload.as_dict())
    return "oke"


@router.delete('/truncate-user-logs')
def truncate_user_log(db: Session = Depends(get_db)):
    """truncate table"""
    return crud.truncate_user_logs(db=db)


"""Socket"""

waiting_clients_for_fil_card_id = []
waiting_clients_for_read_card = []


@router.websocket("/read-card")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    waiting_clients_for_read_card.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except Exception as e:
        print(f"WebSocket connection closed: {e}")
    finally:
        waiting_clients_for_read_card.remove(websocket)


@router.websocket("/fil-card-id")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    waiting_clients_for_fil_card_id.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except Exception as e:
        print(f"WebSocket connection closed: {e}")
    finally:
        waiting_clients_for_fil_card_id.remove(websocket)
