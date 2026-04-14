from __future__ import annotations
from abc import ABC, abstractmethod
from typing import BinaryIO
 
 
# ─────────────────────────────────────────────
#  STRATEGY – Jerarquía de codecs
# ─────────────────────────────────────────────

class VideoCodec(ABC):
 
    @abstractmethod
    def encode(self, data: bytes) -> bytes:
        ...
 
    @abstractmethod
    def decode(self, data: bytes) -> bytes:
        ...
 
    @property
    @abstractmethod
    def name(self) -> str:
        ...

class H264Codec(VideoCodec):
    name = "H.264 (AVC)"
 
    def encode(self, data: bytes) -> bytes:
        print(f"  [{self.name}] Encoding {len(data)} bytes → high compatibility")
        return data  # simulación
 
    def decode(self, data: bytes) -> bytes:
        print(f"  [{self.name}] Decoding {len(data)} bytes")
        return data
    
class H265Codec(VideoCodec):
    name = "H.265 (HEVC)"
 
    def encode(self, data: bytes) -> bytes:
        print(f"  [{self.name}] Encoding {len(data)} bytes → ~50% smaller than H.264")
        return data
 
    def decode(self, data: bytes) -> bytes:
        print(f"  [{self.name}] Decoding {len(data)} bytes")
        return data
    
class AV1Codec(VideoCodec):
    name = "AV1"
 
    def encode(self, data: bytes) -> bytes:
        print(f"  [{self.name}] Encoding {len(data)} bytes → best ratio, royalty-free")
        return data
 
    def decode(self, data: bytes) -> bytes:
        print(f"  [{self.name}] Decoding {len(data)} bytes")
        return data
    
class VP8Codec(VideoCodec):
    name = "VP8"
 
    def encode(self, data: bytes) -> bytes:
        print(f"  [{self.name}] Encoding {len(data)} bytes → legacy WebRTC codec")
        return data
 
    def decode(self, data: bytes) -> bytes:
        print(f"  [{self.name}] Decoding {len(data)} bytes")
        return data
 
 
# ─────────────────────────────────────────────
#  FACTORY – registro centralizado de codecs
# ─────────────────────────────────────────────

class CodecFactory:
        _registry: dict[str, type[VideoCodec]] = {
        "h264": H264Codec,
        "h265": H265Codec,
        "av1":  AV1Codec,
        "vp8":  VP8Codec,
    }
        @classmethod
        def register(cls, key: str, codec_class: type[VideoCodec]) -> None:
            cls._registry[key.lower()] = codec_class
 
        @classmethod
        def create(cls, name: str) -> VideoCodec:
            key = name.lower()
            if key not in cls._registry:
                available = ", ".join(cls._registry)
                raise ValueError(f"Codec '{name}' not found. Available: {available}")
            return cls._registry[key]()
        

        @classmethod
        def available(cls) -> list[str]:
            return list(cls._registry.keys())
 
 
# ─────────────────────────────────────────────
#  BRIDGE – Abstracción de entrega de streaming
# ─────────────────────────────────────────────

class StreamingDelivery(ABC):
    def __init__(self, codec: VideoCodec) -> None:
        self._codec = codec
 
    def set_codec(self, codec: VideoCodec) -> None:
       
        print(f"  Codec switched → {codec.name}")
        self._codec = codec

    # Template Method: fuerza el orden correcto open→encode→close
    def stream(self, path: str) -> bytes:
        handle = self._open(path)
        try:
            raw = self._read(handle)
            encoded = self._codec.encode(raw)
            return encoded
        finally:
            self._close(handle)
 
    # ── Operaciones de I/O que cada subclase implementa ──
 
    @abstractmethod
    def _open(self, path: str) -> BinaryIO:
        ...

    @abstractmethod
    def _read(self, handle: BinaryIO) -> bytes:
        ...
 
    @abstractmethod
    def _close(self, handle: BinaryIO) -> None:
        ...  
class LiveStreamDelivery(StreamingDelivery):
 
    def _open(self, path: str) -> BinaryIO:
        print(f"  [Live] Opening live source: {path}")
        return open(path, "rb")
 
    def _read(self, handle: BinaryIO) -> bytes:
        data = handle.read()
        print(f"  [Live] Read {len(data)} bytes from live source")
        return data
 
    def _close(self, handle: BinaryIO) -> None:
        handle.close()
        print("  [Live] Live source closed")

class VodDelivery(StreamingDelivery):
 
    def _open(self, path: str) -> BinaryIO:
        print(f"  [VoD]  Opening VoD file: {path}")
        return open(path, "rb")
 
    def _read(self, handle: BinaryIO) -> bytes:
        data = handle.read()
        print(f"  [VoD]  Read {len(data)} bytes (buffered)")
        return data
 
    def _close(self, handle: BinaryIO) -> None:
        handle.close()
        print("  [VoD]  VoD file closed")

# ─────────────────────────────────────────────
#  CLIENTE
# ─────────────────────────────────────────────
 
class StreamingClient:
        def __init__(self, delivery: StreamingDelivery) -> None:
            self._delivery = delivery
 
        def play(self, path: str, codec_name: str = "h264") -> bytes:
            codec = CodecFactory.create(codec_name)
            self._delivery.set_codec(codec)
            print(f"\n▶ Streaming '{path}' with {codec.name}")
            return self._delivery.stream(path)
 
        def switch_codec(self, name: str) -> None:
            self._delivery.set_codec(CodecFactory.create(name))