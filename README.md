
# Técnicas de procesamiento digital de imágenes

## Integrantes

- Rodríguez, Noelia
- Miño, Carla
- Armiento, Fernando
- Caviglia, Paula

---

## Descripci

Script en Python que permite cargar una imagen, aplicar tres técnicas distintas de procesamiento y guardar los resultados en disco. Desarrollado con **Pillow** y **OpenCV**.

---

## Requisitos

```bash
pip install opencv-python numpy
```

---

## Cómo correr el script

```bash
python main.py <ruta_imagen> [opciones]
```

### Parámetros

| Parámetro | Tipo  | Default | Descripción |
|---|---|---|---|---|
| `imagen` | string | — | Ruta a la imagen de entrada |
| `--alpha` | float |  1.4 | Ganancia de contraste |
| `--beta` | int | 20 | Sesgo de brillo |
| `--angulo` | float |  30.0 | Ángulo de rotación en grados |
| `--hsv-bajo` | int int int |  5 120 120 | Rango HSV mínimo para segmentación |
| `--hsv-alto` | int int int |  20 255 255 | Rango HSV máximo para segmentación |

### Ejemplos

```bash
# Con valores por defecto
python main.py perro_coker.jpg

# Personalizando contraste y brillo
python main.py perro_coker.jpg --alpha 1.8 --beta 30

# Personalizando rotación
python main.py perro_coker.jpg --angulo 45

# Personalizando segmentación por color
python main.py perro_coker.jpg --hsv-bajo 10 100 100 --hsv-alto 25 255 255

# Combinando todos los parámetros
python main.py perro_coker.jpg --alpha 1.8 --beta 30 --angulo 45 --hsv-bajo 10 100 100 --hsv-alto 25 255 255
```

---

## Técnicas aplicadas

### 1. Mejora de contraste y brillo (`mejora_contraste.py`)

Aplica la transformación lineal `g(x, y) = α · f(x, y) + β` sobre cada píxel de la imagen.

- **`alpha`** controla el contraste: valores mayores a 1 aumentan la diferencia entre píxeles claros y oscuros.
- **`beta`** controla el brillo: valores positivos aclaran la imagen globalmente.

**Efecto:** La imagen resultante tiene colores más definidos y mayor visibilidad en zonas con poca luz.

**Archivo de salida:** `resultado_brillo_contraste.png`

---

### 2. Transformación geométrica — Rotación (`transformacion_rotacion.py`)

Rota la imagen un ángulo dado alrededor de su centro, ajustando el tamaño del lienzo para que no se recorten las esquinas.

- Se calcula la matriz de rotación con `cv2.getRotationMatrix2D`.
- Se recalcula el bounding box del resultado para preservar el contenido completo.
- Se aplica la transformación con `cv2.warpAffine`.

**Efecto:** La imagen aparece rotada sin pérdida de información en los bordes.

**Archivo de salida:** `resultado_rotacion.png`

---

### 3. Análisis de segmentación por color (`analisis_segmentacion.py`)

Convierte la imagen al espacio de color HSV y extrae los píxeles que caen dentro de un rango de tono definido por el usuario.

- HSV separa el color (Hue) de la luminosidad, lo que hace más robusto el filtrado ante cambios de iluminación.
- Se genera una máscara binaria con `cv2.inRange`.
- Se aplica la máscara sobre la imagen original con `cv2.bitwise_and`.

**Efecto:** Se aíslan los píxeles del color del perro, produciendo una máscara y una imagen con solo la región segmentada visible.

**Archivos de salida:** `resultado_mascara_color.png`, `resultado_segmentacion.png`

---

## Decisiones técnicas

**¿Por qué `convertScaleAbs` para el contraste?**
Maneja automáticamente la saturación: los valores que superan 255 o bajan de 0 se recortan sin producir desbordamiento, lo que evita artefactos visuales.

**¿Por qué HSV para la segmentación?**
En el espacio BGR, un mismo color bajo distintas condiciones de iluminación produce valores muy distintos. HSV separa el tono (Hue) de la luminosidad (Value), lo que permite definir rangos de color más estables e intuitivos.

**¿Por qué recalcular el bounding box en la rotación?**
Con `cv2.warpAffine` sin ajuste, las esquinas de la imagen rotada quedan fuera del lienzo y se pierden. Recalcular el tamaño de salida garantiza que el contenido completo sea visible.

**¿Por qué separar en módulos?**
Cada archivo tiene una única responsabilidad: `main.py` orquesta, cada módulo aplica una técnica. Esto facilita el mantenimiento, las pruebas y la explicación de cada parte por separado.

---

## Estructura del proyecto

```
proyecto/
├── main.py                      # Punto de entrada y parseo de argumentos
├── mejora_contraste.py          # Técnica 1: ajuste de brillo y contraste
├── transformacion_rotacion.py   # Técnica 2: rotación geométrica
├── analisis_segmentacion.py     # Técnica 3: segmentación por color HSV
├── imagenes/
│   └── perro_coker.jpg
├── resultados/
│   ├── resultado_brillo_contraste.png
│   ├── resultado_rotacion.png
│   ├── resultado_mascara_color.png
│   └── resultado_segmentacion.png
└── README.md
```
