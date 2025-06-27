import cv2
import numpy as np
from typing import Dict
from sklearn.cluster import KMeans
from utils.config import RANDOM_SEED, KMEANS_N_CLUSTERS, KMEANS_MAX_ITER
from utils.color_utils import color_map_ebay, color_map_vinted, find_closest_color

def process_image(image_path: str, model) -> Dict[str, str]:
    image_bgr = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    pixels = None
    h, w = image_rgb.shape[:2]
    side = min(w, h) * 0.1  # Side length is 10% of image dimension
    center_x, center_y = w / 2, h / 2
    point_coords = [
        [center_x - side / 2, center_y - side / 2],  # Top-left point
        [center_x + side / 2, center_y - side / 2],  # Top-right
        [center_x - side / 2, center_y + side / 2],  # Bottom-left
        [center_x + side / 2, center_y + side / 2]   # Bottom-right
    ]
    point_labels = [1, 1, 1, 1] # Means that the above are'Focus points' (as oppposed to 'ignore' points; less attention)
    results = model(image_rgb, points=point_coords, labels=point_labels, imgsz=640, verbose=False)
    if results and results[0].masks is not None:
        mask = results[0].masks.data[0].cpu().numpy()
        binary_mask = (mask > 0.5).astype(np.uint8)
        pixels = image_rgb[binary_mask == 1]

        if len(pixels) <= KMEANS_N_CLUSTERS:
            pixels = image_rgb.reshape(-1, 3) # Use whole image, as KMeans needs that minimum amount of pixels
    else:
        pixels = image_rgb.reshape(-1, 3)

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=KMEANS_N_CLUSTERS, n_init='auto', max_iter=KMEANS_MAX_ITER)
    kmeans.fit(pixels)
    labels = kmeans.labels_
    cluster_sizes = np.bincount(labels)
    dominant_cluster_idx = np.argmax(cluster_sizes)
    pred_rgb = kmeans.cluster_centers_[dominant_cluster_idx].astype(int)

    # Map predicted RGB to color names
    ebay_color = find_closest_color(pred_rgb, color_map_ebay)
    vinted_color = find_closest_color(pred_rgb, color_map_vinted)

    return {
        'ebay_color': ebay_color,
        'vinted_color': vinted_color,
    }