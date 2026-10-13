from pathlib import Path
from uuid import uuid4

import aiofiles
from fastapi import UploadFile

UPLOAD_DIR = Path("uploads/resumes")
CHUNK_SIZE = 1024 * 1024            # 1 MB


async def save_file(file: UploadFile) -> str:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # unique name, extension fixed by us 
    file_path = UPLOAD_DIR / f"{uuid4().hex}.pdf"

    async with aiofiles.open(file_path, "wb") as output:
        while chunk := await file.read(CHUNK_SIZE):
            await output.write(chunk)

    await file.close()

    return file_path.as_posix()