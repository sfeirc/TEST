"""
Script de nettoyage des fichiers temporaires
Gère automatiquement les fichiers HTML/PPTX anciens dans generated_files/
"""

import os
import time
from datetime import datetime, timedelta
from pathlib import Path


def cleanup_old_files(
    directory: str = "generated_files",
    max_age_hours: int = 24,
    dry_run: bool = False
) -> dict:
    """
    Nettoie les fichiers temporaires anciens
    
    Args:
        directory: Répertoire à nettoyer
        max_age_hours: Âge maximum des fichiers en heures
        dry_run: Si True, liste les fichiers sans les supprimer
    
    Returns:
        Dict avec statistiques de nettoyage
    """
    
    if not os.path.exists(directory):
        return {
            "status": "skipped",
            "reason": f"Répertoire {directory} n'existe pas",
            "files_deleted": 0,
            "space_freed_mb": 0
        }
    
    now = time.time()
    max_age_seconds = max_age_hours * 3600
    cutoff_time = now - max_age_seconds
    
    files_to_delete = []
    total_size = 0
    
    # Parcourir tous les fichiers
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            
            try:
                file_stats = os.stat(file_path)
                file_age = file_stats.st_mtime
                
                if file_age < cutoff_time:
                    files_to_delete.append({
                        "path": file_path,
                        "age_hours": (now - file_age) / 3600,
                        "size_bytes": file_stats.st_size
                    })
                    total_size += file_stats.st_size
            except Exception as e:
                print(f"⚠️ Erreur lors de l'analyse de {file_path}: {e}")
    
    # Afficher les fichiers trouvés
    print(f"\n🔍 Recherche dans: {directory}")
    print(f"📅 Fichiers plus vieux que: {max_age_hours}h")
    print(f"📊 {len(files_to_delete)} fichier(s) trouvé(s)")
    print(f"💾 Espace total: {total_size / (1024*1024):.2f} MB")
    
    if dry_run:
        print("\n⚠️ MODE DRY-RUN - Aucun fichier supprimé")
        print("\nFichiers qui seraient supprimés:")
        for file_info in files_to_delete:
            print(f"  - {file_info['path']} ({file_info['age_hours']:.1f}h, {file_info['size_bytes']/1024:.1f} KB)")
        
        return {
            "status": "dry_run",
            "files_found": len(files_to_delete),
            "space_would_be_freed_mb": total_size / (1024*1024),
            "files": files_to_delete
        }
    
    # Supprimer les fichiers
    files_deleted = 0
    space_freed = 0
    errors = []
    
    print("\n🗑️ Suppression en cours...")
    for file_info in files_to_delete:
        try:
            os.remove(file_info['path'])
            files_deleted += 1
            space_freed += file_info['size_bytes']
            print(f"  ✅ Supprimé: {file_info['path']}")
        except Exception as e:
            errors.append(f"{file_info['path']}: {str(e)}")
            print(f"  ❌ Erreur: {file_info['path']} - {e}")
    
    print(f"\n✅ Nettoyage terminé!")
    print(f"📊 {files_deleted} fichier(s) supprimé(s)")
    print(f"💾 {space_freed / (1024*1024):.2f} MB libéré(s)")
    
    if errors:
        print(f"\n⚠️ {len(errors)} erreur(s):")
        for error in errors:
            print(f"  - {error}")
    
    return {
        "status": "success",
        "files_deleted": files_deleted,
        "space_freed_mb": space_freed / (1024*1024),
        "errors": errors
    }


def cleanup_by_pattern(
    directory: str = "generated_files",
    pattern: str = "*.html",
    max_age_hours: int = 1,
    dry_run: bool = False
) -> dict:
    """
    Nettoie les fichiers correspondant à un pattern spécifique
    
    Args:
        directory: Répertoire à nettoyer
        pattern: Pattern de fichiers (ex: "*.html", "presentation_*.pptx")
        max_age_hours: Âge maximum en heures
        dry_run: Mode simulation
    
    Returns:
        Dict avec statistiques
    """
    
    if not os.path.exists(directory):
        return {
            "status": "skipped",
            "reason": f"Répertoire {directory} n'existe pas"
        }
    
    path = Path(directory)
    now = time.time()
    cutoff_time = now - (max_age_hours * 3600)
    
    files_to_delete = []
    total_size = 0
    
    # Rechercher les fichiers correspondant au pattern
    for file_path in path.glob(pattern):
        if file_path.is_file():
            file_stats = file_path.stat()
            
            if file_stats.st_mtime < cutoff_time:
                files_to_delete.append({
                    "path": str(file_path),
                    "age_hours": (now - file_stats.st_mtime) / 3600,
                    "size_bytes": file_stats.st_size
                })
                total_size += file_stats.st_size
    
    print(f"\n🔍 Pattern: {pattern}")
    print(f"📊 {len(files_to_delete)} fichier(s) trouvé(s)")
    
    if dry_run:
        print("⚠️ MODE DRY-RUN - Simulation")
        for file_info in files_to_delete:
            print(f"  - {file_info['path']}")
        return {
            "status": "dry_run",
            "files_found": len(files_to_delete),
            "pattern": pattern
        }
    
    # Supprimer
    for file_info in files_to_delete:
        try:
            os.remove(file_info['path'])
            print(f"  ✅ {file_info['path']}")
        except Exception as e:
            print(f"  ❌ {file_info['path']}: {e}")
    
    return {
        "status": "success",
        "files_deleted": len(files_to_delete),
        "space_freed_mb": total_size / (1024*1024)
    }


if __name__ == "__main__":
    import sys
    
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║     🧹 NETTOYAGE FICHIERS TEMPORAIRES INFOTEL AI AGENTS     ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    
    # Mode interactif
    if len(sys.argv) > 1:
        if sys.argv[1] == "--dry-run":
            print("\n🔍 Mode DRY-RUN (simulation)")
            result = cleanup_old_files(dry_run=True)
        elif sys.argv[1] == "--html-only":
            print("\n🔍 Nettoyage HTML uniquement")
            result = cleanup_by_pattern(pattern="*.html", max_age_hours=1)
        elif sys.argv[1] == "--force":
            print("\n⚠️ Nettoyage forcé (tous fichiers >24h)")
            result = cleanup_old_files(max_age_hours=24)
        else:
            print("\n❌ Option inconnue")
            print("\nUsage:")
            print("  python cleanup_temp_files.py              # Nettoyage normal")
            print("  python cleanup_temp_files.py --dry-run    # Simulation")
            print("  python cleanup_temp_files.py --html-only  # HTML seulement")
            print("  python cleanup_temp_files.py --force      # Forcé")
            sys.exit(1)
    else:
        # Nettoyage normal
        print("\n🧹 Nettoyage automatique (fichiers >24h)")
        print("Appuyez sur Ctrl+C pour annuler...")
        time.sleep(2)
        result = cleanup_old_files(max_age_hours=24)
    
    print("\n" + "="*60)
    print(f"Status: {result.get('status')}")
    print("="*60)

