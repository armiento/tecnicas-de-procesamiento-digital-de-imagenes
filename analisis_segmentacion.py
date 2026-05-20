# Técnica 3: Análisis de segmentación - Segmentación por color

import cv2
import numpy as np

def segmentar_por_color(img, bajo, alto):
    """Segmenta una imagen extrayendo píxeles dentro de un rango de color HSV.

    Args:
        img: array NumPy BGR (uint8).
        bajo: array NumPy con los valores mínimos HSV (ej. [5, 120, 120]).
        alto: array NumPy con los valores máximos HSV (ej. [20, 255, 255]).

    Returns:
        Tupla (mascara, solo_objeto):
            mascara: imagen binaria donde blanco indica píxeles en el rango.
            solo_objeto: imagen original con solo los píxeles segmentados visibles.
    """
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mascara = cv2.inRange(hsv, bajo, alto)
    solo_objeto = cv2.bitwise_and(img, img, mask=mascara)
    return mascara, solo_objeto