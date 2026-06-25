#!/usr/bin/env python3
"""
fase5_reporte/generar_certificado.py
EP3 - DRY7122 | Generador de certificado de compliance
Alumno: Gonzalez Hernandez Rodrigo | Codigo: 001V-07
"""

import os
import datetime
import socket
import yaml

# ── Cargar variables ──────────────────────────────────────────────────────
VARS_PATH = os.path.join(os.path.dirname(__file__), "../vars/vars_001V-07.yaml")
with open(VARS_PATH, "r") as f:
    v = yaml.safe_load(f)

alumno  = v["alumno"]
cliente = v["cliente"]
router  = v["router"]

EVIDENCIAS  = os.path.join(os.path.dirname(__file__), "evidencias")
FASE3_OUT   = os.path.join(os.path.dirname(__file__), "../fase3_validacion_netconf/evidencias/output_validacion_netconf.txt")
FASE4_OUT   = os.path.join(os.path.dirname(__file__), "../fase4_validacion_restconf/evidencias/output_validacion_restconf.txt")
DIFF_DIR    = os.path.join(EVIDENCIAS, f"diff_{alumno['codigo']}")
CERT_PATH   = os.path.join(EVIDENCIAS, f"certificado_compliance_{alumno['codigo']}.txt")

def leer_resultado(ruta, total_esperado):
    """Lee el output de una fase y determina si es CONFORME."""
    try:
        with open(ruta, "r") as f:
            contenido = f.read()
        ok_count = contenido.count("[OK]")
        if ok_count >= total_esperado and "CONFORME" in contenido and "NO CONFORME" not in contenido.split("RESULTADO")[1]:
            return "CONFORME", ok_count, total_esperado
        else:
            return "NO CONFORME", ok_count, total_esperado
    except FileNotFoundError:
        return "NO EJECUTADO", 0, total_esperado

def contar_diff():
    """Verifica si el diff contiene cambios."""
    if not os.path.isdir(DIFF_DIR):
        return False, "Directorio diff no encontrado"
    archivos = [f for f in os.listdir(DIFF_DIR) if os.path.isfile(os.path.join(DIFF_DIR, f))]
    if not archivos:
        return False, "Directorio diff vacío"
    # Revisar si hay contenido en los archivos
    for archivo in archivos:
        ruta = os.path.join(DIFF_DIR, archivo)
        if os.path.getsize(ruta) > 0:
            return True, f"{len(archivos)} archivo(s) con diferencias detectadas"
    return False, "Archivos diff vacíos (sin cambios detectados)"

# ── Evaluar fases ─────────────────────────────────────────────────────────
resultado_netconf,  ok_netconf,  total_netconf  = leer_resultado(FASE3_OUT, 5)
resultado_restconf, ok_restconf, total_restconf = leer_resultado(FASE4_OUT, 4)
diff_ok, diff_msg = contar_diff()

resultado_diff = "CONFORME" if diff_ok else "NO CONFORME"

# Resultado global
if resultado_netconf == "CONFORME" and resultado_restconf == "CONFORME" and diff_ok:
    resultado_global = "CONFORME"
else:
    resultado_global = "NO CONFORME"

# ── Generar certificado ───────────────────────────────────────────────────
now = datetime.datetime.now()
linea = "=" * 64

cert = f"""
{linea}
       CERTIFICADO DE COMPLIANCE - EP3 DRY7122
       Programacion y Redes Virtualizadas (SDN-NFV)
       DUOC UC - Escuela de Informatica y Telecomunicaciones
{linea}

DATOS DEL ALUMNO
  Codigo   : {alumno['codigo']}
  Nombre   : {alumno['nombre']}
  Seccion  : 001V

DATOS DEL PROYECTO
  Empresa cliente  : {cliente['empresa']}
  Hostname router  : {cliente['hostname']}
  IP Router        : {router['ip']}
  IP Loopback      : {router['loopback_ip']}/{router['loopback_prefix']}
  Descripcion WAN  : {router['descripcion_wan']}
  Servidor NTP     : {router['ntp_server']}

FECHA DE EMISION
  {now.strftime('%Y-%m-%d %H:%M:%S')}
  Host VM : {socket.gethostname()}

{linea}
RESULTADOS DE VALIDACION
{linea}

  [NETCONF]   Criterios conformes : {ok_netconf}/{total_netconf}
              Resultado           : {resultado_netconf}

  [RESTCONF]  Criterios conformes : {ok_restconf}/{total_restconf}
              Resultado           : {resultado_restconf}

  [DIFF]      Cambios detectados  : {diff_msg}
              Resultado           : {resultado_diff}

{linea}
  RESULTADO GLOBAL DE COMPLIANCE : *** {resultado_global} ***
{linea}

RESUMEN DE CONFIGURACION APLICADA
  - Hostname corporativo : {cliente['hostname']}
  - Banner de acceso     : {router['banner']}
  - Loopback{router['loopback_id']}           : {router['loopback_ip']} / {router['loopback_mask']}
  - Descripcion GE1      : {router['descripcion_wan']}
  - Servidor NTP         : {router['ntp_server']}
  - NETCONF habilitado   : Si (puerto 830)
  - RESTCONF habilitado  : Si (HTTPS)

  El equipo ha sido configurado segun los estandares corporativos
  de {cliente['empresa']} y esta listo para operar en produccion.

{linea}
  Generado automaticamente por generar_certificado.py
  EP3 - DRY7122 | {now.strftime('%Y-%m-%d')}
{linea}
"""

os.makedirs(EVIDENCIAS, exist_ok=True)
with open(CERT_PATH, "w") as f:
    f.write(cert)

print(cert)
print(f"[INFO] Certificado guardado en: {CERT_PATH}")
