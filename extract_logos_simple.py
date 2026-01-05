"""
Script simple pour extraire les logos du PDF LIKITA
Utilise PyMuPDF (fitz) qui est plus simple à installer
"""
import sys
import os
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("=" * 60)
    print("Installation de PyMuPDF...")
    print("Exécutez: pip install PyMuPDF")
    print("=" * 60)
    sys.exit(1)

# Chemins
BASE_DIR = Path(__file__).resolve().parent
PDF_PATH = BASE_DIR / "templates" / "logos likita.pdf"
OUTPUT_DIR = BASE_DIR / "static" / "images" / "logos"

# Créer le dossier de sortie
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not PDF_PATH.exists():
    print(f"❌ Fichier PDF non trouvé: {PDF_PATH}")
    sys.exit(1)

print(f"📄 Extraction des logos depuis: {PDF_PATH.name}")
print(f"📁 Sauvegarde dans: {OUTPUT_DIR}\n")

try:
    # Ouvrir le PDF
    pdf_document = fitz.open(str(PDF_PATH))
    
    print(f"✅ PDF ouvert: {len(pdf_document)} page(s) trouvée(s)\n")
    
    # Extraire chaque page comme image
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        
        # Rendre la page en image (300 DPI pour haute qualité)
        mat = fitz.Matrix(300/72, 300/72)  # 300 DPI
        pix = page.get_pixmap(matrix=mat)
        
        # Sauvegarder
        output_path = OUTPUT_DIR / f"logo_page_{page_num + 1}.png"
        pix.save(str(output_path))
        
        print(f"✓ Page {page_num + 1} extraite: {output_path.name} ({pix.width}x{pix.height}px)")
    
    pdf_document.close()
    
    print(f"\n{'=' * 60}")
    print(f"✅ Extraction terminée!")
    print(f"📁 {len(pdf_document)} image(s) sauvegardée(s) dans: {OUTPUT_DIR}")
    print(f"\n📝 Prochaines étapes:")
    print(f"   1. Ouvrez le dossier: {OUTPUT_DIR}")
    print(f"   2. Renommez les fichiers selon leur usage:")
    print(f"      - logo_principal.png (pour la navigation)")
    print(f"      - logo_footer.png (pour le footer)")
    print(f"      - logo_favicon.png (16x16 ou 32x32 pour le favicon)")
    print(f"   3. Si nécessaire, recadrez les logos avec un éditeur d'image")
    print(f"{'=' * 60}")
    
except Exception as e:
    print(f"\n❌ Erreur lors de l'extraction: {e}")
    print(f"\n💡 Solution: Installez PyMuPDF avec: pip install PyMuPDF")
    sys.exit(1)

