from fastapi import UploadFile, APIRouter
import shutil
from app.tasks.tasks import process_pic


router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"],
)


@router.post("/images")
async def add_image(name: int, fail: UploadFile):
    im_path = f"app/static/images/{name}.webp"
    with open(im_path, "wb+") as file_obj:
        shutil.copyfileobj(fail.file, file_obj)

    # Запускаем фоном задачу для обработки картинки
    process_pic.delay(im_path)