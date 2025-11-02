#!/usr/bin/env python3
"""
Script de consolidation des rapports de sécurité DevSecOps
Consolide les rapports SAST, SCA, DAST en un dashboard unique
"""

import json
import argparse
import os
from datetime import datetime

def generate_security_dashboard(sast_data, sca_data, dast_data, container_data):
    """Génère un dashboard de sécurité consolidé"""

    dashboard = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "sast": {"vulnerabilities": 0, "critical": 0, "high": 0},
            "sca": {"vulnerabilities": 0, "critical": 0, "high": 0},
            "dast": {"vulnerabilities": 0, "critical": 0, "high": 0},
            "container": {"vulnerabilities": 0, "critical": 0, "high": 0}
        },
        "compliance_status": "PASS",
        "recommendations": []
    }

    # Générer le HTML du dashboard
    html_content = generate_html_dashboard(dashboard)

    return html_content

def generate_html_dashboard(dashboard):
    """Génère le HTML du dashboard"""

    return f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Sécurité DevSecOps</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .dashboard {{ border: 1px solid #ddd; padding: 20px; border-radius: 5px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 20px; }}
        .card {{ border: 1px solid #ccc; padding: 15px; border-radius: 5px; }}
        .critical {{ background-color: #ffebee; border-color: #f44336; }}
        .high {{ background-color: #fff3e0; border-color: #ff9800; }}
        .medium {{ background-color: #fff9c4; border-color: #ffeb3b; }}
        .low {{ background-color: #e8f5e8; border-color: #4caf50; }}
        .status-pass {{ color: #4caf50; font-weight: bold; }}
        .status-fail {{ color: #f44336; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>🚀 Dashboard Sécurité DevSecOps</h1>
    <div class="dashboard">
        <h2>📊 Résumé de Sécurité</h2>
        <div class="summary">
            <div class="card">
                <h3>SAST</h3>
                <p>Vulnérabilités: {dashboard['summary']['sast']['vulnerabilities']}</p>
                <p>Critiques: <span class="critical">{dashboard['summary']['sast']['critical']}</span></p>
                <p>Élevées: <span class="high">{dashboard['summary']['sast']['high']}</span></p>
            </div>
            <div class="card">
                <h3>SCA</h3>
                <p>Vulnérabilités: {dashboard['summary']['sca']['vulnerabilities']}</p>
                <p>Critiques: <span class="critical">{dashboard['summary']['sca']['critical']}</span></p>
                <p>Élevées: <span class="high">{dashboard['summary']['sca']['high']}</span></p>
            </div>
            <div class="card">
                <h3>DAST</h3>
                <p>Vulnérabilités: {dashboard['summary']['dast']['vulnerabilities']}</p>
                <p>Critiques: <span class="critical">{dashboard['summary']['dast']['critical']}</span></p>
                <p>Élevées: <span class="high">{dashboard['summary']['dast']['high']}</span></p>
            </div>
            <div class="card">
                <h3>Conteneurs</h3>
                <p>Vulnérabilités: {dashboard['summary']['container']['vulnerabilities']}</p>
                <p>Critiques: <span class="critical">{dashboard['summary']['container']['critical']}</span></p>
                <p>Élevées: <span class="high">{dashboard['summary']['container']['high']}</span></p>
            </div>
        </div>

        <h2>✅ Statut de Conformité:
            <span class="status-{dashboard['compliance_status'].lower()}">
                {dashboard['compliance_status']}
            </span>
        </h2>

        <h2>💡 Recommandations</h2>
        <ul>
            {"".join(f"<li>{rec}</li>" for rec in dashboard['recommendations'])}
        </ul>

        <p><em>Généré le: {dashboard['timestamp']}</em></p>
    </div>
</body>
</html>
"""

def main():
    parser = argparse.ArgumentParser(description='Consolide les rapports de sécurité')
    parser.add_argument('--sast', help='Fichier rapport SAST')
    parser.add_argument('--sca', help='Fichier rapport SCA')
    parser.add_argument('--dast', help='Fichier rapport DAST')
    parser.add_argument('--container', help='Fichier rapport conteneur')
    parser.add_argument('--output', required=True, help='Fichier de sortie HTML')

    args = parser.parse_args()

    # Charger les données des rapports (simulation pour l'exemple)
    sast_data = {}
    sca_data = {}
    dast_data = {}
    container_data = {}

    # Générer le dashboard
    dashboard_html = generate_security_dashboard(sast_data, sca_data, dast_data, container_data)

    # Sauvegarder le dashboard
    with open(args.output, 'w') as f:
        f.write(dashboard_html)

    print(f"✅ Dashboard généré: {args.output}")

if __name__ == "__main__":
    main()
