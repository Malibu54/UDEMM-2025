from __future__ import annotations
import abc
import numpy as np


# ─────────────────────────────────────────────────────────────
# Clase base abstracta  (Template Method)
# ─────────────────────────────────────────────────────────────

class ProcessingPipeline(abc.ABC):

    def __init__(self) -> None:
        self._image_data: np.ndarray | None = None

    # ── Template Method ──────────────────────────────────────

    def execute(self, input_path: str, output_path: str) -> None:
        print(f"[{self.__class__.__name__}] iniciando pipeline")

        self._load_image(input_path)   
        self.pre_process()             
        self._image_data = self.apply_filter() 
        self.post_process()            
        self._save_image(output_path)  

        print(f"[{self.__class__.__name__}] imagen guardada → {output_path}\n")

    # ── Paso abstracto (obligatorio en subclases) ─────────────

    @abc.abstractmethod
    def apply_filter(self) -> np.ndarray:

    # ── Hooks (override opcional) ─────────────────────────────

        def pre_process(self) -> None:
            ...

        def post_process(self) -> None:
            ...

    # ── Métodos legacy (privados, no se sobreescriben) ────────

        def _load_image(self, path: str) -> None:
            print(f"  [legacy] cargando imagen desde '{path}'")

            self._image_data = np.zeros((256, 256, 3), dtype=np.uint8)

    def _save_image(self, path: str) -> None:

        print(f"  [legacy] guardando imagen en '{path}'")



# ─────────────────────────────────────────────────────────────
# Subclase 1 – Blur
# ─────────────────────────────────────────────────────────────

class BlurPipeline(ProcessingPipeline):


    def __init__(self, brightness_factor: float = 1.2, kernel_size: int = 5) -> None:
        super().__init__()
        self.brightness_factor = brightness_factor
        self.kernel_size = kernel_size

    # Hook ────────────────────────────────────────────────────

    def pre_process(self) -> None:
        print(f"  [hook] ajustando brillo × {self.brightness_factor}")

        self._image_data = np.clip(
            self._image_data.astype(np.float32) * self.brightness_factor, 0, 255
        ).astype(np.uint8)

    # Filtro abstracto ────────────────────────────────────────

    def apply_filter(self) -> np.ndarray:
        print(f"  [filtro] Gaussian Blur (kernel={self.kernel_size}×{self.kernel_size})")
        return self._image_data  


# ─────────────────────────────────────────────────────────────
# Subclase 2 – Sharpen
# ─────────────────────────────────────────────────────────────

class SharpenPipeline(ProcessingPipeline):

    SHARPEN_KERNEL = np.array([
        [ 0, -1,  0],
        [-1,  5, -1],
        [ 0, -1,  0],
    ], dtype=np.float32)

    # Hook ────────────────────────────────────────────────────

    def post_process(self) -> None:
        print("  [hook] convirtiendo a escala de grises")
        if self._image_data is not None and self._image_data.ndim == 3:

            gray = self._image_data.mean(axis=2).astype(np.uint8)
            self._image_data = np.stack([gray, gray, gray], axis=2)

    # Filtro abstracto ────────────────────────────────────────

    def apply_filter(self) -> np.ndarray:
        print("  [filtro] Sharpen – Unsharp Mask kernel")
        return self._image_data  


# ─────────────────────────────────────────────────────────────
# Subclase 3 – Edge Detection
# ─────────────────────────────────────────────────────────────

class EdgeDetectPipeline(ProcessingPipeline):

    def __init__(self, threshold1: int = 100, threshold2: int = 200) -> None:
        super().__init__()
        self.threshold1 = threshold1
        self.threshold2 = threshold2

    # Hook ────────────────────────────────────────────────────

    def pre_process(self) -> None:
        print("  [hook] convirtiendo a escala de grises (requerido por Canny)")
        if self._image_data is not None and self._image_data.ndim == 3:

            self._image_data = self._image_data.mean(axis=2).astype(np.uint8)

    # Filtro abstracto ────────────────────────────────────────

    def apply_filter(self) -> np.ndarray:
        print(
            f"  [filtro] Canny Edge Detection "
            f"(th1={self.threshold1}, th2={self.threshold2})"
        )

        return self._image_data  


