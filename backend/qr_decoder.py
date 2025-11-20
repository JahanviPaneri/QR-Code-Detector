import io
from typing import Optional

import cv2
import numpy as np
from PIL import Image


def decode_qr_bytes(raw_bytes: bytes) -> Optional[str]:
    """
    Decodes a QR code payload from image bytes using OpenCV.
    Returns the text payload (commonly a URL) or None if decoding fails.
    """
    if not raw_bytes:
        return None

    np_arr = np.frombuffer(raw_bytes, dtype=np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if image is None:
        # Attempt via Pillow fallback
        try:
            pil_image = Image.open(io.BytesIO(raw_bytes))
            rgb = cv2.cvtColor(np.array(pil_image.convert('RGB')), cv2.COLOR_RGB2BGR)
            image = rgb
        except Exception:
            return None

    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(image)
    payload = data.strip() if data else None
    return payload or None

