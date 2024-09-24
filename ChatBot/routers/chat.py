from fastapi import APIRouter, File, HTTPException, UploadFile, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, ChatHistory, ChatThread
from openai_utils import get_openai_response, summarize_text, transcribe_audio, create_upload_file, create_response, translator
import os
import aiofiles

router = APIRouter()

@router.post("/chat/threads",status_code=status.HTTP_200_OK)
async def create_thread(username: str, thread_name: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = User(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)

    thread = ChatThread(user_id=user.id, thread_name=thread_name)
    db.add(thread)
    db.commit()
    db.refresh(thread)

    return create_response(success=True, payload={"thread_id": thread.id, "thread_name": thread.thread_name}, code=status.HTTP_200_OK)


@router.post("/chat/threads/{thread_id}/messages", status_code=status.HTTP_200_OK)
async def chat(username: str, message: str, thread_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = User(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    thread = db.query(ChatThread).filter(ChatThread.id == thread_id, ChatThread.user_id == user.id).first()
    if not thread:
        return {"error": "Thread not found"}

    response = await get_openai_response(message)

    chat_history = ChatHistory(user_id=user.id, thread_id=thread.id, message=message, response=response)
    db.add(chat_history)
    db.commit()

    return create_response(success=True, payload={"message": message, "response": response, "thread_id": thread.id}, code=status.HTTP_200_OK)


@router.post("/summary", status_code=status.HTTP_200_OK)
async def summary(file: UploadFile):
    try:
        response = await create_upload_file(file)
        
        return create_response(success=True, payload={"response": response}, code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=500, detail=create_response(success=False, error={"code": 500, "message": str(e)}))


@router.post("/translate",status_code=status.HTTP_200_OK)
async def translate(language1: str, language2: str, message : str):
    try:
        translated_message = await translator(language1, language2, message)
        return create_response(success=True, payload={"translated_message":translated_message}, code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/speech-to-summary", status_code=status.HTTP_200_OK)
async def speech_to_text(file: UploadFile = File(...)):
    try:
        upload_dir = "uploaded_files"
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, file.filename)
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        transcription = await transcribe_audio(file_path)
        summary = await summarize_text(transcription)

        os.remove(file_path)
        return create_response(success=True, payload={"speech-summary":summary}, code=status.HTTP_200_OK)

    except Exception as e:
        raise HTTPException(status_code=500, detail=create_response(success=False, error={"code": 500, "message": str(e)}))