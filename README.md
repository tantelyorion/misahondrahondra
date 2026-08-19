# 🇲🇬 Misahondrahondra

> A harmless Malagasy Windows prank that makes your desktop windows twerk to the Misahondrahondra beat for up to 6 minutes. 💃🪟

Inspiré de la tendance virale **Misahondrahondra** sur les réseaux sociaux, ce petit programme transforme ton bureau Windows en piste de danse. Aucune donnée n'est touchée : c'est du visuel pur, 100% réversible.

## ✨ Ce que ça fait

1. Lance `Misahondrahondra.exe`
2. Une bannière `MISAHONDRAHONDRA ACTIVATED 😂` s'affiche
3. La musique `misahondrahondra.mp3` démarre
4. Toutes les fenêtres ouvertes se mettent à bouger/twerker en rythme, chacune avec un mouvement légèrement différent
5. Ça dure la durée de la musique (≈ 3 min 39, plafonné à 6 min max)
6. Toutes les fenêtres reviennent **exactement** à leur position d'origine
7. Le programme se ferme tout seul

**ESC** à tout moment = arrêt immédiat + restauration des fenêtres.

## 🛡️ Ce que ça ne fait PAS

- ❌ Pas de suppression de fichiers
- ❌ Pas de chiffrement
- ❌ Pas de modification du registre
- ❌ Pas d'installation cachée ni de persistance
- ❌ Pas de collecte de données
- ❌ Pas de connexion réseau requise
- ❌ Pas de modification permanente de Windows

C'est un **prankware assumé**, pas un virus. Le repo le dit clairement pour éviter toute confusion (antivirus, utilisateurs, etc.).

## 🚀 Installation & usage

```bash
pip install -r requirements.txt
python misahondrahondra.py
```

Place `misahondrahondra.mp3` dans le même dossier que le script (ou l'exe).

## 📦 Générer le .exe

Sur Windows :

```bash
build_exe.bat
```

Ça utilise PyInstaller pour produire `dist\Misahondrahondra.exe`.

## ⚙️ Technique

- **Détection des fenêtres** : `win32gui.EnumWindows`, en excluant la barre des tâches, le bureau, et les fenêtres système
- **Animation** : chaque fenêtre a un profil de danse aléatoire (phase, vitesse, amplitude) basé sur des sinusoïdes, pour un effet "bureau qui twerke" non synchronisé de façon robotique
- **Musique** : API Windows MCI (`winmm.dll` via `ctypes`, intégrée à Windows — aucune dépendance externe), durée détectée automatiquement pour caler l'animation
- **Arrêt d'urgence** : `GetAsyncKeyState(VK_ESCAPE)` vérifié à chaque frame
- **Sécurité** : `try/finally` garantit la restauration des positions même en cas d'erreur ou d'interruption

## 🎬 Idée de pitch

> *"Quand Misahondrahondra quitte TikTok et arrive directement sur ton Windows."*

## Licence

À toi de choisir (MIT recommandé pour un projet meme open-source).
