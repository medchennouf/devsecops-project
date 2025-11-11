#!/bin/bash
echo "🔐 CORRECTION AUTHENTIFICATION GITHUB"
echo "===================================="

echo "1. Configuration des credentials Git..."
git config --global credential.helper store

echo "2. Nouvelle tentative de push..."
echo "   Username: medchennouf"
echo "   Password: [REDACTED_FOR_SECURITY]"
git push origin main

echo ""
echo "✅ Si réussi, Jenkins va détecter le changement dans 2 minutes !"
