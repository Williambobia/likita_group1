"""
Script pour extraire les images du PDF de logos LIKITA
"""
import sys
import os
from pathlib import Path

try:
    from pdf2image import convert_from_path
    from PIL import Image
except ImportError:
    print("Installation des dépendances nécessaires...")
    print("Veuillez exécuter: pip install pdf2image poppler")
    print("Pour Windows, téléchargez Poppler depuis: https://github.com/oschwartz10612/poppler-windows/releases/")
    sys.exit(1)

# Chemins
BASE_DIR = Path(__file__).resolve().parent
PDF_PATH = BASE_DIR / "templates" / "logos likita.pdf"
OUTPUT_DIR = BASE_DIR / "static" / "images" / "logos"

# Créer le dossier de sortie
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Extraction des logos depuis: {PDF_PATH}")
print(f"Sauvegarde dans: {OUTPUT_DIR}")

try:
    # Convertir le PDF en images
    images = convert_from_path(str(PDF_PATH), dpi=300)
    
    print(f"\n{len(images)} page(s) trouvée(s) dans le PDF")
    
    # Sauvegarder chaque page comme image
    for i, image in enumerate(images, 1):
        # Sauvegarder en PNG haute qualité
        output_path = OUTPUT_DIR / f"logo_page_{i}.png"
        image.save(output_path, "PNG", quality=95)
        print(f"✓ Page {i} sauvegardée: {output_path.name}")
        
        # Essayer aussi de détecter et extraire les logos individuels
        # (cette partie peut nécessiter un traitement manuel)
    
    print(f"\n✅ Extraction terminée! {len(images)} image(s) sauvegardée(s)")
    print(f"📁 Dossier: {OUTPUT_DIR}")
    
except Exception as e:
    print(f"\n❌ Erreur lors de l'extraction: {e}")
    print("\nSi vous obtenez une erreur liée à poppler, veuillez:")
    print("1. Télécharger Poppler pour Windows depuis: https://github.com/oschwartz10612/poppler-windows/releases/")
    print("2. Extraire l'archive et ajouter le dossier 'bin' au PATH système")
    print("3. Ou installer via: pip install poppler-utils")
    sys.exit(1)



