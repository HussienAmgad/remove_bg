from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
import httpx
from PIL import Image
from io import BytesIO
from rembg import remove, new_session

app = FastAPI(title="Free Background Remover API", version="1.0.0")

# Load the model session once for better performance
session = new_session()  # default U2Net

@app.get("/health")
async def health():
    return {"status": "ok"}

async def fetch_image(url: str) -> Image.Image:
    # Download the image
    async with httpx.AsyncClient(follow_redirects=True, timeout=20.0) as client:
        try:
            resp = await client.get(url)
            resp.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to download image: {e}")

        # Validate it's an image by attempting to open it
        try:
            img = Image.open(BytesIO(resp.content))
            # Ensure consistent mode for alpha support
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            return img
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"URL is not a valid image: {e}")

@app.get("/remove")
async def remove_bg(
    url: str = Query(..., description="Direct URL to an image"),
    format: str = Query("png", pattern="^(png|webp)$", description="Output format: png or webp"),
    download: int = Query(0, description="Set to 1 to force file download"),
):
    """
    Example:
    /remove?url=https://example.com/cat.jpg&format=png&download=1
    """
    img = await fetch_image(url)
    # Remove background
    out_img = remove(img, session=session)

    # Prepare buffer
    buf = BytesIO()
    if format == "png":
        out_img.save(buf, format="PNG")
        media_type = "image/png"
        ext = "png"
    else:
        out_img.save(buf, format="WEBP")
        media_type = "image/webp"
        ext = "webp"
    buf.seek(0)

    headers = {}
    if download:
        headers["Content-Disposition"] = f'attachment; filename="removed_bg.{ext}"'

    return StreamingResponse(buf, media_type=media_type, headers=headers)

@app.get("/")
def root():
    return {
        "info": "Use /remove?url=...&format=png|webp&download=1",
        "examples": [
            "/remove?url=https://images.unsplash.com/photo-1544005313-94ddf0286df2",
            "/remove?url=https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg&format=webp&download=1",
        ],
    }
