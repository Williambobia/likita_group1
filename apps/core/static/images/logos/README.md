# Logos LIKITA Group

Ce dossier contient les logos de LIKITA Group extraits du PDF.

## Instructions pour extraire les logos

### Option 1 - Extraction automatique (recommandé)

1. Installez PyMuPDF :
   ```bash
   pip install PyMuPDF
   ```

2. Exécutez le script d'extraction :
   ```bash
   python extract_logos_simple.py
   ```

3. Les logos seront extraits dans ce dossier avec les noms `logo_page_1.png`, `logo_page_2.png`, etc.

4. Renommez les fichiers selon leur usage :
   - `logo_principal.png` - Logo principal pour la navigation (hauteur recommandée: 50px)
   - `logo_footer.png` - Logo pour le footer (hauteur recommandée: 60px)
   - `logo_favicon.png` - Favicon (16x16, 32x32, ou 48x48 pixels)

### Option 2 - Extraction manuelle

1. Ouvrez le fichier `templates/logos likita.pdf`
2. Exportez chaque logo en PNG avec fond transparent
3. Placez les fichiers dans ce dossier avec les noms ci-dessus

## Formats recommandés

- **PNG** avec fond transparent pour les logos
- **SVG** pour une meilleure qualité (si disponible)
- **ICO** ou **PNG** pour le favicon

## Tailles recommandées

- Logo navigation : 150-200px de largeur, hauteur proportionnelle
- Logo footer : 100-150px de largeur, hauteur proportionnelle  
- Favicon : 16x16, 32x32, ou 48x48 pixels

## Utilisation dans le site

Les logos sont automatiquement intégrés dans :
- **Navigation** : `logo_principal.png`
- **Footer** : `logo_footer.png`
- **Favicon** : `logo_favicon.png`

Si un logo n'existe pas, le texte "LIKITA Group" s'affichera à la place.
