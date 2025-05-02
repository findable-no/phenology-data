import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from skimage.morphology import dilation, disk
from skimage.transform import resize
from PIL import Image as PILImage
import io


# Display selected regions from tables with optional rotation and dilation.
def show_selection(tables,
                   info_dict,
                   offset=5,
                   figsize=(25, 25),
                   rotate=False,
                   selem_size=1.5,
                   selection_size=50,
                   subplot_size=(5, 10),
                   show_images=True,
                   table_rows=None,
                   table_cols=None,
                   use_dilation=False):
    """Display selected regions from tables with optional rotation and dilation."""
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
        else:
            tmp_img = table[start_r:(stop_r + offset), start_c:(stop_c + offset)]
            tmp_img = np.rot90(tmp_img, k=3)

        # Normalize the image
        tmp_img = tmp_img - tmp_img.min()
        tmp_img = tmp_img / tmp_img.max()

        # Apply morphological grayscale dilation to increase contrast
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

    return images

# Analyze optimal rotation angle for images using projected sums.
def image_rotation_analysis(image, rotations=[-1, 1], rotation_step=0.1):
    """Analyze optimal rotation angle for images using projected sums."""
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

# Convert numpy image array to bytes.
def img_to_bytes(image):
    """Convert numpy image array to bytes."""
    image = 255 * image
    image = image.astype(np.uint8)
    image = PILImage.fromarray(image)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='TIFF')
    img_byte_str = img_byte_arr.getvalue()
    return img_byte_str

# Convert bytes to PIL Image.
def bytes_to_img(img_byte_str):
    """Convert bytes to PIL Image."""
    img_byte_arr = io.BytesIO(img_byte_str)
    image = PILImage.open(img_byte_arr)
    return image.convert("RGB") 

# Plot vertical and horizontal projections of an image.
def plot_projections(image, figsize_v=(12, 15), figsize_h=(15, 10)):
    h_proj = np.sum(np.max(image) - image, axis=1)
    v_proj = np.sum(np.max(image) - image, axis=0)
    height, width = image.shape
    
    #-----------------------------------
    # 1. VERTICAL PROJECTION
    #-----------------------------------
    fig1, (ax_vproj, ax_img) = plt.subplots(
        2, 1, figsize=figsize_v, gridspec_kw={'height_ratios': [1, 5]}, sharex=True
    )
    
    ax_vproj.plot(np.arange(width), v_proj, 'b-')
    ax_vproj.set_xlim(0, width)
    ax_vproj.set_ylabel('Sum')
    ax_vproj.set_title('Vertical Pixel Sums')
    ax_vproj.grid(True)
    
    ax_img.imshow(np.max(image) - image, cmap='gray', aspect='auto', extent=[0, width, height, 0])
    ax_img.set_title('Document')

    #-----------------------------------
    # 2. HORIZONTAL PROJECTION
    #-----------------------------------
    fig2, (ax_img2, ax_hproj) = plt.subplots(
        1, 2, figsize=figsize_h, gridspec_kw={'width_ratios': [5, 1]}, sharey=True
    )
    
    ax_img2.imshow(np.max(image) - image, cmap='gray', aspect='auto', extent=[0, width, height, 0])
    ax_img2.set_title('Document')

    ax_hproj.plot(h_proj, np.arange(height), 'r-')
    ax_hproj.set_ylim(height, 0)  # flip the y-axis here, instead of the image
    ax_hproj.set_xlabel('Sum')
    ax_hproj.set_title('Horizontal Pixel Sums')
    ax_hproj.grid(True)

    fig1.tight_layout()
    fig2.tight_layout()

    return fig1, fig2, h_proj, v_proj

# Find the corner of a table in an image.
def find_corner(corner_candidate, corner_name):
    nonzero_y, nonzero_x = np.nonzero(corner_candidate)
    if corner_name == 'upper_left':
        distances = np.sqrt(nonzero_y**2 + nonzero_x**2)  # Calculate distances to (0,0)
        closest_idx = np.argmin(distances)  # Find index of minimum distance
        closest_row = nonzero_y[closest_idx]
        closest_col = nonzero_x[closest_idx]
    elif corner_name == 'lower_right':
        distances = np.sqrt((nonzero_y - corner_candidate.shape[0])**2 + (nonzero_x - corner_candidate.shape[1])**2)  # Calculate distances to (corner_candidate.shape[0], corner_candidate.shape[1])
        closest_idx = np.argmin(distances)  # Find index of minimum distance
        closest_row = nonzero_y[closest_idx]
        closest_col = nonzero_x[closest_idx]
    return closest_row, closest_col

# This function show species and their phase information overlaid on a table
def visualize_observation_phases(image,
                                 observation_name,
                                 phase,
                                 observation_list,
                                 table_rows,
                                 table_cols,
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
    row_start = table_rows[observation_info['row_start_idx']]
    row_end = table_rows[observation_info['row_end_idx']]
    # Get column positions
    col_start = table_cols[observation_info['col_start_idx']]
    col_end = table_cols[observation_info['col_end_idx']]

    # Create and add the rectangle
    rect = Rectangle((col_start, row_start), col_end - col_start, row_end - row_start, 
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