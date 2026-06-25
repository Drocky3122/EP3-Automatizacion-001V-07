#!/bin/bash
# fase2_aprovisionamiento/run_fase2.sh
# EP3 - DRY7122 | Alumno: 001V-07

cd ~/ep3-automatizacion-001V-07/fase2_aprovisionamiento

echo "=== FASE 2: PRIMERA EJECUCION ==="
ansible-playbook -i inventario.ini playbook_001V-07.yaml | tee evidencias/output_primera_ejecucion.txt

echo ""
echo "=== FASE 2: SEGUNDA EJECUCION (idempotencia) ==="
ansible-playbook -i inventario.ini playbook_001V-07.yaml | tee evidencias/output_segunda_ejecucion.txt

echo ""
echo "=== VERIFICANDO RESPALDO ==="
head -10 respaldo/backup_001V-07.cfg
