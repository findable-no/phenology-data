import io
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import random
from matplotlib.patches import Rectangle
from skimage.morphology import dilation, disk
from skimage.transform import resize
from PIL import Image as PILImage
import torch as tt
from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
from qwen_vl_utils import process_vision_info
import re
# Need some nifty functions to make this work

# Define coordinates in organized dictionaries
table_rows = [0, 85, 130, 180, 228, 270, 320, 365, 413, 455, 503, 550,
              595, 640, 690, 735, 784, 830, 871, 924, 972, 1017, 1064, 1110]
#table_rows_lower = [1187, 1281, 1329, 1377, 1423, 1467, 1516, 1560, 1609, \
#    1655, 1701, 1750, 1797, 1843, 1889, 1937, 1987, 2032, 2072, 2125, 2169, \
#        2219, 2269, 2315]

table_cols = [
    0, 95, 173, 257, 340, 420, 504, 581, 662, 747, 825, 905, 
    988, 1070, 1150, 1232, 1312, 1398, 1475, 1549, 1630
]


def dms_to_decimal(degrees, minutes, direction):
    if minutes == '':
        minutes = 0
    decimal = float(degrees) + float(minutes)/60
    if direction in ['S', 'W']:
        decimal *= -1
    return decimal


def parse_coordinates(coord_str):
    # Grab the relevant part of the string (latitude and longitude only)
    match = re.match(r'(\d+)[°′\'](\d{0,2})[°′\']{0,1}(N),\s*(\d+)[°′\'](\d{0,2})[°′\']{0,1}(E)', coord_str)
    if not match:
        raise ValueError("Invalid coordinate format")
    
    lat_deg, lat_decimals, lat_dir, lon_deg, lon_decimals, lon_dir = match.groups()
    
    if lat_decimals != '':
        latitude = float(lat_deg) + float(lat_decimals) / 10
    else:
        latitude = float(lat_deg)
    
    if lon_decimals != '':
        longitude = float(lon_deg) + float(lon_decimals) / 10
    else:
        longitude = float(lon_deg)
    
    return latitude, longitude

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


def show_selection(tables,
                   info_dict,
                   offset = 5,
                   figsize=(25, 25),
                   rotate = False,
                   selem_size = 1.5,
                   selection_size = 50,
                   subplot_size = (5, 10),
                   show_images = True,
                   table_rows = table_rows,
                   table_cols = table_cols,
                   use_dilation = False):
    
    # Get the coordinates from the info_dict
    start_r_idx = info_dict['row_start_idx']
    stop_r_idx = info_dict['row_end_idx']
    start_c_idx = info_dict['col_start_idx']
    stop_c_idx = info_dict['col_end_idx']

    start_r = table_rows[start_r_idx]
    stop_r = table_rows[stop_r_idx]
    start_c = table_cols[start_c_idx]
    stop_c = table_cols[stop_c_idx]

    # Select random table
    if selection_size is not None:
        indexes = np.random.choice(range(len(tables)), size=selection_size, replace=False)
    else:
        indexes = range(len(tables))
    images = []
    for table in tables:
        if not rotate:

            tmp_img = table[start_r:(stop_r + offset), start_c:(stop_c + offset)]

            # Normalize the image
            tmp_img = tmp_img - tmp_img.min()
            tmp_img = tmp_img / tmp_img.max()

            # Apply morphlogical grayscale dilation to increase contrast
            if use_dilation:
                selem = disk(selem_size)
                tmp_img = dilation(1 - tmp_img, selem)
                tmp_img = 1 - tmp_img

            images.append(tmp_img)
            
        else:

            tmp_img = table[start_r:(stop_r + offset), start_c:(stop_c + offset)]

            # Normalize the image
            tmp_img = tmp_img - tmp_img.min()
            tmp_img = tmp_img / tmp_img.max()

            tmp_img = np.rot90(tmp_img, k = 3)

            # Apply morphlogical grayscale dilation to increase contrast
            if use_dilation:
                selem = disk(selem_size)
                tmp_img = dilation(1 - tmp_img, selem)
                tmp_img = 1 - tmp_img

            images.append(tmp_img)

    # Plot the images
    if show_images:
        fig, axs = plt.subplots(subplot_size[0], subplot_size[1], figsize=figsize)
        for idx, random_idx in enumerate(indexes):
            axs[idx // subplot_size[1], idx % subplot_size[1]].imshow(images[random_idx], cmap='gray', vmin=0, vmax=1)
            axs[idx // subplot_size[1], idx % subplot_size[1]].axis('off')
        plt.show()

    # Return the images
    return images


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
        out_ids[len(in_ids) :]
        for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )
    return output_text[0], text


def img_to_bytes(image):
    image = 255 * image
    image = image.astype(np.uint8)
    image = PILImage.fromarray(image)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='TIFF')
    img_byte_str = img_byte_arr.getvalue()
    return img_byte_str


def bytes_to_img(img_byte_str):
    img_byte_arr = io.BytesIO(img_byte_str)
    image = PILImage.open(img_byte_arr)
    return image.convert("RGB")


# This function generates a dictionary of species and their phases
def generate_species_phase_dicts(species_list):
    species_phase_dicts = {}

    for species in species_list:
        if species['phases'] is None:
            # Directly add elements without phases
            key = '_'.join(species['english_name'].lower().split())
            species_phase_dicts[key] = {
                'norwegian_name': species['norwegian_name'],
                'english_name': species['english_name'],
                'latin_name': species['latin_name'],
                'phase': None,
                'row_start_idx': species['row_start_idx'],
                'row_end_idx': species['row_end_idx'],
                'col_start_idx': species['col_start_idx'],
                'col_end_idx': species['col_end_idx']
            }
        else:
            # Handle species with phases normally
            start_table_idx = species['row_start_idx']
            for phase in species['phases']:
                key = f'{"_".join(species["english_name"].lower().split())}_{phase}'
                species_phase_dicts[key] = {
                    'norwegian_name': species['norwegian_name'],
                    'english_name': species['english_name'],
                    'latin_name': species['latin_name'],
                    'phase': phase,
                    'row_start_idx': start_table_idx,
                    'row_end_idx': start_table_idx + 1,
                    'col_start_idx': species['col_start_idx'],
                    'col_end_idx': species['col_end_idx'],
                }
                start_table_idx += 1

    return species_phase_dicts

# This function show species and their phase information overlaid on a table
def visualize_observation_phases(image,
                                 observation_name,
                                 phase,
                                 observation_list,
                                 table_rows = table_rows,
                                 table_cols = table_cols,
                                 ax = None):
    """
    Visualize specified phase for a plant species by overlaying colored boxes on the image.
    
    Parameters:
    -----------
    image : numpy.ndarray
        Numpy array of the image normalized to 0...1.
    observation_name : str
        English name of the observation to visualize.
    phase : str
        Phase to visualize.
    observation_list : dict
        Dictionary containing observation information.
    table_rows : list of row indices.
    table_cols : list of column indices.
    Returns:
    --------
    None
        Displays the image with overlaid colored boxes.
    """
    # Verify the image is a valid numpy array
    if not isinstance(image, np.ndarray):
        raise ValueError("Input image must be a numpy array")

    # Check if the image is already normalized (values between 0 and 1)
    if np.max(image) > 1.1:  # Allow a small margin above 1 for floating-point errors
        # Normalize if needed
        image = image / 255.0

    # Find the species in the list
    observation_info = None
    for observation in observation_list.values():
        if observation['english_name'].lower() == observation_name.lower():
            if phase is None:
                observation_info = observation
                break
            else:
                if observation['phase'].lower() == phase.lower():
                    observation_info = observation
                    break

    if observation_info is None:
        raise ValueError(f"Species '{observation_name}' not found in the species list")

    # Create a figure and axis
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    ax.imshow(image, cmap='gray', vmin=0, vmax=1)

    # Generate random colors for each phase
    #r, g, b = [random.random() for _ in range(3)]
    r, g, b = (1.0, 0.0, 0.0)
    colors = (r, g, b, 0.3)

    # Calculate the row positions based on the phase
    upper_row_start = table_rows[observation_info['row_start_idx']]
    upper_row_end = table_rows[observation_info['row_end_idx']]
    # Get column positions
    col_start = table_cols[observation_info['col_start_idx']]
    col_end = table_cols[observation_info['col_end_idx']]

    # Create and add the rectangle
    rect = Rectangle((col_start, upper_row_start), col_end - col_start, upper_row_end - upper_row_start, 
                     linewidth=2, edgecolor=colors, facecolor=colors)
    ax.add_patch(rect)

    # Set title
    if phase is None:
        title = f"{observation_name}"
    else:
        title = f"{observation_name} ({phase})"
    ax.set_title(title)

    # Remove axes
    ax.axis('off')


# this function is used to get the optimal rotation angle for the images using simple projected sums
def image_rotation_analysis(image, rotations=[-1, 1], rotation_step=0.1):

    # Begin by detection edges in the image using the Beucher transform
    edges = ndimage.morphological_gradient(image, size=(3,3))
    edges = edges > edges.std()

    # Now loop over rotations in the rotation variable and calculate the sum of the pixels along the rows
    sum_of_rows_max_list = []
    for r in np.arange(rotations[0], rotations[1], rotation_step):
        rotated_edges = ndimage.rotate(edges, r, reshape=True, mode="nearest", cval=1.0)
        sum_of_rows = np.sum(rotated_edges, axis=0)
        sum_of_rows_max_list.append(np.max(sum_of_rows))

    # Then find the rotation with the maximum value in the sum of the rows
    max_sum_of_rows_rotation = np.arange(rotations[0], rotations[1], rotation_step)[np.argmax(sum_of_rows_max_list)]

    return max_sum_of_rows_rotation

# Prepare a list of phases
phases = [
    'greenup',
    'greenup_timespan',
    'flowering',
    'start_ripening',
    'flowering_timespan',
    'start_senescence',
    'start_leaffall',
    'end_leaffall'
]

# Define the list of different species and their phases

species_list = [
    {
        'norwegian_name': 'Nummer', # Number coordinates
        'english_name': 'Number',
        'latin_name': '',
        'row_start_idx': 0,
        'row_end_idx': 1,
        'col_start_idx': 0,
        'col_end_idx': 2,
        'phases': None
    }, 
    {
        'norwegian_name': 'Lokasjon', # Location coordinates
        'english_name': 'Location',
        'latin_name': '',
        'row_start_idx': 0,
        'row_end_idx': 1,
        'col_start_idx': 2,
        'col_end_idx': 15,
        'phases': None
    },
    {
        'norwegian_name': 'Fylke', # County coordinates
        'english_name': 'County',
        'latin_name': '',
        'row_start_idx': 0,
        'row_end_idx': 1,
        'col_start_idx': 15,
        'col_end_idx': 20,
        'phases': None
    },
    {
        'norwegian_name': 'Posisjon', # Position coordinates
        'english_name': 'Position',
        'latin_name': '',
        'row_start_idx': 5,
        'row_end_idx': 19,
        'col_start_idx': 0,
        'col_end_idx': 1,
        'phases': None
    },
    {
        'norwegian_name': 'HOH', # HASL coordinates
        'english_name': 'HASL',
        'latin_name': '',
        'row_start_idx': 5,
        'row_end_idx': 19,
        'col_start_idx': 0,
        'col_end_idx': 1,
        'phases': None
    },
    {
        'norwegian_name': 'DH', # Distance to sea in kilometers
        'english_name': 'DS',
        'latin_name': '',
        'row_start_idx': 5,
        'row_end_idx': 19,
        'col_start_idx': 0,
        'col_end_idx': 1,
        'phases': None
    },
    {
        'norwegian_name': 'Hestehov',
        'english_name': 'Coltsfoot',
        'latin_name': 'Tussilago farfara',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 2,
        'col_end_idx': 3,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Blåveis',
        'english_name': 'Liverleaf',
        'latin_name': 'Hepatica nobilis',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 3,
        'col_end_idx': 4,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Hvitveis',
        'english_name': 'Wood anemone',
        'latin_name': 'Anemone nemorosa',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 4,
        'col_end_idx': 5,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Rødsildre',
        'english_name': 'Purple saxifrage',
        'latin_name': 'Saxifraga oppositifolia',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 5,
        'col_end_idx': 6,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Nyresildre',
        'english_name': 'Meadow saxifrage',
        'latin_name': 'Saxifraga nemorosa',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 6,
        'col_end_idx': 7,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Maria nøklebånd',
        'english_name': 'Cowslip',
        'latin_name': 'Primula veris',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 7,
        'col_end_idx': 8,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Soleihov',
        'english_name': 'Marsh marigold',
        'latin_name': 'Caltha palustris',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 8,
        'col_end_idx': 9,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Ballblom',
        'english_name': 'Globeflower',
        'latin_name': 'Trollius europaeus',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 9,
        'col_end_idx': 10,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Liljekonvall',
        'english_name': 'Lily of the valley',
        'latin_name': 'Convallaria majalis',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 10,
        'col_end_idx': 11,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Markjordbær',
        'english_name': 'Wild strawberry',
        'latin_name': 'Fragaria vesca',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 11,
        'col_end_idx': 12,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Gjøksyre',
        'english_name': 'Wood sorrel',
        'latin_name': 'Oxalis acetosella',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 12,
        'col_end_idx': 13,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Skogstjerne',
        'english_name': 'Arctic starflower',
        'latin_name': 'Trientalis europaea',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 13,
        'col_end_idx': 14,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Linnea',
        'english_name': 'Linnaea',
        'latin_name': 'Linnaea borealis',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 14,
        'col_end_idx': 15,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Blåbær',
        'english_name': 'Blueberry',
        'latin_name': 'Vaccinium myrtillus',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 15,
        'col_end_idx': 16,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Multer',
        'english_name': 'Cloudberry',
        'latin_name': 'Rubus chamaemorus',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 16,
        'col_end_idx': 17,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Geitrams',
        'english_name': 'Fireweed',
        'latin_name': 'Epilobium angustifolium',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 17,
        'col_end_idx': 18,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Mjødurt',
        'english_name': 'Meadowsweet',
        'latin_name': 'Spirea ulmaria',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 18,
        'col_end_idx': 19,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Røsslyng',
        'english_name': 'Heather',
        'latin_name': 'Calluna vulgaris',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 19,
        'col_end_idx': 20,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Hassel',
        'english_name': 'Hazel',
        'latin_name': 'Corylus avellana',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 3,
        'col_end_idx': 4,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Gråor',  # Grey Alder coordinates, species 19
        'english_name': 'Grey Alder',
        'latin_name': 'Alnus incana',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 4,
        'col_end_idx': 5,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Selje',  # Goat Willow coordinates, species 20
        'english_name': 'Goat Willow',
        'latin_name': 'Salix caprea',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 5,
        'col_end_idx': 6,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Osp',  # Aspen coordinates, species 21
        'english_name': 'Aspen',
        'latin_name': 'Populus tremula',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 6,
        'col_end_idx': 7,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Lavlandsbjerk',  # Silver Birch coordinates, species 22
        'english_name': 'Silver Birch',
        'latin_name': 'Betula verrucosa',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 7,
        'col_end_idx': 8,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Fjellbjerk',  # Downy Birch coordinates, species 23
        'english_name': 'Downy Birch',
        'latin_name': 'Betula odorata',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 8,
        'col_end_idx': 9,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Alm',  # Wych Elm coordinates, species 24
        'english_name': 'Wych Elm',
        'latin_name': 'Ulmus montana',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 9,
        'col_end_idx': 10,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Sommerek',  # Pedunculate Oak coordinates, species 25
        'english_name': 'Pedunculate Oak',
        'latin_name': 'Quercus pedunculata',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 10,
        'col_end_idx': 11,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Bøk',  # European Beech coordinates, species 26
        'english_name': 'European Beech',
        'latin_name': 'Fagus silvatica',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 11,
        'col_end_idx': 12,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Hegg',  # Bird Cherry coordinates, species 27
        'english_name': 'Bird Cherry',
        'latin_name': 'Prunus padus',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 12,
        'col_end_idx': 13,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Slåpetorn',  # Blackthorn coordinates, species 28
        'english_name': 'Blackthorn',
        'latin_name': 'Prunus spinosa',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 13,
        'col_end_idx': 14,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Kirsebær',  # Cherry coordinates, species 29
        'english_name': 'Cherry',
        'latin_name': 'Pyrus malus',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 14,
        'col_end_idx': 15,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Eple',  # Apple coordinates, species 30
        'english_name': 'Apple',
        'latin_name': 'Pyrus malus',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 15,
        'col_end_idx': 16,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Rips',  # Redcurrant coordinates, species 31
        'english_name': 'Redcurrant',
        'latin_name': 'Ribes rubrum',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 16,
        'col_end_idx': 17,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Stikkelsbær',  # Gooseberry coordinates, species 32
        'english_name': 'Gooseberry',
        'latin_name': 'Ribes grossularia',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 17,
        'col_end_idx': 18,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Bringebær',  # Raspberry coordinates, species 33
        'english_name': 'Raspberry',
        'latin_name': 'Rubus idaeus',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 18,
        'col_end_idx': 19,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Rogn',  # Rowan coordinates, species 34
        'english_name': 'Rowan',
        'latin_name': 'Sorbus aucuparia',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 19,
        'col_end_idx': 20,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Lønn',  # Norway Maple coordinates, species 35
        'english_name': 'Norway Maple',
        'latin_name': 'Acer platanoides',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 2,
        'col_end_idx': 3,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening']
    },
    {
        'norwegian_name': 'Lind',  # Small-leaved Lime coordinates, species 36
        'english_name': 'Small leaved Lime',
        'latin_name': 'Tilia cordata',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 3,
        'col_end_idx': 4,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening']
    },
    {
        'norwegian_name': 'Syren',  # Common Lilac coordinates, species 37
        'english_name': 'Common Lilac',
        'latin_name': 'Syringa vulgaris',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 4,
        'col_end_idx': 5,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening']
    },
    {
        'norwegian_name': 'Ask',  # European Ash coordinates, species 38
        'english_name': 'European Ash',
        'latin_name': 'Fraxinus excelsior',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 5,
        'col_end_idx': 6,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening']
    },
    {
        'norwegian_name': 'Nyperose',  # Dog Rose coordinates, species 39
        'english_name': 'Dog Rose',
        'latin_name': 'Rosa sp.',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 6,
        'col_end_idx': 7,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening']
    },
    {
        'norwegian_name': 'Jasmin',  # Mock Orange coordinates, species 40
        'english_name': 'Mock Orange',
        'latin_name': 'Philadelphus coronarius',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 7,
        'col_end_idx': 8,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening']
    },
    {
        'norwegian_name': 'Gran',  # Norway Spruce coordinates, species 41
        'english_name': 'Norway Spruce',
        'latin_name': 'Picea excelsa',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 8,
        'col_end_idx': 9,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening']
    },
    {
        'norwegian_name': 'Furu',
        'english_name': 'Pine',
        'latin_name': 'Pinus sylvestris',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 9,
        'col_end_idx': 10,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening']
    },
    {
        'norwegian_name': 'Lønn',  # Norway Maple coordinates, species 35
        'english_name': 'Norway Maple',
        'latin_name': 'Acer platanoides',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 12,
        'col_end_idx': 13,
        'phases': ['flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Lind',  # Small-leaved Lime coordinates, species 36
        'english_name': 'Small leaved Lime',
        'latin_name': 'Tilia cordata',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 13,
        'col_end_idx': 14,
        'phases': ['flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Syren',  # Common Lilac coordinates, species 37
        'english_name': 'Common Lilac',
        'latin_name': 'Syringa vulgaris',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 14,
        'col_end_idx': 15,
        'phases': ['flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Ask',  # European Ash coordinates, species 38
        'english_name': 'European Ash',
        'latin_name': 'Fraxinus excelsior',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 15,
        'col_end_idx': 16,
        'phases': ['flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Nyperose',  # Dog Rose coordinates, species 39
        'english_name': 'Dog Rose',
        'latin_name': 'Rosa sp.',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 16,
        'col_end_idx': 17,
        'phases': ['flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Jasmin',  # Mock Orange coordinates, species 40
        'english_name': 'Mock Orange',
        'latin_name': 'Philadelphus coronarius',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 17,
        'col_end_idx': 18,
        'phases': ['flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Gran',  # Norway Spruce coordinates, species 41
        'english_name': 'Norway Spruce',
        'latin_name': 'Picea excelsa',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 18,
        'col_end_idx': 19,
        'phases': ['flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Furu',
        'english_name': 'Pine',
        'latin_name': 'Pinus sylvestris',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 19,
        'col_end_idx': 20,
        'phases': ['flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Antall observasjonsår',
        'english_name': 'Number of observation years',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 1,
        'col_end_idx': 2,
        'phases': None
    },
    {
        'norwegian_name': 'Løvsprett ved tregrensen',
        'english_name': 'Leafout at the treeline',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 2,
        'col_end_idx': 3,
        'phases': None
    },
    {
        'norwegian_name': 'Gjennomsnittelig høyde hvor løvsprett ved tregrensen måles',
        'english_name': 'Average height where leafout at the treeline is measured',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 3,
        'col_end_idx': 4,
        'phases': None
    },
    {
        'norwegian_name': 'Type tre som definerer tregrensen',
        'english_name': 'Type of tree that defines the treeline',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 4,
        'col_end_idx': 5,
        'phases': None
    },
    {
        'norwegian_name': 'Isløsning',
        'english_name': 'Ice break',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 5,
        'col_end_idx': 6,
        'phases': None
    },
    {
        'norwegian_name': 'Elver eller innsjøer definerer isløsning', # e -> river, s -> lake
        'english_name': 'Rivers or lakes define the ice break',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 6,
        'col_end_idx': 7,
        'phases': None
    },
    {
        'norwegian_name': 'Tid mellom isløsning elver og vann',
        'english_name': 'Time between ice break rivers and lakes',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 7,
        'col_end_idx': 8,
        'phases': None
    },
    {
        'norwegian_name': 'Ingen is prosent åpent vann hele året',
        'english_name': 'No ice percentage open water all year',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 8,
        'col_end_idx': 9,
        'phases': None
    },
    {
        'norwegian_name': 'Teleløsning',
        'english_name': 'No permafrost',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 9,
        'col_end_idx': 10,
        'phases': None
    },
    {
        'norwegian_name': 'Prosent telefritt hele året',
        'english_name': 'Percentage without permafrost all year',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 10,
        'col_end_idx': 11,
        'phases': None
    },
    {
        'norwegian_name': 'Første pløyedag',
        'english_name': 'First ploughing day',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 11,
        'col_end_idx': 12,
        'phases': None
    },
    {
        'norwegian_name': 'Første spiring åker',
        'english_name': 'First greenup fields',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 12,
        'col_end_idx': 13,
        'phases': None
    },
    {
        'norwegian_name': 'Feslepp',
        'english_name': 'Release of cattle',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 13,
        'col_end_idx': 14,
        'phases': None
    },
    {
        'norwegian_name': 'Sau eller ku definerer feslepp',
        'english_name': 'Sheep or cattle define release of cattle',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 14,
        'col_end_idx': 15,
        'phases': None
    },
    {
        'norwegian_name': 'Tid mellom feslepp sau og ku',
        'english_name': 'Time between sheep and cattle release',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 15,
        'col_end_idx': 16,
        'phases': None
    },
    {
        'norwegian_name': 'Såtid bygg',
        'english_name': 'Sowtime barley',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 16,
        'col_end_idx': 17,
        'phases': None
    },
    {
        'norwegian_name': 'Såtid havre',
        'english_name': 'Sowtime oats',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 17,
        'col_end_idx': 18,
        'phases': None
    },
    {
        'norwegian_name': 'Såtid hvete',
        'english_name': 'Sowtime wheat',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 18,
        'col_end_idx': 19,
        'phases': None
    },
    {
        'norwegian_name': 'Settetid poteter',
        'english_name': 'Potato planting',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 18,
        'col_end_idx': 19,
        'phases': None
    },
    {
        'norwegian_name': 'Første observasjon stær',
        'english_name': 'First observation of starling',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 1,
        'col_end_idx': 2,
        'phases': None
    },
    {
        'norwegian_name': 'Prosent stær overvintret',
        'english_name': 'Percentage of starling overwintering',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 2,
        'col_end_idx': 3,
        'phases': None
    },
    {
        'norwegian_name': 'Første observasjon lerke',
        'english_name': 'First observation of lark',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 3,
        'col_end_idx': 4,
        'phases': None
    },
    {
        'norwegian_name': 'Første observasjon måltrost',
        'english_name': 'First observation of song thrush',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 4,
        'col_end_idx': 5,
        'phases': None
    },
    {
        'norwegian_name': 'Første observasjon linerle',
        'english_name': 'First observation of wagtail',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 5,
        'col_end_idx': 6,
        'phases': None
    },
    {
        'norwegian_name': 'Første observasjon svale',
        'english_name': 'First observation of swallow',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 6,
        'col_end_idx': 7,
        'phases': None
    },
    {
        'norwegian_name': 'Første observasjon gjøk',
        'english_name': 'First observation of cuckoo',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 7,
        'col_end_idx': 8,
        'phases': None
    },
    {
        'norwegian_name': 'Åker moden for slått',
        'english_name': 'Field ripe for harvesting',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 8,
        'col_end_idx': 9,
        'phases': None
    },
    {
        'norwegian_name': 'Vinterrug moden for slått',
        'english_name': 'Winter rye ripe for harvesting',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 9,
        'col_end_idx': 10,
        'phases': None
    },
    {
        'norwegian_name': 'Prosent umodnet vinterrug',
        'english_name': 'Percentage of unripe winter rye',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 10,
        'col_end_idx': 11,
        'phases': None
    },
    {
        'norwegian_name': 'Havre moden for slått',
        'english_name': 'Oats ripe for harvesting',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 11,
        'col_end_idx': 12,
        'phases': None
    },
    {
        'norwegian_name': 'Havre modningstid',
        'english_name': 'Oats maturing time',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 12,
        'col_end_idx': 13,
        'phases': None
    },
    {
        'norwegian_name': 'Prosent umodnet havre',
        'english_name': 'Percentage of unripe barley',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 13,
        'col_end_idx': 14,
        'phases': None
    },
    {
        'norwegian_name': 'Bygg moden for slått',
        'english_name': 'Barley ripe for harvesting',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 14,
        'col_end_idx': 15,
        'phases': None
    },
    {
        'norwegian_name': 'Bygg modningstid',
        'english_name': 'Barley maturing time',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 15,
        'col_end_idx': 16,
        'phases': None
    },
    {
        'norwegian_name': 'Prosent umodnet bygg',
        'english_name': 'Percentage of unripe barley',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 16,
        'col_end_idx': 17,
        'phases': None
    },
    {
        'norwegian_name': 'Hvete moden for slått',
        'english_name': 'Wheat ripe for harvesting',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 17,
        'col_end_idx': 18,
        'phases': None
    },
    {
        'norwegian_name': 'Hvete modningstid',
        'english_name': 'Wheat maturing time',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 18,
        'col_end_idx': 19,
        'phases': None
    },
    {
        'norwegian_name': 'Prosent umodnet hvete',
        'english_name': 'Percentage of unripe wheat',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 19,
        'col_end_idx': 20,
        'phases': None
    },
]