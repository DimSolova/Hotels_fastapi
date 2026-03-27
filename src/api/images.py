from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.services.images import ImagesService

router = APIRouter(prefix="/images", tags=["Images hotels"])


@router.post("")
def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    ImagesService().upload_images(file, background_tasks)
