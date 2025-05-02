"""
Do inference with EasyOCR
"""

import pandas as pd
import easyocr
import numpy as np
from qwen_helper_funcs import prep_image

reader = easyocr.Reader(["en"])


def inference_easyocr(image_bytes, display_image=False):
    pil_image = prep_image(image_bytes)
    image_array = np.array(pil_image)
    result = reader.readtext(image_array, detail=0)
    if display_image:
        pil_image.show()
    return result[0] if len(result) > 0 else ""
