"""
Plot geospatial predictions on an interactive map using H3 hexagons.
"""

import pandas as pd
from ast import literal_eval
import h3
import folium
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from branca.colormap import LinearColormap
from typing import List, Dict, Tuple, Optional, Any, Union


class Config:
    """Configuration parameters for the geo plotting application."""

    H3_RESOLUTION = 5  # Resolution for H3 hexagons (0-15)


class DataLoader:
    """Handles loading and basic preprocessing of geographical data."""

    @staticmethod
    def load_data(
        original_data_path: str,
        ground_truth_path: str,
        predictions_path: str,
        pred_column: str,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, List[str], List[Dict], List]:
        """
        Load all required datasets.

        Returns:
            Tuple containing:
            - Original dataframe
            - Ground truth dataframe
            - Predictions dataframe
            - Location names
            - Positions
            - Predictions
        """
        df_orig = pd.read_pickle(original_data_path)
        df = pd.read_parquet(ground_truth_path)
        df_preds = pd.read_parquet(predictions_path)

        place_names = df_orig["location"].values
        positions = df["position_ground_truth"].values
        predictions = df_preds[pred_column].values

        return df_orig, df, df_preds, place_names, positions, predictions


class DataProcessor:
    """Processes geographical data for visualization."""

    @staticmethod
    def parse_coordinates(item: str) -> Tuple[float, float]:
        """Convert dictionary coordinates to lat/lng pairs."""
        parsed_item = literal_eval(item)
        return parsed_item

    @staticmethod
    def get_coordinates(positions: List[str]) -> List[Dict]:
        """Extract coordinates from position dictionaries."""
        coordinates = []
        for idx, pos in enumerate(positions):
            try:
                coordinates.append(DataProcessor.parse_coordinates(pos))
            except Exception as e:
                print(f"Error parsing position {idx}: {pos}")
                print(f"Error: {e}")
                coordinates.append(None)
        return coordinates

    @staticmethod
    def parse_predictions(preds: List[str], column_name: str) -> List[Optional[int]]:
        """Parse prediction strings into numeric values."""
        parsed_preds = []
        for pred in preds:
            try:
                if pred == "" or pred == "?":
                    parsed_pred = None
                else:
                    parsed_pred = int(pred.strip("()[]"))
                    is_height_column = (
                        column_name
                        == "average_height_where_leafout_at_the_treeline_is_measured"
                    )
                    if not is_height_column and (parsed_pred < 0 or parsed_pred > 365):
                        print(f"Prediction {pred} is out of range")
                        parsed_pred = None
                parsed_preds.append(parsed_pred)
            except Exception as e:
                print(f"Error parsing prediction {pred}: {e}")
                parsed_preds.append(None)
        return parsed_preds

    @staticmethod
    def create_hexagon_data(
        coordinates: List[Dict],
        locations: List[str],
        predictions: List[Optional[int]],
        pred_column: str,
        h3_resolution: int,
    ) -> Tuple[List[str], Dict[str, Dict]]:
        """
        Group data points into H3 hexagons.

        Returns:
            h3_hexagons: List of H3 cell IDs
            hex_data: Dictionary mapping H3 IDs to aggregated data
        """
        h3_hexagons = []
        hex_data = {}

        for idx, (coord, location) in enumerate(zip(coordinates, locations)):
            if coord is None or predictions[idx] is None:
                continue

            lat, lng = coord["E"], coord["N"]
            hex_id = h3.latlng_to_cell(lat, lng, h3_resolution)
            h3_hexagons.append(hex_id)

            # Initialize or update hexagon data
            if hex_id not in hex_data:
                hex_data[hex_id] = {
                    "coords": [(lat, lng)],
                    "H": [coord.get("H", "N/A")],
                    "K": [coord.get("K", "N/A")],
                    "location": [location],
                    pred_column: [predictions[idx]],
                }
            else:
                hex_data[hex_id]["coords"].append((lat, lng))
                hex_data[hex_id]["H"].append(coord.get("H", "N/A"))
                hex_data[hex_id]["K"].append(coord.get("K", "N/A"))
                hex_data[hex_id]["location"].append(location)
                hex_data[hex_id][pred_column].append(predictions[idx])

        return h3_hexagons, hex_data


class MapVisualizer:
    """Creates and configures interactive folium maps with H3 hexagons."""

    @staticmethod
    def create_map(
        center_coords: Tuple[float, float], zoom_level: int = 10
    ) -> folium.Map:
        """Create a new folium map centered at the specified coordinates."""
        return folium.Map(location=center_coords, zoom_start=zoom_level)

    @staticmethod
    def calculate_color_range(
        hex_data: Dict[str, Dict], pred_column: str
    ) -> Tuple[float, float]:
        """Calculate the min and max prediction values for color scaling."""
        all_preds = []
        for hex_id in hex_data:
            all_preds.extend(hex_data[hex_id][pred_column])
        return min(all_preds), max(all_preds)

    @staticmethod
    def create_popup_content(hex_data: Dict, hex_id: str, pred_column: str) -> str:
        """Create HTML content for hexagon popups."""
        center_lat, center_lng = h3.cell_to_latlng(hex_id)
        popup_content = f"<b>Center:</b> {center_lat:.6f}, {center_lng:.6f}<br>"
        popup_content += "<b>Points:</b><br>"

        for i, (point_lat, point_lng) in enumerate(hex_data[hex_id]["coords"]):
            h_val = hex_data[hex_id]["H"][i]
            k_val = hex_data[hex_id]["K"][i]
            location = hex_data[hex_id]["location"][i]
            pred_val = hex_data[hex_id][pred_column][i]

            popup_content += f"<b>Location:</b> {location}<br>"
            popup_content += f"Lat/Lng: {point_lat:.6f}, {point_lng:.6f}<br>"
            popup_content += f"H: {h_val}, K: {k_val}<br>"
            popup_content += f"<b>{pred_column}:</b> {pred_val}<br>"
            popup_content += "<hr>" if i < len(hex_data[hex_id]["coords"]) - 1 else ""

        return popup_content

    @staticmethod
    def add_hexagons_to_map(
        m: folium.Map,
        hex_data: Dict[str, Dict],
        h3_hexagons: List[str],
        pred_column: str,
        colormap: Any,
        color_norm: Any,
    ) -> None:
        """Add H3 hexagons to the map with appropriate styling and popups."""
        for hex_id in set(h3_hexagons):
            boundaries = h3.cell_to_boundary(hex_id)
            boundaries = [(lng, lat) for lat, lng in boundaries]

            # Calculate average prediction for this hexagon
            avg_pred = sum(hex_data[hex_id][pred_column]) / len(
                hex_data[hex_id][pred_column]
            )

            # Get color for this hexagon
            rgba_color = colormap(color_norm(avg_pred))
            hex_color = mcolors.rgb2hex(rgba_color)

            # Create popup content
            popup_content = MapVisualizer.create_popup_content(
                hex_data, hex_id, pred_column
            )

            # Add polygon to map
            folium.Polygon(
                locations=boundaries,
                color="black",
                fill_color=hex_color,
                fill=True,
                weight=2,
                fill_opacity=0.7,
                popup=folium.Popup(popup_content, max_width=500),
            ).add_to(m)

    @staticmethod
    def add_colorbar(
        m: folium.Map,
        min_val: float,
        max_val: float,
        colormap: Any,
        color_norm: Any,
        caption: str,
    ) -> None:
        """Add a color legend to the map."""
        linear_map = LinearColormap(
            colors=[
                mcolors.rgb2hex(colormap(color_norm(min_val))),
                mcolors.rgb2hex(
                    colormap(color_norm(min_val + (max_val - min_val) * 0.25))
                ),
                mcolors.rgb2hex(
                    colormap(color_norm(min_val + (max_val - min_val) * 0.5))
                ),
                mcolors.rgb2hex(
                    colormap(color_norm(min_val + (max_val - min_val) * 0.75))
                ),
                mcolors.rgb2hex(colormap(color_norm(max_val))),
            ],
            index=[
                min_val,
                min_val + (max_val - min_val) * 0.25,
                min_val + (max_val - min_val) * 0.5,
                min_val + (max_val - min_val) * 0.75,
                max_val,
            ],
            vmin=min_val,
            vmax=max_val,
            caption=caption,
        )
        linear_map.add_to(m)


def create_geo_visualization(
    data_path: str, pred_column: str, output_path: str
) -> None:
    """
    Main function to create a hexagon-based geographic visualization.

    Args:
        original_data_path: Path to the pickle file with original data
        ground_truth_path: Path to the parquet file with ground truth data
        predictions_path: Path to the parquet file with prediction data
        pred_column: Column name in predictions dataframe to visualize
        output_path: Path to save the output HTML map
    """

    # Load data
    df = pd.read_parquet(data_path)
    place_names = df["location"].values
    positions = df["position_ground_truth"].values
    predictions = df[pred_column].values

    # Process data
    coordinates = DataProcessor.get_coordinates(positions)
    parsed_predictions = DataProcessor.parse_predictions(predictions, pred_column)
    h3_hexagons, hex_data = DataProcessor.create_hexagon_data(
        coordinates, place_names, parsed_predictions, pred_column, Config.H3_RESOLUTION
    )

    if not h3_hexagons:
        print("No valid hexagons to display. Check your data.")
        return

    # Create map
    center_coords = coordinates[0]["N"], coordinates[0]["E"]
    m = MapVisualizer.create_map(center_coords)

    # Create color mapping
    min_pred, max_pred = MapVisualizer.calculate_color_range(hex_data, pred_column)
    norm = mcolors.Normalize(vmin=min_pred, vmax=max_pred)
    cmap = plt.get_cmap("coolwarm")

    # Add hexagons to map
    MapVisualizer.add_hexagons_to_map(m, hex_data, h3_hexagons, pred_column, cmap, norm)

    # Add color legend
    caption = (
        "Tree line"
        if pred_column == "average_height_where_leafout_at_the_treeline_is_measured"
        else f"{pred_column} Prediction Value"
    )
    MapVisualizer.add_colorbar(m, min_pred, max_pred, cmap, norm, caption)

    # Save map
    m.save(output_path)
    print(f"Map saved to {output_path}")


if __name__ == "__main__":
    # Configuration parameters

    DATA_PATH = "./data/df_complete.parquet"
    PRED_COLUMN = "average_height_where_leafout_at_the_treeline_is_measured"  # select any column with data, for example average_height_where_leafout_at_the_treeline_is_measured, norway_spruce_greenup, silver_birch_greenup, blueberry_flowering, ...
    OUTPUT_PATH = f"h3_map_with_color_by_prediction_{PRED_COLUMN}.html"

    create_geo_visualization(DATA_PATH, PRED_COLUMN, OUTPUT_PATH)
