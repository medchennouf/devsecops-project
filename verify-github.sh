#!/bin/bash
echo "🌐 VÉRIFICATION GITHUB"
echo "====================="

echo "1. Votre repository :"
echo "   https://github.com/medchennouf/devsecops-project"
echo ""
echo "2. Vérifiez que :"
echo "   - Le code est bien présent"
echo "   - La branche 'main' existe"
echo "   - Le fichier 'Jenkinsfile-complet-devsecops' est présent"
echo ""
echo "3. Test de l'URL Git :"
curl -s https://github.com/medchennouf/devsecops-project | grep -q "devsecops" && echo "✅ Repository accessible" || echo "❌ Problème repository"
