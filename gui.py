import sys
import math
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QTextEdit, QFrame)
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QBrush

class ArcReactor(QWidget):
    """Composant visuel : Réacteur ARC animé avec effets néon."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0
        self.pulse = 0
        self.pulse_growing = True
        
        # Timer pour l'animation (60 FPS)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)

    def update_animation(self):
        self.angle = (self.angle + 2) % 360
        if self.pulse_growing:
            self.pulse += 0.5
            if self.pulse >= 15:
                self.pulse_growing = False
        else:
            self.pulse -= 0.5
            if self.pulse <= 0:
                self.pulse_growing = True
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center = QPointF(self.width() / 2, self.height() / 2)
        radius = min(self.width(), self.height()) / 3

        # Anneau externe
        pen = QPen(QColor(0, 229, 255, 180), 3)
        painter.setPen(pen)
        painter.drawEllipse(center, radius + self.pulse, radius + self.pulse)

        # Anneau interne pointillé tournant
        painter.save()
        painter.translate(center)
        painter.rotate(self.angle)
        pen_dash = QPen(QColor(0, 255, 204, 220), 2, Qt.PenStyle.DashLine)
        painter.setPen(pen_dash)
        painter.drawEllipse(QPointF(0, 0), radius - 15, radius - 15)
        painter.restore()

        # Cœur central lumineux
        glow = QBrush(QColor(0, 229, 255, 100))
        painter.setBrush(glow)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center, radius - 35, radius - 35)


class JarvisHUD(QMainWindow):
    """Fenêtre principale de l'interface utilisateur Jarvis."""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("JARVIS - Interface de Contrôle")
        self.resize(900, 600)
        
        # Style global (Thème sombre Cyberpunk / HUD Iron Man)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #080b12;
            }
            QLabel {
                color: #00e5ff;
                font-family: 'Consolas', 'Segoe UI', monospace;
            }
            QTextEdit {
                background-color: #0d131d;
                border: 1px solid #00e5ff;
                border-radius: 5px;
                color: #a0f0ff;
                font-family: 'Consolas', monospace;
                font-size: 13px;
            }
        """)

        # Disposition principale
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # --- Panneau Gauche (Réacteur + Statut) ---
        left_panel = QVBoxLayout()
        
        # Titre HUD
        title_label = QLabel("J.A.R.V.I.S.")
        title_label.setFont(QFont("Consolas", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_panel.addWidget(title_label)

        # Animation Réacteur ARC
        self.reactor = ArcReactor(self)
        self.reactor.setMinimumSize(300, 300)
        left_panel.addWidget(self.reactor)

        # Indicateur d'état du système
        self.status_label = QLabel("STATUT : EN VEILLE (Hey Jarvis)")
        self.status_label.setFont(QFont("Consolas", 11))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #00ffcc; border: 1px solid #00ffcc; padding: 6px; border-radius: 4px;")
        left_panel.addWidget(self.status_label)

        main_layout.addLayout(left_panel, stretch=1)

        # --- Panneau Droit (Journal des opérations) ---
        right_panel = QVBoxLayout()
        
        log_title = QLabel("JOURNAL DES SYSTÈMES & INTENTIONS")
        log_title.setFont(QFont("Consolas", 12, QFont.Weight.Bold))
        right_panel.addWidget(log_title)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.append("[SYSTEM] Initialisation des modules terminée.")
        self.log_box.append("[SYSTEM] Connexion réseau et outils OK.")
        right_panel.addWidget(self.log_box)

        main_layout.addLayout(right_panel, stretch=2)

    def update_status(self, text, color="#00e5ff"):
        """Permet de mettre à jour le statut affiché sur le HUD."""
        self.status_label.setText(f"STATUT : {text}")
        self.status_label.setStyleSheet(f"color: {color}; border: 1px solid {color}; padding: 6px; border-radius: 4px;")

    def add_log(self, sender, message):
        """Ajoute une ligne de log dans le journal."""
        self.log_box.append(f"[{sender}] {message}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JarvisHUD()
    window.show()
    sys.exit(app.exec())