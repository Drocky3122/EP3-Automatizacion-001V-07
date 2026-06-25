# EP3 — Implementación de Automatización de Red con Compliance Auditado
**DRY7122 — Programación y Redes Virtualizadas (SDN-NFV)**  
**DUOC UC — Escuela de Informática y Telecomunicaciones**

| Campo | Valor |
|-------|-------|
| Alumno | Gonzalez Hernandez Rodrigo |
| Código | 001V-07 |
| Sección | 001V |
| Empresa cliente | Planta Industrial Ltda |
| Hostname router | RTR-PLANTIND |

---

## 1. Objetivo del Proyecto

El proyecto consistió en incorporar un nuevo router (Cisco CSR1kv) a la red corporativa de **Planta Industrial Ltda**, ejecutando el ciclo completo de implementación automatizada. El objetivo fue dejar el equipo completamente configurado bajo los estándares corporativos de la empresa, con evidencia auditada de cada etapa del proceso mediante un repositorio GitHub.

---

## 2. Alcance

**Dentro del alcance:**
- Captura del estado inicial del router (baseline) antes de cualquier modificación.
- Habilitación de los servicios de automatización: NETCONF (puerto 830) y RESTCONF (HTTPS).
- Aplicación de configuración corporativa: hostname, banner, NTP, descripción WAN e interfaz Loopback de gestión.
- Validación independiente de la configuración aplicada mediante NETCONF y RESTCONF.
- Generación de un certificado de compliance que certifica el estado final del equipo.
- Registro auditado de toda la actividad en repositorio GitHub.

**Fuera del alcance:**
- Configuración de protocolos de enrutamiento dinámico (OSPF, BGP).
- Configuración de VLANs o segmentación de red.
- Integración con sistemas de monitoreo externos (Nagios, Zabbix).
- Configuración de interfaces adicionales más allá de GigabitEthernet1 y Loopback7.

**Herramientas utilizadas:** pyATS/Genie, Ansible, ncclient (NETCONF), Python requests (RESTCONF), Git/GitHub.

---

## 3. Infraestructura Utilizada

| Componente | Detalle |
|-----------|---------|
| Estación de trabajo | DEVASC VM (devasc@labvm) |
| Sistema operativo VM | Ubuntu 20.04 LTS |
| Router configurado | Cisco CSR1000v (IOS-XE) |
| IP del router | 192.168.56.101 |
| Python | 3.8+ |
| Ansible | 2.12+ |
| pyATS / Genie | 23.x |
| ncclient | 0.6.x |
| Git | 2.x |

---

## 4. Tecnologías Empleadas y Justificación

| Herramienta | Fase | Justificación |
|-------------|------|---------------|
| **pyATS / Genie** | Fase 1 y 5 | Permite capturar el estado estructurado del router (interfaces, rutas, plataforma) vía SSH, sin requerir NETCONF habilitado. Facilita comparar estados antes/después con `genie diff`. |
| **Ansible** | Fase 2 | Herramienta de aprovisionamiento idempotente que permite aplicar la configuración corporativa de forma declarativa y reproducible, usando módulos nativos `ios_config` e `ios_command`. |
| **NETCONF / ncclient** | Fase 3 | Protocolo estándar (RFC 6241) que devuelve el árbol completo de configuración en XML, permitiendo una validación detallada e independiente de Ansible. |
| **RESTCONF / requests** | Fase 4 | Permite consultar recursos de configuración específicos vía HTTP/JSON, complementando la validación NETCONF con una interfaz más liviana orientada a APIs REST. |

---

## 5. Configuración Aplicada

| Parámetro | Valor configurado |
|-----------|------------------|
| Hostname | `RTR-PLANTIND` |
| Banner de acceso | `ACCESO RESTRINGIDO - PLANTIND` |
| Interfaz Loopback | `Loopback7` — `10.1.7.1 / 255.255.255.0` |
| Descripción GigabitEthernet1 | `Enlace-WAN-Iquique` |
| Servidor NTP | `9.9.9.9` |
| NETCONF | Habilitado — puerto 830 |
| RESTCONF | Habilitado — HTTPS |
| HTTP seguro | `ip http secure-server` habilitado |

---

## 6. Resultados de Validación

### Validación NETCONF (Fase 3)

| Criterio | Esperado | Resultado |
|---------|----------|-----------|
| Hostname corporativo | `RTR-PLANTIND` | CONFORME |
| IP Loopback | `10.1.7.1` | CONFORME |
| Máscara Loopback | `255.255.255.0` | CONFORME |
| Descripción WAN | `Enlace-WAN-Iquique` | CONFORME |
| Servidor NTP | `9.9.9.9` | CONFORME |

**Resultado NETCONF: 5/5 CONFORME**

### Validación RESTCONF (Fase 4)

| Criterio | Esperado | Resultado |
|---------|----------|-----------|
| Hostname corporativo | `RTR-PLANTIND` | CONFORME |
| IP Loopback | `10.1.7.1` | CONFORME |
| Descripción WAN | `Enlace-WAN-Iquique` | CONFORME |
| Servidor NTP | `9.9.9.9` | CONFORME |

**Resultado RESTCONF: 4/4 CONFORME**

---

## 7. Conclusiones

El router Cisco CSR1kv fue incorporado exitosamente a la red corporativa de **Planta Industrial Ltda** cumpliendo al 100% los requisitos de configuración estándar de la empresa. El ciclo completo de automatización fue ejecutado en cinco fases:

1. **Baseline documentado:** el estado inicial del router quedó registrado antes de cualquier cambio, permitiendo auditar las diferencias post-aprovisionamiento mediante `genie diff`.
2. **Aprovisionamiento idempotente:** el playbook Ansible fue verificado en dos ejecuciones consecutivas, demostrando que la segunda ejecución no genera cambios innecesarios en el equipo.
3. **Validación dual independiente:** la configuración fue verificada de forma independiente mediante NETCONF y RESTCONF, obteniendo 100% de criterios conformes en ambas tecnologías.
4. **Entrega a operaciones:** el equipo queda listo para operar en producción con el certificado de compliance `certificado_compliance_001V-07.txt` emitido como cierre formal del ticket de implementación.

Toda la actividad quedó registrada en este repositorio con un historial de commits que permite auditar qué se hizo, cuándo y cómo, cumpliendo con los requerimientos de trazabilidad del cliente.

---

## Estructura del Repositorio

```
ep3-automatizacion-001V-07/
├── README.md
├── vars/
│   └── vars_001V-07.yaml
├── fase1_baseline/
│   ├── testbed_001V-07.yaml
│   ├── run_fase1.sh
│   └── evidencias/
│       ├── output_fase1.txt
│       └── baseline_001V-07/
├── fase2_aprovisionamiento/
│   ├── inventario.ini
│   ├── playbook_001V-07.yaml
│   ├── run_fase2.sh
│   ├── respaldo/
│   │   └── backup_001V-07.cfg
│   └── evidencias/
│       ├── output_primera_ejecucion.txt
│       └── output_segunda_ejecucion.txt
├── fase3_validacion_netconf/
│   ├── validacion_netconf.py
│   └── evidencias/
│       ├── rpc_reply_raw.xml
│       └── output_validacion_netconf.txt
├── fase4_validacion_restconf/
│   ├── validacion_restconf.py
│   └── evidencias/
│       ├── output_validacion_restconf.txt
│       └── responses/
│           ├── get_hostname.json
│           ├── get_loopback.json
│           ├── get_interfaces.json
│           └── get_ntp.json
└── fase5_reporte/
    ├── generar_certificado.py
    ├── run_fase5.sh
    └── evidencias/
        ├── output_fase5.txt
        ├── snapshot_final_001V-07/
        ├── diff_001V-07/
        └── certificado_compliance_001V-07.txt
```
