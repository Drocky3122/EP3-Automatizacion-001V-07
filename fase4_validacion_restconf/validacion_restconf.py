#!/usr/bin/env python3
"""
fase4_validacion_restconf/validacion_restconf.py
EP3 - DRY7122 | Validacion via RESTCONF con requests
Alumno: Gonzalez Hernandez Rodrigo | Codigo: 001V-07
"""

import sys
import os
import socket
import datetime
import json
import yaml
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("=" * 60)
print("  VALIDACION RESTCONF - EP3 DRY7122")
print(f"  Script  : {os.path.basename(__file__)}")
print(f"  Fecha   : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"  Host VM : {socket.gethostname()}")
print(f"  Alumno  : 001V-07 - Gonzalez Hernandez Rodrigo")
print("=" * 60)
print()

VARS_PATH = os.path.join(os.path.dirname(__file__), "../vars/vars_001V-07.yaml")
with open(VARS_PATH, "r") as f:
    v = yaml.safe_load(f)

router  = v["router"]
cliente = v["cliente"]

ROUTER_IP = router["ip"]
USUARIO   = router["usuario"]
PASSWORD  = router["password"]
BASE_URL  = f"https://{ROUTER_IP}/restconf/data"
HEADERS   = {"Accept": "application/yang-data+json"}
AUTH      = (USUARIO, PASSWORD)
LB_ID     = router["loopback_id"]

RESPONSES_DIR = os.path.join(os.path.dirname(__file__), "evidencias/responses")
os.makedirs(RESPONSES_DIR, exist_ok=True)

def get_endpoint(nombre, endpoint, archivo):
    url = f"{BASE_URL}/{endpoint}"
    print(f"[INFO] GET {url}")
    try:
        resp = requests.get(url, auth=AUTH, headers=HEADERS, verify=False, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        path = os.path.join(RESPONSES_DIR, archivo)
        with open(path, "w") as jf:
            json.dump(data, jf, indent=2)
        print(f"[INFO] Guardado: {archivo}")
        return data
    except Exception as e:
        print(f"[ERROR] {nombre}: {e}")
        return None

print("[INFO] Consultando endpoints RESTCONF ...")
print()

data_hostname   = get_endpoint("Hostname",       "Cisco-IOS-XE-native:native/hostname",                    "get_hostname.json")
data_loopback   = get_endpoint("Loopback",       f"ietf-interfaces:interfaces/interface=Loopback{LB_ID}",  "get_loopback.json")
data_interfaces = get_endpoint("GigabitEthernet1","ietf-interfaces:interfaces/interface=GigabitEthernet1", "get_interfaces.json")
data_ntp        = get_endpoint("NTP",            "Cisco-IOS-XE-native:native/ntp",                        "get_ntp.json")

# Extraer valores
hostname_actual = None
if data_hostname:
    hostname_actual = str(data_hostname.get("Cisco-IOS-XE-native:hostname", "")).strip()

loopback_ip_actual = None
if data_loopback:
    try:
        addrs = data_loopback["ietf-interfaces:interface"]["ietf-ip:ipv4"]["address"]
        if addrs:
            loopback_ip_actual = addrs[0].get("ip")
    except (KeyError, IndexError):
        pass

desc_wan_actual = None
if data_interfaces:
    try:
        desc_wan_actual = data_interfaces["ietf-interfaces:interface"].get("description", "").strip()
    except KeyError:
        pass

ntp_actual = None
if data_ntp:
    try:
        servers = data_ntp["Cisco-IOS-XE-native:ntp"]["Cisco-IOS-XE-ntp:server"]["server-list"]
        if servers:
            ntp_actual = servers[0].get("ip-address")
    except (KeyError, IndexError):
        pass

# Reporte
print()
print("-" * 60)
print("  REPORTE DE VALIDACION RESTCONF")
print("-" * 60)

criterios = [
    ("Hostname corporativo", cliente["hostname"],      hostname_actual),
    ("IP Loopback",          router["loopback_ip"],    loopback_ip_actual),
    ("Descripcion WAN",      router["descripcion_wan"], desc_wan_actual),
    ("Servidor NTP",         router["ntp_server"],     ntp_actual),
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
