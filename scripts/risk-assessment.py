#!/usr/bin/env python3
import json
import sys
import argparse
import math
from datetime import datetime

class RiskCalculator:
    def __init__(self):
        self.risk_factors = {
            "exposure": {
                "internal": 0.1,
                "dmz": 0.5,
                "public": 0.9
            },
            "data_sensitivity": {
                "public": 0.1,
                "internal": 0.3,
                "confidential": 0.7,
                "restricted": 0.9
            },
            "business_impact": {
                "low": 0.2,
                "medium": 0.5,
                "high": 0.8,
                "critical": 1.0
            }
        }

    def calculate_vulnerability_risk(self, vuln_data, context):
        """Calcule le risque d'une vulnérabilité spécifique"""
        base_score = vuln_data.get('cvss_score', 0) / 10.0

        # Facteurs contextuels
        exposure_factor = self.risk_factors["exposure"].get(context.get("exposure", "internal"), 0.5)
        data_factor = self.risk_factors["data_sensitivity"].get(context.get("data_sensitivity", "internal"), 0.5)
        impact_factor = self.risk_factors["business_impact"].get(context.get("business_impact", "medium"), 0.5)

        # Calcul du risque contextuel
        contextual_risk = base_score * exposure_factor * data_factor * impact_factor

        return {
            "base_score": base_score,
            "contextual_score": contextual_risk,
            "level": self._get_risk_level(contextual_risk),
            "factors": {
                "exposure": exposure_factor,
                "data_sensitivity": data_factor,
                "business_impact": impact_factor
            }
        }

    def assess_application_risk(self, security_reports, app_context):
        """Évalue le risque global de l'application"""
        risks = []

        # Analyser les rapports SAST
        for issue in security_reports.get('sast', {}).get('issues', []):
            risk = self.calculate_vulnerability_risk(issue, app_context)
            risks.append(risk)

        # Analyser les rapports SCA
        for vuln in security_reports.get('sca', {}).get('vulnerabilities', []):
            risk = self.calculate_vulnerability_risk(vuln, app_context)
            risks.append(risk)

        # Analyser les rapports DAST
        for alert in security_reports.get('dast', {}).get('alerts', []):
            risk = self.calculate_vulnerability_risk(alert, app_context)
            risks.append(risk)

        # Calculer le risque global
        if risks:
            max_risk = max(r['contextual_score'] for r in risks)
            avg_risk = sum(r['contextual_score'] for r in risks) / len(risks)
            critical_count = sum(1 for r in risks if r['level'] == 'CRITICAL')
            high_count = sum(1 for r in risks if r['level'] == 'HIGH')
        else:
            max_risk = avg_risk = 0
            critical_count = high_count = 0

        overall_risk = max(max_risk, avg_risk * 1.5)  # Pénalité pour multiples risques

        return {
            "overall_risk_score": overall_risk,
            "overall_risk_level": self._get_risk_level(overall_risk),
            "vulnerability_count": len(risks),
            "critical_vulnerabilities": critical_count,
            "high_vulnerabilities": high_count,
            "detailed_risks": risks,
            "assessment_date": datetime.now().isoformat()
        }

    def _get_risk_level(self, score):
        """Convertit un score en niveau de risque"""
        if score >= 0.8:
            return "CRITICAL"
        elif score >= 0.6:
            return "HIGH"
        elif score >= 0.4:
            return "MEDIUM"
        elif score >= 0.2:
            return "LOW"
        else:
            return "VERY_LOW"

def main():
    parser = argparse.ArgumentParser(description='Évaluation des risques de sécurité')
    parser.add_argument('--sast-report', help='Rapport SAST (JSON)')
    parser.add_argument('--sca-report', help='Rapport SCA (JSON)')
    parser.add_argument('--dast-report', help='Rapport DAST (JSON)')
    parser.add_argument('--app-context', required=True, help='Contexte application (JSON)')
    parser.add_argument('--output', required=True, help='Fichier de sortie')

    args = parser.parse_args()

    # Chargement des rapports
    security_reports = {}

    if args.sast_report:
        with open(args.sast_report) as f:
            security_reports['sast'] = json.load(f)

    if args.sca_report:
        with open(args.sca_report) as f:
            security_reports['sca'] = json.load(f)

    if args.dast_report:
        with open(args.dast_report) as f:
            security_reports['dast'] = json.load(f)

    with open(args.app_context) as f:
        app_context = json.load(f)

    # Calcul des risques
    calculator = RiskCalculator()
    risk_assessment = calculator.assess_application_risk(security_reports, app_context)

    # Sauvegarde du rapport
    with open(args.output, 'w') as f:
        json.dump(risk_assessment, f, indent=2)

    print(f"Rapport d'évaluation des risques généré: {args.output}")
    print(f"Niveau de risque: {risk_assessment['overall_risk_level']}")
    print(f"Score: {risk_assessment['overall_risk_score']:.2f}")

    # Code de sortie basé sur le risque
    if risk_assessment['overall_risk_level'] in ['CRITICAL', 'HIGH']:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
