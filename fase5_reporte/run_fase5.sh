#!/bin/bash
# fase5_reporte/run_fase5.sh
# EP3 - DRY7122 | Fase 5: Snapshot final, diff y certificado
# Alumno: Gonzalez Hernandez Rodrigo | Codigo: 001V-07

cd ~/ep3-automatizacion-001V-07/fase5_reporte

echo "=== FASE 5: SNAPSHOT FINAL ==="
genie learn interface platform routing \
  --testbed-file ../fase1_baseline/testbed_001V-07.yaml \
  --devices CSR1kv \
  --output evidencias/snapshot_final_001V-07

echo ""
echo "=== FASE 5: DIFF BASELINE vs FINAL ==="
genie diff \
  ../fase1_baseline/evidencias/baseline_001V-07 \
  evidencias/snapshot_final_001V-07 \
  --output evidencias/diff_001V-07

echo ""
echo "=== FASE 5: GENERANDO CERTIFICADO ==="
python3 generar_certificado.py | tee evidencias/output_fase5.txt
