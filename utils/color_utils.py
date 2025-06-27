import numpy as np
from typing import Dict, Tuple

color_map_ebay = {
    (245, 245, 220): "Beige",
    (0, 0, 0): "Black",
    (0, 0, 255): "Blue",
    (150, 75, 0): "Brown",
    (255, 215, 0): "Gold",
    (128, 128, 128): "Gray",
    (0, 128, 0): "Green",
    (255, 255, 240): "Ivory",
    (255, 165, 0): "Orange",
    (255, 192, 203): "Pink",
    (128, 0, 128): "Purple",
    (255, 0, 0): "Red",
    (192, 192, 192): "Silver",
    (255, 255, 255): "White",
    (255, 255, 0): "Yellow"
}

color_map_vinted = {
    (0, 0, 0): "Zwart",
    (150, 75, 0): "Bruin",
    (128, 128, 128): "Grijs",
    (245, 245, 220): "Beige",
    (255, 192, 203): "Roze",
    (128, 0, 128): "Paars",
    (255, 0, 0): "Rood",
    (255, 255, 0): "Geel",
    (0, 0, 255): "Blauw",
    (0, 128, 0): "Groen",
    (255, 165, 0): "Oranje",
    (255, 255, 255): "Wit",
    (192, 192, 192): "Zilver",
    (255, 215, 0): "Goud",
    (107, 142, 35): "Khaki",
    (64, 224, 208): "Turqoise",
    (255, 245, 235): "Creme",
    (255, 204, 153): "Pasteloranje",
    (102, 0, 0): "Wijnrood",
    (255, 127, 127): "Koraal",
    (255, 182, 193): "Lichtroze",
    (200, 162, 200): "Lila",
    (173, 216, 230): "Lichtblauw",
    (0, 0, 128): "Marineblauw",
    (0, 100, 0): "Donkergroen",
    (255, 219, 88): "Mosterdgeel",
    (152, 255, 152): "Mintgroen"
}

def find_closest_color(rgb: np.ndarray, color_map: Dict[Tuple[int, int, int], str]) -> str:
    rgb = np.array(rgb)
    min_distance = float('inf')
    closest_color = "Unknown"
    for color_rgb, color_name in color_map.items():
        distance = np.sqrt(np.sum((rgb - np.array(color_rgb)) ** 2))
        if distance < min_distance:
            min_distance = distance
            closest_color = color_name
    return closest_color