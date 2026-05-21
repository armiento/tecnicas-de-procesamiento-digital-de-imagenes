Veo que tenés el material del proyecto de procesamiento de imágenes. ¿En qué te puedo ayudar? ¿Están arrancando el parcial, tienen dudas sobre alguna técnica específica, o necesitan orientación para estructurar el código?Dijiste: cuales puedo usar: Aplicar al menos tres técnicas distintas de procesamiento (mejora, transformación, análisis o detección)?cuales puedo usar: Aplicar al menos tres técnicas distintas de procesamiento (mejora, transformación, análisis o detección)?20 mayClaude respondió: Basándome en el material de la materia, tenés un montón de opciones.Basándome en el material de la materia, tenés un montón de opciones. Te listo algunas combinaciones interesantes:
Mejora

Ecualización de histograma / CLAHE (contraste)
Corrección gamma (imágenes oscuras)
Ajuste de brillo/contraste con convertScaleAbs
Reducción de ruido (Gaussiano, mediana, bilateral)

Transformación

Rotación, traslación, escalado
Corrección de perspectiva
Conversión entre espacios de color (RGB → HSV, Lab, grises)

Análisis

Histograma de intensidades
Segmentación por color (máscara en HSV)
Segmentación por umbralización (Otsu, adaptativa)
K-means para cuantización de color

Detección

Detección de bordes (Canny, Sobel)
Detección de contornos y conteo de objetos
Detección de rostros con cascadas de Haar
Operaciones morfológicas (apertura, cierre, top-hat)


Para elegir bien, ayuda saber una cosa:Dijiste: P: ¿Qué tipo de imágenes pensás usar como entrada?P: ¿Qué tipo de imágenes pensás usar como entrada?
R: perros20 mayClaude respondió: Buena elección, es un tema concreto y divertido.Buena elección, es un tema concreto y divertido. Para imágenes de perros, estas tres técnicas tienen mucho sentido juntas:
1. Detección de bordes con Canny
Resalta el contorno del perro, el pelaje, las orejas. Es visual e interesante de mostrar.
2. Segmentación por color en HSV
Podés aislar el perro del fondo si hay contraste de color, o crear una máscara de la región del animal.
3. Mejora de contraste con CLAHE
Muy útil si las fotos tienen iluminación despareja (sombras en el pelaje, fotos de interior). Mejora el detalle sin saturar.

Como cuarta opcional que queda muy bien con perros:
Detección de contornos + conteo de formas — si tenés fotos con más de un perro, podés detectar y contar cuántos hay.

La combinación que te recomendaría para el parcial sería:

CLAHE (mejora) → Canny (detección) → Segmentación HSV (análisis)

Son tres categorías distintas (mejora, detección, análisis), cada una tiene parámetros configurables por CLI, y se puede armar un pipeline donde una prepara la imagen para la siguiente. ¿Te parece bien esa dirección o querés explorar otra combinación?import cv2
import numpy as np

img = cv2.imread("perro_coker.jpg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Rango aproximado del color naranja en HSV
bajo  = np.array([5,  120, 120])
alto  = np.array([20, 255, 255])

mascara = cv2.inRange(hsv, bajo, alto)
solo_obj = cv2.bitwise_and(img, img, mask=mascara)

cv2.imwrite("mascara_color.png", mascara)
cv2.imwrite("objetos_color.png", solo_obj)



import cv2

img = cv2.imread("perro_coker.jpg")

# alpha = ganancia (contraste); beta = sesgo (brillo)
alpha, beta = 1.4, 20
ajustada = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

cv2.imwrite("ajustada.png", ajustada)





import cv2
import numpy as np

img = cv2.imread("perro_coker.jpg")
h, w = img.shape[:2]
cx, cy = w / 2, h / 2
angulo = 30

M = cv2.getRotationMatrix2D((cx, cy), angulo, scale=1.0)

# Calcula el bounding box rotado para no perder esquinas
cos = abs(M[0, 0])
sin = abs(M[0, 1])
nuevo_w = int(h * sin + w * cos)
nuevo_h = int(h * cos + w * sin)

# Ajusta la traslación de la matriz para centrar el resultado
M[0, 2] += (nuevo_w / 2) - cx
M[1, 2] += (nuevo_h / 2) - cy

rotada = cv2.warpAffine(img, M, (nuevo_w, nuevo_h))
cv2.imwrite("rotada.png", rotada)Mostrar más20 mayClaude respondió: Buen arranque, el código funciona.Buen arranque, el código funciona. Ahora el trabajo es convertirlo en un proyecto bien estructurado según la consigna. Te marco lo que falta:
Problemas actuales

Todo está en un solo archivo, sin funciones ni clases
No hay argparse (parámetros por CLI)
No hay docstrings
No hay main.py separado de la lógica


Estructura que deberías armar:
proyecto/
├── main.py              # solo parsea args y orquesta
├── filtros.py           # ajuste de brillo/contraste
├── transformaciones.py  # rotación
├── segmentacion.py      # máscara HSV
├── README.md
├── imagenes/
│   └── perro_coker.jpg
└── resultados/

Cómo quedaría cada módulo, por ejemplo transformaciones.py:
pythonimport cv2
import numpy as np

def rotar_imagen(img, angulo):
    """Rota una imagen preservando el contenido completo.

    Args:
        img: array NumPy BGR (uint8).
        angulo: ángulo de rotación en grados (sentido antihorario).

    Returns:
        Array NumPy con la imagen rotada, sin recortar esquinas.
    """
    # tu lógica acá

Y main.py con argparse:
pythonimport argparse
from transformaciones import rotar_imagen
from segmentacion import segmentar_color
from filtros import ajustar_brillo

def main():
    parser = argparse.ArgumentParser(description="Procesador de imágenes de perros")
    parser.add_argument("imagen", help="Ruta a la imagen de entrada")
    parser.add_argument("--angulo", type=float, default=30.0,
                        help="Ángulo de rotación en grados (default: 30)")
    parser.add_argument("--alpha", type=float, default=1.4,
                        help="Ganancia de contraste (default: 1.4)")
    # etc.
    args = parser.parse_args()
    # llamar a las funciones acá

if __name__ == "__main__":
    main()

El código que tenés está bien como borrador. El siguiente paso es moverlo a funciones con docstrings y separarlo en archivos. ¿Querés que te ayude a pensar cómo dividir responsabilidades entre los módulos?Dijiste: me faltaría el de segmentacion y mejorame faltaría el de segmentacion y mejora20 mayClaude respondió: Para la consigna necesitás cubrir al menos tres categorías distintas.Para la consigna necesitás cubrir al menos tres categorías distintas. Ya tenés:

✅ Transformación — rotación
✅ Mejora — ajuste de brillo/contraste (convertScaleAbs)

Entonces lo que falta es una de análisis o detección. La segmentación HSV que tenés cuenta como análisis, así que ya cubrís las tres categorías.
Pero antes de escribir código, pensemos un poco:
Para segmentación HSV en perros, el rango [5-20] que usaste es para tonos naranjas/dorados. Eso funciona bien para un cocker spaniel dorado, pero si la foto tiene otro fondo o el perro es de otro color, la máscara va a quedar vacía o con ruido.
Algunas preguntas para que pienses antes de implementar:

¿El perro de tu foto es de color claro/dorado o de otro color?
¿El fondo contrasta bien con el perro?
¿Qué querés mostrar con la segmentación — aislar al perro, o aislar el fondo?


Para mejora, ya tenés convertScaleAbs. Si querés algo más interesante para el parcial, podrías agregar CLAHE como segunda técnica de mejora, que trabaja sobre el canal de luminancia en Lab y da mejores resultados en fotos con iluminación despareja.
¿Qué preferís — me contás sobre la foto y vemos si el rango HSV tiene sentido, o arrancamos a estructurar el módulo segmentacion.py?Dijiste: python#Técnica 1: mejora de imagen - Contraste y brillo

import cv2

img = cv2.imread("perro_coker.jpg")

# alpha = ganancia (contraste); beta = sesgo (brillo)
alpha, beta = 1.4, 20
ajustada = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

cv2.imwrite("ajustada.png", ajustada)# Técnica 3: Análisis de segmentación - Segmentación por color

import cv2
import numpy as np


img = cv2.imread("perro_coker.jpg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Rango aproximado del color naranja en HSV
bajo  = np.array([5,  120, 120])
alto  = np.array([20, 255, 255])

mascara = cv2.inRange(hsv, bajo, alto)
solo_obj = cv2.bitwise_and(img, img, mask=mascara)

cv2.imwrite("mascara_color.png", mascara)
cv2.imwrite("objetos_color.png", solo_obj)Mostrar más20 mayClaude respondió: Bien, ya tenés la lógica.Bien, ya tenés la lógica. Ahora el trabajo es convertir cada bloque en una función documentada dentro de su módulo correspondiente.
filtros.py debería quedar así:
pythonimport cv2

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
segmentacion.py debería quedar así:
pythonimport cv2
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

Dos cosas para que pienses antes de conectarlo en main.py:

Los valores bajo y alto del rango HSV, ¿los vas a hardcodear o los va a poder cambiar el usuario por CLI?
¿Dónde van a guardarse los resultados — siempre en la misma carpeta, o también eso es configurable?
Dijiste: lo completa el usuario.lo completa el usuario. En la misma carpeta guardar20 mayClaude respondió: Perfecto.Perfecto. Entonces en main.py los rangos HSV y los parámetros de brillo/contraste van como argumentos opcionales con valores por defecto.
Así quedaría el esqueleto de main.py:
pythonimport argparse
import cv2
import numpy as np
from filtros import ajustar_brillo_contraste
from segmentacion import segmentar_por_color
from transformaciones import rotar_imagen

def main():
    """Punto de entrada del script. Parsea argumentos y orquesta el procesamiento."""
    parser = argparse.ArgumentParser(description="Procesador de imágenes de perros")
    
    # Obligatorio
    parser.add_argument("imagen", help="Ruta a la imagen de entrada")
    
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

Se usaría así desde la terminal:
bash# Con valores por defecto
python main.py perro_coker.jpg

# Personalizando parámetros
python main.py perro_coker.jpg --alpha 1.8 --beta 30 --angulo 45 --hsv-bajo 10 100 100 --hsv-alto 25 255 255

Lo que falta completar es transformaciones.py con la función rotar_imagen documentada. Ya tenés la lógica escrita — solo hay que moverla adentro de la función con su docstring. ¿Lo intentás vos y me mostrás cómo te queda?Dijiste: ferar@DESKTOP-NE0FO6Q MINGW64 ~/OneDrive/Documentos/TSCD/QUINTO CUATRIMESTRE/TECNICAS DE PROCESAMIENTO DE IMAGENES/TP INTEGRADORferar@DESKTOP-NE0FO6Q MINGW64 ~/OneDrive/Documentos/TSCD/QUINTO CUATRIMESTRE/TECNICAS DE PROCESAMIENTO DE IMAGENES/TP INTEGRADOR
$ c:/python313/python.exe "c:/Users/ferar/OneDrive/Documentos/TSCD/QUINTO CUATRIMESTRE/TECNICAS DE PROCESAMIENTO DE IMAGENES/TP INTEGRADOR/main.py"
usage: main.py [-h] [--alpha ALPHA] [--beta BETA] [--angulo ANGULO] [--hsv-bajo H S V] [--hsv-alto H S V] imagen
main.py: error: the following arguments are required: imagen20 mayClaude respondió: Perfecto, eso significa que el script funciona correctamente.Perfecto, eso significa que el script funciona correctamente. Ese mensaje no es un error del código, es argparse avisando que falta el argumento obligatorio imagen.
Tenés que ejecutarlo así:
bashpython main.py perro_coker.jpg
O con la ruta completa si la imagen está en otra carpeta:
bashpython main.py "c:/Users/ferar/.../perro_coker.jpg"
Para verificar que todo funciona, fijate que después de ejecutarlo aparezcan estos archivos en la misma carpeta:

resultado_brillo_contraste.png
resultado_rotacion.png
resultado_mascara_color.png
resultado_segmentacion.png

¿Te corrió bien?Dijiste: no guarda imagen# Técnica 3: Análisis de segmentación - Segmentación por color

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
    return mascara, solo_objetono guarda imagenMostrar más20 mayClaude respondió: El problema es que segmentarporcolor solo procesa y devuelve, pero quien tiene que guardar es main.El problema es que segmentar_por_color solo procesa y devuelve, pero quien tiene que guardar es main.py. Fijate en el main.py que armamos, ya está el guardado:
pythonmascara, solo_obj = segmentar_por_color(img, bajo, alto)
cv2.imwrite("resultado_mascara_color.png", mascara)
cv2.imwrite("resultado_segmentacion.png", solo_obj)
Eso es correcto — la función no debería guardar, ese es el trabajo de main.py. La separación de responsabilidades es justamente lo que pide la consigna.
El problema probablemente es otro. Revisá estas cosas:
1. ¿La imagen se cargó bien?
pythonimg = cv2.imread(args.imagen)
if img is None:
    print(f"Error: no se pudo cargar {args.imagen}")
    return
2. ¿Desde qué carpeta estás ejecutando?
Si ejecutás desde una carpeta distinta a donde está la imagen, cv2.imread devuelve None y todo falla silenciosamente.
3. ¿Cuál es el error exacto que aparece en la terminal? ¿El script termina sin mensajes, o tira alguna excepción?
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
    return mascara, solo_objetoMostrar más20 mayClaude respondió: Ese archivo está bien.Ese archivo está bien. El problema no está en segmentacion.py.
Mostrame el main.py completo que estás usando ahora, para ver si el guardado está conectado correctamente con la función.def main():
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
    main()Mostrar más20 mayClaude respondió: El código está bien.El código está bien. El problema casi seguro es que img es None porque la imagen no se encuentra en la carpeta desde donde ejecutás.
Agregá esta validación justo después de cv2.imread:
pythonimg = cv2.imread(args.imagen)

if img is None:
    print(f"Error: no se pudo cargar la imagen '{args.imagen}'")
    print("Verificá que la ruta sea correcta y que el archivo exista.")
    return
Y ejecutalo así desde la terminal, estando en la carpeta del proyecto:
bashcd "c:/Users/ferar/OneDrive/Documentos/TSCD/QUINTO CUATRIMESTRE/TECNICAS DE PROCESAMIENTO DE IMAGENES/TP INTEGRADOR"
python main.py perro_coker.jpg
Si el error aparece, significa que perro_coker.jpg no está en esa carpeta. Verificá con:
bashls *.jpg
¿Qué te muestra?Dijiste: funciona todo, precisamos seguir con las consignas, como Documentación con docstringsfunciona todo, precisamos seguir con las consignas, como Documentación con docstrings20 mayClaude respondió: Bien.Bien. Ya tenés los docstrings en las funciones, eso es lo principal. Repasemos qué falta según la consigna:

Cada clase y cada función definidas en el código deben tener docstring con:

Qué hace
Parámetros (tipo y significado)
Qué devuelve
Qué excepciones puede lanzar (si aplica)



Mostrame los archivos que tenés hasta ahora:

main.py completo
filtros.py
transformaciones.py
segmentacion.py

Así vemos qué funciones ya tienen docstring correcto y cuáles les falta, antes de dar la consigna por cumplida.Dijiste: Archivo README.Archivo README.md con:
 Nombres de los integrantes del equipo.Cómo correr el script (ejemplos con parámetros).Descripción de cada técnica aplicada y qué efecto produce.Decisiones técnicas tomadas y por qué.20 mayClaude respondió: Mostrame los datos y te ayudo a armarlo:Mostrame los datos y te ayudo a armarlo:

¿Cuáles son los nombres de los integrantes del equipo?
¿Cómo se llama el proyecto/repositorio?

Y confirmame las tres técnicas que quedaron en el script final con sus parámetros CLI, así el README refleja exactamente lo que entregás.Dijiste: pythonimport argparse
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
    main()# Técnica 3: Análisis de segmentación - Segmentación por color

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
    return mascara, solo_objeto#Técnica 1: mejora de imagen - Contraste y brillo



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
    img = cv2.imread("perro_coker.jpg")

    # alpha = ganancia (contraste); beta = sesgo (brillo)
    alpha, beta = 1.4, 20
    ajustada = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    cv2.imwrite("ajustada.png", ajustada)
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
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

    img = cv2.imread("perro_coker.jpg")
    h, w = img.shape[:2]
    cx, cy = w / 2, h / 2
    angulo = 30

    M = cv2.getRotationMatrix2D((cx, cy), angulo, scale=1.0)

    # Calcula el bounding box rotado para no perder esquinas
    cos = abs(M[0, 0])
    sin = abs(M[0, 1])
    nuevo_w = int(h * sin + w * cos)
    nuevo_h = int(h * cos + w * sin)

    # Ajusta la traslación de la matriz para centrar el resultado
    M[0, 2] += (nuevo_w / 2) - cx
    M[1, 2] += (nuevo_h / 2) - cy

    rotada = cv2.warpAffine(img, M, (nuevo_w, nuevo_h))
    cv2.imwrite("rotada.png", rotada)
    return rotadaMostrar más20 mayClaude respondió: Hay dos problemas en mejoracontraste.Hay dos problemas en mejora_contraste.py y transformacion_rotacion.py que hay que corregir antes del README. Dentro de las funciones estás volviendo a cargar la imagen y hardcodeando los parámetros, lo que ignora todo lo que llega desde main.py:
mejora_contraste.py — corregir así:
pythonimport cv2

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
transformacion_rotacion.py — corregir así:
pythonimport cv2
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

    cos = abs(M[0, 0])
    sin = abs(M[0, 1])
    nuevo_w = int(h * sin + w * cos)
    nuevo_h = int(h * cos + w * sin)

    M[0, 2] += (nuevo_w / 2) - cx
    M[1, 2] += (nuevo_h / 2) - cy

    return cv2.warpAffine(img, M, (nuevo_w, nuevo_h))
La regla es: las funciones no cargan ni guardan imágenes, solo reciben, procesan y devuelven. El cv2.imread y cv2.imwrite van únicamente en main.py.