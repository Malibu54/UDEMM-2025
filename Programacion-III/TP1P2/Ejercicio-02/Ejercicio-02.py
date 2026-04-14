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
        

