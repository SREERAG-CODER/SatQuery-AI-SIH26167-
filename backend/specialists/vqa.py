from transformers import BlipProcessor, BlipForQuestionAnswering
from PIL import Image
import rasterio
import numpy as np

processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")

def load_image(image_path):

    with rasterio.open(image_path) as src:
        data = src.read(
            1,
            out_shape=(512, 512)
        )

    data = np.nan_to_num(data)

    minimum = data.min()
    maximum = data.max()

    if maximum > minimum:
        data = (data - minimum) / (maximum - minimum)

    data = (data * 255).astype(np.uint8)

    return Image.fromarray(data).convert("RGB")


def answer_question(image_path, question):

    image = load_image(image_path)

    inputs = processor(
        images=image,
        text=question,
        return_tensors="pt"
    )

    output = model.generate(**inputs)

    answer = processor.decode(
        output[0],
        skip_special_tokens=True
    )

    return answer