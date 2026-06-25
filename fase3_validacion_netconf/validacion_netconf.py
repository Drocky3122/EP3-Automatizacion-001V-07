#!/usr/bin/env python3
"""
fase3_validacion_netconf/validacion_netconf.py
EP3 - DRY7122 | Validacion via NETCONF con ncclient
Alumno: Gonzalez Hernandez Rodrigo | Codigo: 001V-07
"""

import sys
import os
import socket
import datetime
import yaml
from ncclient import manager
from lxml import etree

# ── Metadatos ─────────────────────────────────────────────────────────────
print("=" * 60)
print("  VALIDACION NETCONF - EP3 DRY7122")
print(f"  Script  : {os.path.basename(__file__)}")
print(f"  Fecha   : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"  Host VM : {socket.gethostname()}")
print(f"  Alumno  : 001V-07 - Gonzalez Hernandez Rodrigo")
print("=" * 60)
print()

# ── Cargar variables ──────────────────────────────────────────────────────
VARS_PATH = os.path.join(os.path.dirname(__file__), "../vars/vars_001V-07.yaml")
with open(VARS_PATH, "r") as f:
    v = yaml.safe_load(f)

router   = v["router"]
cliente  = v["cliente"]
alumno   = v["alumno"]

ROUTER_IP   = router["ip"]
USUARIO     = router["usuario"]
PASSWORD    = router["password"]
HOSTNAME_EXP = cliente["hostname"]
LOOPBACK_IP_EXP   = router["loopback_ip"]
LOOPBACK_MASK_EXP = router["loopback_mask"]
DESC_WAN_EXP      = router["descripcion_wan"]
NTP_EXP           = router["ntp_server"]
LOOPBACK_ID       = router["loopback_id"]

print(f"[INFO] Conectando a {ROUTER_IP}:830 via NETCONF ...")

# ── Filtro XML para modelo Cisco-IOS-XE-native ───────────────────────────
FILTER_XML = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname/>
    <banner/>
    <ntp/>
    <interface>
      <GigabitEthernet>
        <name>1</name>
        <description/>
      </GigabitEthernet>
      <Loopback>
        <name/>
        <ip/>
      </Loopback>
    </interface>
  </native>
</filter>
"""

# ── Conexión y get_config ─────────────────────────────────────────────────
try:
    with manager.connect(
        host=ROUTER_IP,
        port=830,
        username=USUARIO,
        password=PASSWORD,
        hostkey_verify=False,
        allow_agent=False,
        look_for_keys=False
    ) as m:
        print("[INFO] Sesion NETCONF establecida correctamente")

        reply = m.get_config(source="running", filter=FILTER_XML)
        xml_raw = reply.xml

        # Guardar XML crudo
        evidencias_dir = os.path.join(os.path.dirname(__file__), "evidencias")
        os.makedirs(evidencias_dir, exist_ok=True)
        xml_path = os.path.join(evidencias_dir, "rpc_reply_raw.xml")
        with open(xml_path, "w") as xf:
            xf.write(xml_raw)
        print(f"[INFO] XML crudo guardado en: {xml_path}")
        print()

        # ── Parsear XML ──────────────────────────────────────────────────
        root = etree.fromstring(xml_raw.encode())
        ns = {"ios": "http://cisco.com/ns/yang/Cisco-IOS-XE-native"}

        def get_text(element, xpath):
            node = element.find(xpath, ns)
            return node.text.strip() if node is not None and node.text else None

        # Extraer valores
        hostname_actual = get_text(root, ".//ios:native/ios:hostname")

        loopback_ip_actual   = None
        loopback_mask_actual = None
        for lb in root.findall(".//ios:native/ios:interface/ios:Loopback", ns):
            lb_name = get_text(lb, "ios:name")
            if lb_name == str(LOOPBACK_ID):
                loopback_ip_actual   = get_text(lb, ".//ios:primary/ios:address")
                loopback_mask_actual = get_text(lb, ".//ios:primary/ios:mask")

        desc_wan_actual = get_text(root, ".//ios:native/ios:interface/ios:GigabitEthernet/ios:description")
        ntp_actual      = get_text(root, ".//ios:native/ios:ntp/ios:server/ios:server-list/ios:ip-address")

        # ── Comparación y reporte ────────────────────────────────────────
        print("-" * 60)
        print("  REPORTE DE VALIDACION NETCONF")
        print("-" * 60)

        criterios = [
            ("Hostname corporativo", HOSTNAME_EXP,      hostname_actual),
            ("IP Loopback",          LOOPBACK_IP_EXP,   loopback_ip_actual),
            ("Mascara Loopback",     LOOPBACK_MASK_EXP, loopback_mask_actual),
            ("Descripcion WAN",      DESC_WAN_EXP,      desc_wan_actual),
            ("Servidor NTP",         NTP_EXP,           ntp_actual),
        ]

        resultados = []
        for nombre, esperado, obtenido in criterios:
            ok = (esperado == obtenido)
            estado = "[OK]  " if ok else "[FAIL]"
            resultados.append(ok)
            print(f"  {estado} {nombre}")
            print(f"         Esperado : {esperado}")
            print(f"         Obtenido : {obtenido}")
            print()

        total_ok = sum(resultados)
        total    = len(resultados)
        print("-" * 60)
        print(f"  Criterios CONFORME : {total_ok}/{total}")
        print()
        if total_ok == total:
            print("  *** RESULTADO GLOBAL: CONFORME ***")
        else:
            print("  *** RESULTADO GLOBAL: NO CONFORME ***")
        print("=" * 60)

except Exception as e:
    print(f"[ERROR] No se pudo conectar via NETCONF: {e}")
    sys.exit(1)
