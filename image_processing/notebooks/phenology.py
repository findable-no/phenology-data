"""
Phenology module for plant phenology analysis and visualization.

This module provides a comprehensive set of tools for analyzing and visualizing
plant phenology data, including coordinate handling, image processing, model
interaction, and species definitions.

The module is organized into several submodules:
- utils.coordinates: Coordinate-related utilities and constants
- utils.image_processing: Image processing and visualization functions
- models.model_utils: Model interaction and data formatting functions
- data.species_definitions: Species and phase definitions
"""

from utils.coordinates import table_rows, table_cols, dms_to_decimal, parse_coordinates
from utils.image_processing import show_selection, image_rotation_analysis, img_to_bytes, bytes_to_img, visualize_observation_phases, plot_projections, find_corner
from models.model_utils import format_data, generate_description, get_model_and_processor
from data.species_definitions import phases, species_list, generate_species_phase_dicts

# Re-export all the necessary components
__all__ = [
    'table_rows',
    'table_cols',
    'dms_to_decimal',
    'parse_coordinates',
    'show_selection',
    'image_rotation_analysis',
    'img_to_bytes',
    'bytes_to_img',
    'visualize_observation_phases',
    'plot_projections',
    'find_corner',
    'format_data',
    'generate_description',
    'get_model_and_processor',
    'phases',
    'species_list',
    'generate_species_phase_dicts'
]