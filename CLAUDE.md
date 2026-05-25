# P08 — Detector de Elipses por Transformada de Hough

Práctica 8 de Laboratorio de Visión por Computadora. Implementación nativa en Python del detector de elipses de **Yuen, Illingworth y Kittler (1988)** basada en la descomposición en dos etapas de la Transformada de Hough con restricción TM-line y Adaptive Hough Transform (AHT).

**Referencias canónicas**:
- Yuen H.K., Illingworth J., Kittler J. — *Ellipse Detection Using the Hough Transform* (1988)
- Illingworth J., Kittler J. — *A Survey of the Hough Transform*, CVGIP 44, 87–116 (1988)

---

## Comandos rápidos

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar detector sobre imagen de prueba
python -m ellipse_detector.cli --image data/test.png --output results/

# Ejecutar suite de tests
pytest tests/ -v

# Ejecutar con visualización
python -m ellipse_detector.cli --image data/test.png --visualize

# Verificar tipos
mypy ellipse_detector/

# Formatear código
black ellipse_detector/ tests/
```

---

## Arquitectura del proyecto

```
P08-ELIPSES/
├── ellipse_detector/
│   ├── __init__.py
│   ├── cli.py                  # Punto de entrada de línea de comandos
│   ├── pipeline.py             # Orquestador del pipeline completo
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   ├── edge_detector.py    # Detección de bordes (Canny / Spacek)
│   │   └── gradient.py         # Cálculo de gradientes y pendientes
│   ├── hough/
│   │   ├── __init__.py
│   │   ├── stage1_center.py    # Etapa 1: centro por restricción TM-line
│   │   ├── stage2_aht.py       # Etapa 2: B, D, C por AHT
│   │   └── accumulator.py      # Acumulador 2D y 3D (9×9×9)
│   ├── postprocessing/
│   │   ├── __init__.py
│   │   ├── peak_detector.py    # Detección de picos en acumuladores
│   │   └── ellipse_params.py   # Conversión (B,D,C) → (a, b, θ)
│   └── visualization/
│       ├── __init__.py
│       └── draw.py             # Dibujo de elipses sobre imagen original
├── tests/
│   ├── test_stage1.py
│   ├── test_stage2.py
│   ├── test_ellipse_params.py
│   └── data/                   # Imágenes sintéticas de prueba
├── data/                       # Imágenes de entrada
├── results/                    # Salida del detector
├── references/                 # PDFs originales
├── requirements.txt
└── CLAUDE.md
```

---

## Algoritmo: fundamento teórico

### El problema de los 5 parámetros

Una elipse general en el plano requiere 5 parámetros: `(x₀, y₀, a, b, θ)`. Un acumulador ingenuo con `α` intervalos por eje necesita `α⁵` celdas — inviable incluso para `α = 20` (3.2 millones de celdas sin contar la precisión necesaria).

**Solución**: descomposición secuencial en dos etapas de menor dimensión.

---

### Etapa 1 — Encontrar el centro (x₀, y₀)

#### Restricción TM-line (contribución central de Yuen et al.)

Dado un par de puntos de borde `P(x₁, y₁)` y `Q(x₂, y₂)` con pendientes de tangente `s₁` y `s₂` (obtenidas del gradiente de imagen):

1. **Calcular el punto de intersección de tangentes T**:
   ```
   t₁ = (y₁ - y₂ - s₁·x₁ + s₂·x₂) / (s₂ - s₁)
   t₂ = s₁·(t₁ - x₁) + y₁
   ```

2. **Calcular el punto medio M del segmento PQ**:
   ```
   m₁ = (x₁ + x₂) / 2
   m₂ = (y₁ + y₂) / 2
   ```

3. **El centro de la elipse yace sobre la línea TM** (siempre, sin requerir simetría):
   ```
   y·(t₁ - m₁) = x·(t₂ - m₂) + (t₂·m₁ - t₁·m₂)
   ```

4. **Votar solo el segmento MN** (no la línea completa), donde la longitud `L = |MN|` se fija por conocimiento previo del tamaño esperado de la elipse.

#### Restricción de emparejamiento

Para evitar pares cross-elipse entre elipses distintas:
```
|x₁ - x₂| < δ₁   AND   |y₁ - y₂| < δ₂
```
Donde `δ₁` y `δ₂` son parámetros configurables (típicamente 20–50 px).

#### Por qué es superior al enfoque clásico

El enfoque clásico (Tsukune & Goto, Tsuji & Matsumoto) requiere pares con **tangentes paralelas** — falla en elipses ocluidas o asimétricas. El enfoque TM-line funciona con cualquier par de puntos con tangentes **no paralelas**.

---

### Etapa 2 — Encontrar B, D, C con AHT

Una vez conocido el centro `(x₀, y₀)`, se traslada el origen allí. La ecuación de la elipse se simplifica de 5 a 3 parámetros:

```
X² + B·Y² + 2D·X·Y + C = 0,   con B - D² > 0
```

donde `X = x - x₀`, `Y = y - y₀`.

#### Algoritmo AHT (coarse-to-fine)

1. Iniciar un acumulador **9×9×9** cubriendo los rangos iniciales de `(B, D, C)`
2. Para cada punto de borde asociado al centro candidato, calcular la superficie en espacio `(B, D, C)` e incrementar las celdas intersectadas
3. Encontrar la celda con máximo de votos
4. **Centrar el acumulador** en esa celda y **reducir cada rango a 1/3**
5. Repetir hasta la resolución requerida (máximo ~10 iteraciones en la práctica)

**Costo por iteración**:
```
C_iter = 3 × 9² × n_puntos
```

El AHT varía resolución por parámetro de forma independiente — crítico porque `C` tiene un rango mucho mayor que `B` y `D`.

---

### Conversión a parámetros geométricos

Una vez obtenidos `B`, `D`, `C` para la ecuación centrada:

```python
discriminant = sqrt((B - 1)**2 + 4 * D**2)

a = sqrt(-2 * C / ((B + 1) - discriminant))   # semieje mayor
b = sqrt(-2 * C / ((B + 1) + discriminant))   # semieje menor
theta = 0.5 * arctan(2 * D / (1 - B))         # ángulo de rotación (rad)
```

**Condición de validez**: `B - D² > 0` (garantiza que es elipse y no hipérbola).

---

### Detección de múltiples elipses

Para imágenes con `k` elipses:

1. Ejecutar Etapa 1 sobre todos los puntos de borde
2. Aceptar el centro si el conteo en el acumulador supera un umbral `τ`
3. Ejecutar Etapa 2 para obtener `B, D, C`
4. **Eliminar los puntos de borde** asociados a la elipse encontrada
5. Repetir Etapa 1 sobre los puntos restantes
6. Detener cuando el máximo del acumulador < `τ`

**Complejidad total**: `O(k²)` — cada elipse adicional requiere re-acumular.

---

## Convenciones de implementación

### Tipos y estructuras de datos

```python
from dataclasses import dataclass
import numpy as np

@dataclass
class EdgePoint:
    x: float
    y: float
    slope: float          # pendiente de tangente (dy/dx del gradiente)

@dataclass
class EllipseCandidate:
    center_x: float
    center_y: float
    B: float
    D: float
    C: float

@dataclass
class Ellipse:
    center_x: float
    center_y: float
    semi_major: float     # a
    semi_minor: float     # b
    angle_rad: float      # θ
    votes: int            # soporte en acumulador
```

### Reglas de codificación

- **Lenguaje**: Python 3.11+ con `numpy` para operaciones matriciales, sin dependencias de OpenCV para el algoritmo central
- **Nombres**: `snake_case` para variables y funciones, `PascalCase` para clases
- **Constantes**: `UPPER_SNAKE_CASE` — nunca magic numbers en el código
- **Longitud de función**: máximo 40 líneas — extraer helpers si se supera
- **Sin comentarios obvios** — los nombres de variables deben ser auto-documentados
- **Typing completo**: todas las funciones públicas llevan anotaciones de tipo

### Constantes del algoritmo

```python
# stage1_center.py
AHT_ACCUMULATOR_SIZE = 9        # 9×9×9 para Stage 2
AHT_MAX_ITERATIONS = 10         # convergencia garantizada en práctica
AHT_RANGE_REDUCTION = 1 / 3    # factor de reducción por iteración

# Restricción de emparejamiento — ajustar según tamaño de imagen
DEFAULT_DELTA_X = 30            # δ₁ en píxeles
DEFAULT_DELTA_Y = 30            # δ₂ en píxeles

CENTER_VOTE_THRESHOLD = 5       # τ mínimo para aceptar un centro
```

---

## Diseño del pipeline

```
Imagen de entrada
      │
      ▼
┌─────────────────┐
│  Detección de   │  Canny o Spacek — produce puntos (x, y, dx, dy)
│  bordes         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Cálculo de     │  slope = dy/dx para cada punto de borde
│  gradientes     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  ETAPA 1 — Búsqueda de centros      │
│  • Generar pares (P, Q) con δ-check │
│  • Calcular línea TM por par        │
│  • Votar segmento MN en acumulador  │
│  • Detectar picos (centros)         │
└────────┬────────────────────────────┘
         │  centros candidatos
         ▼
┌─────────────────────────────────────┐
│  ETAPA 2 — AHT por cada centro      │
│  • Traducir puntos al nuevo origen  │
│  • Acumulador 9×9×9 coarse-to-fine  │
│  • Extraer (B, D, C) del pico       │
│  • Validar B - D² > 0               │
└────────┬────────────────────────────┘
         │  parámetros (B, D, C)
         ▼
┌─────────────────┐
│  Conversión a   │  → (a, b, θ) geométricos
│  (a, b, θ)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Eliminación de │  Borrar puntos de la elipse encontrada
│  puntos         │  → repetir si quedan elipses
└────────┬────────┘
         │
         ▼
    Elipses detectadas
```

---

## Dependencias

```
numpy>=1.26          # operaciones matriciales vectorizadas
scipy>=1.12          # detección de picos, filtros
Pillow>=10.0         # lectura/escritura de imágenes
matplotlib>=3.8      # visualización de resultados
```

**No se usa OpenCV** en el algoritmo central — toda la lógica HT es implementación propia. OpenCV puede usarse opcionalmente solo en preprocessing si se indica explícitamente.

---

## Tests

Los tests verifican **comportamiento observable**, no implementación interna.

```
tests/
├── test_stage1.py          # TM-line produce centros correctos en elipses sintéticas
├── test_stage2.py          # AHT converge a (B, D, C) correctos en < 10 iter
├── test_ellipse_params.py  # Conversión (B,D,C) → (a,b,θ) con tolerancia numérica
├── test_pipeline.py        # Detección end-to-end en imágenes sintéticas conocidas
└── data/
    ├── single_ellipse.png  # Una elipse en blanco
    ├── multi_ellipse.png   # 3 elipses sin oclusión
    └── occluded.png        # Elipses parcialmente ocluidas
```

Tolerancias de aceptación para tests de regresión:
- Centro: error < 2 px
- Semiejes: error < 3%
- Ángulo θ: error < 2°

---

## Decisiones de diseño

### Por qué no usar OpenCV para el algoritmo HT

`cv2.HoughEllipses` no implementa el método de Yuen — usa una variante diferente. El propósito de la práctica es implementar el paper original, por lo que toda la lógica de acumulación es propia.

### Por qué numpy vectorizado en el emparejamiento

La Etapa 1 es `O(n²)` en puntos de borde. Implementarlo con bucles Python puro es ~100× más lento que numpy broadcasting. Se usa `np.triu_indices` para generar pares sin repetición.

### Por qué AHT y no acumulador uniforme para Etapa 2

Un acumulador uniforme en 3D con resolución fina exigiría demasiada memoria y tiempo. El AHT coarse-to-fine converge en ≤10 iteraciones con un acumulador fijo de 9³ = 729 celdas, independiente de la resolución final requerida.

### Longitud del segmento MN en Stage 1

El parámetro `L` (longitud de voto sobre la línea TM) se fija por conocimiento previo del tamaño esperado de las elipses. Un valor demasiado grande introduce votos espurios; demasiado pequeño pierde el centro verdadero. Default: `L = 0.3 × min(imagen_alto, imagen_ancho)`.

---

## Parámetros configurables

| Parámetro | Default | Descripción |
|---|---|---|
| `delta_x` | 30 px | Restricción horizontal de emparejamiento (δ₁) |
| `delta_y` | 30 px | Restricción vertical de emparejamiento (δ₂) |
| `vote_segment_length` | 0.3 × min(H,W) | Longitud del segmento MN en Stage 1 |
| `center_threshold` | 5 | Votos mínimos para aceptar un centro (τ) |
| `aht_iterations` | 10 | Iteraciones máximas del AHT |
| `aht_init_range_B` | (0.1, 10.0) | Rango inicial para B |
| `aht_init_range_D` | (-5.0, 5.0) | Rango inicial para D |
| `aht_init_range_C` | (-1e6, -1.0) | Rango inicial para C |
| `canny_low` | 50 | Umbral bajo de Canny |
| `canny_high` | 150 | Umbral alto de Canny |

---

## Notas de implementación importantes

- **Tangentes paralelas**: descartar pares donde `|s₁ - s₂| < ε` (ε ≈ 0.01) — la fórmula del punto T diverge.
- **Punto T fuera de la imagen**: descartar el par — el segmento MN quedaría fuera del dominio.
- **Validación de elipse**: verificar `B - D² > 0` antes de calcular `a`, `b`, `θ`. Si falla, la celda AHT ganadora es inválida.
- **Orden de semiejes**: asegurar siempre `a ≥ b` intercambiando si es necesario y ajustando `θ` en `π/2`.
- **Rango de θ**: mantener `θ ∈ (-π/2, π/2]` para representación canónica.
