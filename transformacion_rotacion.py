
# Técnica 2: Transformación de imagen - Rotación



import cv2
import numpy as np

def rotar_imagen(img, angulo):
    """Rota una imagen preservando el contenido completo.

    Args:
        img: array NumPy BGR (uint8).
        angulo: ángulo de rotación en grados (sentido antihorario).

    Returns:
        Array NumPy con la imagen rotada, sin recortar esquinas.
    """
    h, w = img.shape[:2]
    cx, cy = w / 2, h / 2

    M = cv2.getRotationMatrix2D((cx, cy), angulo, scale=1.0)
    
    # Calcula el bounding box rotado para no perder esquinas
    cos = abs(M[0, 0])
    sin = abs(M[0, 1])
    nuevo_w = int(h * sin + w * cos)
    nuevo_h = int(h * cos + w * sin)
    
    # Ajusta la traslación de la matriz para centrar el resultado
    M[0, 2] += (nuevo_w / 2) - cx
    M[1, 2] += (nuevo_h / 2) - cy

    return cv2.warpAffine(img, M, (nuevo_w, nuevo_h))