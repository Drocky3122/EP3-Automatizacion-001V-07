#!/bin/bash
# fase1_baseline/run_fase1.sh
# Captura baseline del router con Genie
# Alumno: Gonzalez Hernandez Rodrigo | Codigo: 001V-07

cd ~/ep3-automatizacion-001V-07/fase1_baseline

echo "=== BASELINE SNAPSHOT ===" | tee evidencias/output_fase1.txt
echo "Alumno : 001V-07 - Gonzalez Hernandez Rodrigo" | tee -a evidencias/output_fase1.txt
echo "Fecha  : $(date)" | tee -a evidencias/output_fase1.txt
echo "Host   : $(hostname)" | tee -a evidencias/output_fase1.txt
echo "=========================" | tee -a evidencias/output_fase1.txt

genie learn interface platform routing \
  --testbed-file testbed_001V-07.yaml \
  --devices CSR1kv \
  --output evidencias/baseline_001V-07 2>&1 | tee -a evidencias/output_fase1.txt

echo "" | tee -a evidencias/output_fase1.txt
echo "=== BASELINE COMPLETADO ===" | tee -a evidencias/output_fase1.txt
echo "Archivos generados en: evidencias/baseline_001V-07/" | tee -a evidencias/output_fase1.txt
ls evidencias/baseline_001V-07/ | tee -a evidencias/output_fase1.txt
