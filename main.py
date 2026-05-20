import argparse
import cv2
import numpy as np
from mejora_contraste import ajustar_brillo_contraste
from analisis_segmentacion import segmentar_por_color
from transformacion_rotacion import rotar_imagen

def main():
    """Punto de entrada del script. Parsea argumentos y orquesta el procesamiento."""
    parser = argparse.ArgumentParser(description="Procesador de imágenes de perros")
    
    # Obligatorio
    parser.add_argument("imagen", help="perro_coker.jpg")
    
    # Mejora
    parser.add_argument("--alpha", type=float, default=1.4,
                        help="Ganancia de contraste (default: 1.4)")
    parser.add_argument("--beta", type=int, default=20,
                        help="Sesgo de brillo (default: 20)")
    
    # Transformación
    parser.add_argument("--angulo", type=float, default=30.0,
                        help="Ángulo de rotación en grados (default: 30)")
    
    # Segmentación HSV
    parser.add_argument("--hsv-bajo", type=int, nargs=3, default=[5, 120, 120],
                        metavar=("H", "S", "V"),
                        help="Rango HSV mínimo para segmentación (default: 5 120 120)")
    parser.add_argument("--hsv-alto", type=int, nargs=3, default=[20, 255, 255],
                        metavar=("H", "S", "V"),
                        help="Rango HSV máximo para segmentación (default: 20 255 255)")

    args = parser.parse_args()

    img = cv2.imread(args.imagen)

    # Técnica 1: mejora
    ajustada = ajustar_brillo_contraste(img, alpha=args.alpha, beta=args.beta)
    cv2.imwrite("resultado_brillo_contraste.png", ajustada)

    # Técnica 2: transformación
    rotada = rotar_imagen(img, args.angulo)
    cv2.imwrite("resultado_rotacion.png", rotada)

    # Técnica 3: segmentación
    bajo = np.array(args.hsv_bajo)
    alto = np.array(args.hsv_alto)
    mascara, solo_obj = segmentar_por_color(img, bajo, alto)
    cv2.imwrite("resultado_mascara_color.png", mascara)
    cv2.imwrite("resultado_segmentacion.png", solo_obj)

if __name__ == "__main__":
    main()