import torch as tt
from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
from qwen_vl_utils import process_vision_info
from skimage.transform import resize
import numpy as np
from PIL import Image as PILImage


def get_model_and_processor(model_id, max_pixels, device='mps'):
    
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        model_id,
        torch_dtype=tt.bfloat16,
        #device_map="auto",
        ).to(device)


    # Get the processor
    processor = AutoProcessor.from_pretrained(model_id,
                                              min_pixels=max_pixels,
                                              max_pixels=max_pixels)

    return model, processor


def format_data(image, system_message):
    # Construct the system message
    system_content = [
        {
            "type": "text",
            "text": system_message
        }
    ]

    # Construct the user message with separate image entries
    user_content = []
    user_content.append({
                "type": "image",
                "image": image
            })

    # Return the formatted data
    return {
        "messages": [
            {
                "role": "system",
                "content": system_content
            },
            {
                "role": "user",
                "content": user_content
            },
        ]
    }

def generate_description(image, model, processor, system_message, max_new_tokens=32, scale_factor=1):
    # Scale the image
    image = resize(image, (image.shape[0] * scale_factor, image.shape[1] * scale_factor), anti_aliasing=True)

    image = image * 255
    image = image.astype(np.uint8)
    image = PILImage.fromarray(image)

    sample = format_data(image, system_message)

    text = processor.apply_chat_template(
        sample["messages"], tokenize=False, add_generation_prompt=True
    )
    image_inputs, _ = process_vision_info(sample["messages"])

    inputs = processor(
        text=[text],
        images=image_inputs,
        padding=True,
        return_tensors="pt",
        do_resize=False,
    )
    inputs = inputs.to(model.device)
    
    # Inference: Generation of the output
    with tt.no_grad():
        generated_ids = model.generate(
            **inputs, max_new_tokens=max_new_tokens, top_p=1.0, do_sample=True, temperature=0.1
        )
    generated_ids_trimmed = [
        out_ids[len(in_ids):]
        for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )
    return output_text[0], text 