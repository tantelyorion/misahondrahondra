"""
Misahondrahondra.exe
=====================
Prankware humoristique malgache (100% inoffensif).

Ce script :
  - fait "danser" les fenêtres ouvertes du bureau Windows (twerk visuel)
  - joue la musique misahondrahondra.mp3 en fond
  - restaure TOUJOURS les positions originales des fenêtres à la fin
  - peut être interrompu à tout moment avec la touche ESC

Aucun fichier n'est supprimé, chiffré ou modifié. Aucune persistance,
aucune modification du registre, aucune collecte de données, aucune
connexion réseau requise.

Nécessite Windows + Python 3.9+  (voir requirements.txt)
"""

import math
import os
import random
import sys
import time
import tkinter as tk

try:
    import win32gui
    import win32con
    import win32api
except ImportError:
    print("Ce script nécessite pywin32 : pip install pywin32")
    sys.exit(1)

try:
    import pygame
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False


# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

MAX_DURATION_SEC = 6 * 60          # plafond absolu demandé (6 min)
MUSIC_FILENAME = "misahondrahondra.mp3"
FPS = 30
FRAME_DELAY = 1.0 / FPS

# Classes de fenêtres système à ne JAMAIS toucher (barre des tâches, bureau...)
IGNORED_CLASSES = {
    "Shell_TrayWnd",      # barre des tâches
    "Progman",             # bureau
    "WorkerW",              # bureau (calques)
    "Shell_SecondaryTrayWnd",
    "Windows.UI.Core.CoreWindow",
    "Xaml_WindowedPopupClass",
}


# --------------------------------------------------------------------------
# Détection des fenêtres
# --------------------------------------------------------------------------

def list_dancer_windows(own_hwnds):
    """Retourne {hwnd: (x, y, w, h)} pour les fenêtres visibles à faire danser."""
    windows = {}

    def callback(hwnd, _):
        if hwnd in own_hwnds:
            return True
        if not win32gui.IsWindowVisible(hwnd):
            return True
        if win32gui.GetParent(hwnd) != 0:
            return True
        title = win32gui.GetWindowText(hwnd)
        if not title.strip():
            return True
        cls = win32gui.GetClassName(hwnd)
        if cls in IGNORED_CLASSES:
            return True
        try:
            rect = win32gui.GetWindowRect(hwnd)
        except Exception:
            return True
        x, y, right, bottom = rect
        w, h = right - x, bottom - y
        if w <= 0 or h <= 0:
            return True
        # Ignore les fenêtres minimisées (position hors écran typique -32000)
        if x <= -30000 or y <= -30000:
            return True
        windows[hwnd] = (x, y, w, h)
        return True

    win32gui.EnumWindows(callback, None)
    return windows


# --------------------------------------------------------------------------
# Interface "MISAHONDRAHONDRA ACTIVATED"
# --------------------------------------------------------------------------

def show_activation_banner(duration_ms=2500):
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    try:
        root.attributes("-alpha", 0.95)
    except tk.TclError:
        pass

    w, h = 520, 140
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")
    root.configure(bg="#0b0b0f")

    label1 = tk.Label(
        root, text="🇲🇬 MISAHONDRAHONDRA ACTIVATED 😂",
        font=("Segoe UI", 18, "bold"), fg="#ff2e63", bg="#0b0b0f"
    )
    label1.pack(pady=(20, 5))

    label2 = tk.Label(
        root, text="Ton bureau va twerker... ESC pour arrêter à tout moment.",
        font=("Segoe UI", 10), fg="#eaeaea", bg="#0b0b0f"
    )
    label2.pack()

    root.after(duration_ms, root.destroy)
    root.mainloop()


# --------------------------------------------------------------------------
# Audio
# --------------------------------------------------------------------------

def start_music_and_get_duration(base_dir):
    """Lance la musique si dispo, retourne la durée en secondes (ou None)."""
    if not HAS_PYGAME:
        print("pygame absent : le prank continuera SANS musique.")
        return None

    music_path = os.path.join(base_dir, MUSIC_FILENAME)
    if not os.path.isfile(music_path):
        print(f"'{MUSIC_FILENAME}' introuvable à côté du programme : pas de musique.")
        return None

    try:
        pygame.mixer.init()
        sound = pygame.mixer.Sound(music_path)
        duration = sound.get_length()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()
        return duration
    except Exception as e:
        print(f"Impossible de lire la musique ({e}). Le prank continue sans son.")
        return None


def stop_music():
    if HAS_PYGAME and pygame.mixer.get_init():
        pygame.mixer.music.stop()


# --------------------------------------------------------------------------
# Animation "twerk"
# --------------------------------------------------------------------------

class DanceProfile:
    """Paramètres de mouvement propres à chaque fenêtre, pour un effet varié."""

    def __init__(self):
        self.phase_x = random.uniform(0, math.tau)
        self.phase_y = random.uniform(0, math.tau)
        self.speed_x = random.uniform(2.2, 3.4)   # rad/s
        self.speed_y = random.uniform(4.0, 6.0)   # deux fois plus vite -> twerk
        self.amp_x_ratio = random.uniform(0.03, 0.07)   # % de la largeur écran
        self.amp_y_ratio = random.uniform(0.015, 0.035)  # % de la hauteur écran


def is_escape_pressed():
    # 0x8000 = touche actuellement enfoncée (GetAsyncKeyState)
    return bool(win32api.GetAsyncKeyState(win32con.VK_ESCAPE) & 0x8000)


def dance_loop(windows, duration_sec, own_hwnds):
    sw = win32api.GetSystemMetrics(0)
    sh = win32api.GetSystemMetrics(1)

    profiles = {hwnd: DanceProfile() for hwnd in windows}
    start = time.time()

    print(f"💃 {len(windows)} fenêtre(s) en train de twerker pendant {duration_sec:.0f}s "
          f"(ESC pour arrêter)...")

    try:
        while True:
            elapsed = time.time() - start
            if elapsed >= duration_sec:
                break
            if is_escape_pressed():
                print("ESC détecté : arrêt du prank.")
                break

            for hwnd, (ox, oy, w, h) in windows.items():
                if not win32gui.IsWindow(hwnd):
                    continue
                p = profiles[hwnd]
                dx = math.sin(elapsed * p.speed_x + p.phase_x) * sw * p.amp_x_ratio
                dy = abs(math.sin(elapsed * p.speed_y + p.phase_y)) * sh * p.amp_y_ratio
                nx = int(ox + dx)
                ny = int(oy + dy)
                try:
                    win32gui.SetWindowPos(
                        hwnd, 0, nx, ny, w, h,
                        win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE
                    )
                except Exception:
                    pass  # fenêtre fermée entre-temps, on ignore

            time.sleep(FRAME_DELAY)
    except KeyboardInterrupt:
        print("Interruption clavier : arrêt du prank.")


def restore_windows(windows):
    print("🔄 Restauration des positions originales...")
    for hwnd, (x, y, w, h) in windows.items():
        if not win32gui.IsWindow(hwnd):
            continue
        try:
            win32gui.SetWindowPos(
                hwnd, 0, x, y, w, h,
                win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE
            )
        except Exception:
            pass


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main():
    if os.name != "nt":
        print("Misahondrahondra ne fonctionne que sous Windows.")
        sys.exit(1)

    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    # Bannière d'activation (bloquante ~2.5s, humoristique)
    show_activation_banner()

    # On note nos propres handles pour ne pas se faire danser soi-même
    own_hwnds = set()

    def collect_own(hwnd, _):
        title = win32gui.GetWindowText(hwnd)
        if "MISAHONDRAHONDRA" in title.upper() or "PYTHON" in title.upper():
            own_hwnds.add(hwnd)
        return True

    win32gui.EnumWindows(collect_own, None)

    windows = list_dancer_windows(own_hwnds)
    if not windows:
        print("Aucune fenêtre à faire danser (bureau trop vide 😅).")
        return

    duration = start_music_and_get_duration(base_dir)
    if duration is None:
        duration = 60  # fallback si pas de musique : 1 minute
    duration = min(duration, MAX_DURATION_SEC)

    try:
        dance_loop(windows, duration, own_hwnds)
    finally:
        stop_music()
        restore_windows(windows)
        print("✅ Misahondrahondra terminé proprement. Misaotra! 🇲🇬")


if __name__ == "__main__":
    main()
