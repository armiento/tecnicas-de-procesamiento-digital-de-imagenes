#Técnica 1: mejora de imagen - Contraste y brillo




import cv2

def ajustar_brillo_contraste(img, alpha=1.4, beta=20):
    """Ajusta el brillo y contraste de una imagen.

    Args:
        img: array NumPy BGR (uint8).
        alpha: ganancia de contraste. Valores > 1 aumentan contraste (default: 1.4).
        beta: sesgo de brillo. Valores positivos aclaran la imagen (default: 20).

    Returns:
        Array NumPy BGR (uint8) con brillo y contraste ajustados.
    """
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)