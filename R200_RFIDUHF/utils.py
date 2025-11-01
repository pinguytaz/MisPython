# -*- coding: utf-8 -*-
#########################################################################
#  Fco. Javier Rodriguez Navarro 
#  https://www.pinguytaz.net
#
#  Funciones auxiliares
#########################################################################

import re

#########################################################################
# hexdump     Convierte a STring datos bytes
#########################################################################
def hexdump(data: bytes) -> str:
    return " ".join(f"{b:02X}" for b in data)

#########################################################################
# parse_hex_bytes    pasa hexadecimal("AA FE") y lo pasa a bytes
#########################################################################
def parse_hex_bytes(s: str) -> bytes:
    if not isinstance(s, str):
        raise TypeError("La entrada debe ser str")

    # Elimina prefijos 0x y separadores no-hex, dejando solo [0-9A-Fa-f]
    s_norm = re.sub(r'0x', '', s, flags=re.IGNORECASE)
    hex_only = re.findall(r'[0-9A-Fa-f]{2}', s_norm)
    # Si hay número impar de dígitos hex, intenta recomponer o falla
    # (Aquí exigimos pares completos)
    if not hex_only and re.search(r'[0-9A-Fa-f]', s_norm):
        raise ValueError("Cadena hex con dígitos impares o mal formateada")
    return bytes(int(b, 16) for b in hex_only)

