import sys, math, json
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPainter, QPen, QBrush, QColor
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QFrame, QStackedWidget,
    QMessageBox, QFileDialog, QTextEdit, QScrollArea, QGroupBox, QFormLayout
)

APP_TITLE = "Footing Design Pro | IS 456"

class FootingCanvas(QWidget):
    """Schematic-only footing drawing; not to scale."""
    def __init__(self):
        super().__init__()
        self.kind = "Isolated Plan Footing"
        self.L = 2.5
        self.B = 2.5
        self.D = 0.6
        self.cx = 0.45
        self.cy = 0.45
        self.ecc = 0.25
        self.setMinimumHeight(260)
        self.setMinimumWidth(320)

    def update_model(self, kind, vals):
        self.kind = kind
        self.L = max(0.2, vals.get("L", 2.5))
        self.B = max(0.2, vals.get("B", 2.5))
        self.D = max(0.1, vals.get("D", 0.6))
        self.cx = max(0.1, vals.get("cx", 0.45))
        self.cy = max(0.1, vals.get("cy", 0.45))
        self.ecc = vals.get("ecc", 0.25)
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor("#FFFFFF"))
        p.setPen(QPen(QColor("#17365D"), 2))
        p.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        p.drawText(12, 22, self.kind.upper() + " — SCHEMATIC")
        area = self.rect().adjusted(24, 38, -24, -25)
        # Diagram is intentionally schematic, not dimensionally scaled.
        if "Combined" in self.kind:
            fw, fh = int(area.width()*0.82), int(area.height()*0.43)
            x, y = area.center().x()-fw//2, area.center().y()-fh//2
            p.setBrush(QBrush(QColor("#D9EAF7")))
            p.drawRect(x, y, fw, fh)
            p.setBrush(QBrush(QColor("#9FBAD2")))
            colw, colh = max(18, fw//12), max(18, fh//2)
            if "Eccentric" in self.kind:
                c1x, c2x = x+fw//5, x+fw*3//5
            else:
                c1x, c2x = x+fw//3, x+fw*2//3
            p.drawRect(c1x-colw//2, y+fh//2-colh//2, colw, colh)
            p.drawRect(c2x-colw//2, y+fh//2-colh//2, colw, colh)
            p.setPen(QPen(QColor("#17365D"), 1))
            p.drawText(c1x-10, y+fh//2+4, "C1")
            p.drawText(c2x-10, y+fh//2+4, "C2")
            p.setPen(QPen(QColor("#0F6B78"), 1))
            p.drawLine(x, y+fh+15, x+fw, y+fh+15)
            p.drawLine(x, y+fh+10, x, y+fh+20)
            p.drawLine(x+fw, y+fh+10, x+fw, y+fh+20)
            p.drawText(x+fw//2-25, y+fh+32, f"L = {self.L:.2f} m")
        else:
            fw, fh = int(area.width()*0.48), int(area.height()*0.48)
            x, y = area.center().x()-fw//2, area.center().y()-fh//2
            if self.kind == "Isolated Sloped Footing":
                p.setBrush(QBrush(QColor("#D9EAF7")))
                p.setPen(QPen(QColor("#17365D"), 2))
                p.drawPolygon([
                    __import__("PyQt6").QtCore.QPoint(x, y+fh),
                    __import__("PyQt6").QtCore.QPoint(x+fw, y+fh),
                    __import__("PyQt6").QtCore.QPoint(x+int(fw*.78), y+int(fh*.58)),
                    __import__("PyQt6").QtCore.QPoint(x+int(fw*.67), y+int(fh*.18)),
                    __import__("PyQt6").QtCore.QPoint(x+int(fw*.33), y+int(fh*.18)),
                    __import__("PyQt6").QtCore.QPoint(x+int(fw*.22), y+int(fh*.58)),
                ])
                p.setBrush(QBrush(QColor("#9FBAD2")))
                p.drawRect(x+int(fw*.4), y-int(fh*.15), int(fw*.2), int(fh*.42))
                p.setPen(QPen(QColor("#B45F06"), 2))
                p.drawLine(x+8, y+fh-8, x+fw-8, y+fh-8)
            else:
                p.setBrush(QBrush(QColor("#D9EAF7")))
                p.setPen(QPen(QColor("#17365D"), 2))
                p.drawRect(x, y, fw, fh)
                # plan-view column; eccentric case offsets column toward one edge
                p.setBrush(QBrush(QColor("#9FBAD2")))
                colw, colh = max(20, int(fw*.25)), max(20, int(fh*.25))
                if "Eccentric" in self.kind:
                    cx = x + max(colw//2+4, min(fw-colw//2-4, int(fw*.22 + (self.ecc/max(self.L, .1))*fw)))
                else:
                    cx = x+fw//2
                cy = y+fh//2
                p.drawRect(cx-colw//2, cy-colh//2, colw, colh)
                p.setPen(QPen(QColor("#B45F06"), 1))
                for i in range(1, 5):
                    yy = y + int(fh*i/5)
                    p.drawLine(x+5, yy, x+fw-5, yy)
                p.setPen(QPen(QColor("#0F6B78"), 1))
                p.drawLine(x, y+fh+15, x+fw, y+fh+15)
                p.drawLine(x, y+fh+10, x, y+fh+20)
                p.drawLine(x+fw, y+fh+10, x+fw, y+fh+20)
                p.drawText(x+fw//2-28, y+fh+32, f"L = {self.L:.2f} m")
                p.drawText(x+fw+8, y+fh//2, f"B={self.B:.2f} m")
        p.setPen(QPen(QColor("#667788"), 1))
        p.setFont(QFont("Arial", 8))
        p.drawText(12, self.height()-8, "Schematic only — not to scale; verify engineering design independently.")
        p.end()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.resize(1180, 780)
        self.setMinimumSize(980, 650)
        self.fields = {}
        self.result_box = None
        self.canvas = FootingCanvas()
        self._build_ui()
        self._load_defaults()
        self.update_diagram()

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(0,0,0,0)
        header = QFrame()
        header.setStyleSheet("background:#17365D;")
        hl = QHBoxLayout(header)
        title = QLabel("FOOTING DESIGN PRO")
        title.setStyleSheet("color:white;font-size:23px;font-weight:700;")
        subtitle = QLabel("Preliminary RC footing calculation workspace • Indian code basis")
        subtitle.setStyleSheet("color:#D9EAF7;font-size:11px;")
        left = QVBoxLayout(); left.addWidget(title); left.addWidget(subtitle)
        hl.addLayout(left); hl.addStretch()
        self.btn_open = QPushButton("Open Project")
        self.btn_save = QPushButton("Save Project")
        for b in (self.btn_open, self.btn_save):
            b.setStyleSheet("QPushButton{background:#FFFFFF;color:#17365D;padding:8px 14px;border-radius:5px;font-weight:600;} QPushButton:hover{background:#D9EAF7;}")
        hl.addWidget(self.btn_open); hl.addWidget(self.btn_save)
        outer.addWidget(header)

        body = QHBoxLayout()
        body.setContentsMargins(14,14,14,14)
        body.setSpacing(14)
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("background:#F3F7FB;border:1px solid #D6DEE8;border-radius:8px;")
        sl = QVBoxLayout(sidebar)
        sl.addWidget(QLabel("FOOTING TYPE"))
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Isolated Plan Footing",
            "Isolated Sloped Footing",
            "Isolated Eccentric Footing",
            "Combined Footing",
            "Combined Eccentric Footing"
        ])
        self.type_combo.setMinimumHeight(36)
        sl.addWidget(self.type_combo)
        sl.addSpacing(10)
        self.btn_calc = QPushButton("Calculate")
        self.btn_calc.setObjectName("primary")
        self.btn_calc.setMinimumHeight(42)
        self.btn_report = QPushButton("Export Report (.txt)")
        self.btn_report.setMinimumHeight(36)
        sl.addWidget(self.btn_calc); sl.addWidget(self.btn_report)
        sl.addSpacing(12)
        caution = QLabel("DESIGN STATUS\n\nThis first version performs preliminary area / bearing-pressure checks only. It is not a complete code design.")
        caution.setWordWrap(True)
        caution.setStyleSheet("color:#8A3B12;background:#FFF2CC;padding:10px;border-radius:5px;border:1px solid #E6C76A;")
        sl.addWidget(caution); sl.addStretch()
        body.addWidget(sidebar)

        center = QVBoxLayout()
        top = QHBoxLayout()
        self.input_group = QGroupBox("Project Inputs")
        self.input_layout = QGridLayout(self.input_group)
        self.input_layout.setHorizontalSpacing(12)
        self.input_layout.setVerticalSpacing(9)
        top.addWidget(self.input_group, 3)
        diag_group = QGroupBox("Footing Diagram")
        dg = QVBoxLayout(diag_group); dg.addWidget(self.canvas)
        top.addWidget(diag_group, 2)
        center.addLayout(top, 3)

        results_group = QGroupBox("Calculation Summary")
        rg = QVBoxLayout(results_group)
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setMinimumHeight(200)
        self.result_box.setPlaceholderText("Enter project values and click Calculate.")
        rg.addWidget(self.result_box)
        center.addWidget(results_group, 2)
        body.addLayout(center, 1)
        outer.addLayout(body)

        self.type_combo.currentTextChanged.connect(self._rebuild_inputs)
        self.btn_calc.clicked.connect(self.calculate)
        self.btn_report.clicked.connect(self.export_report)
        self.btn_save.clicked.connect(self.save_project)
        self.btn_open.clicked.connect(self.open_project)
        self._rebuild_inputs()

        self.setStyleSheet("""
            QWidget { font-family: 'Segoe UI'; font-size: 10pt; color:#243447; }
            QMainWindow { background:#EAF0F6; }
            QGroupBox { background:white; border:1px solid #C7D3E0; border-radius:7px; margin-top:10px; padding-top:10px; font-weight:700; }
            QGroupBox::title { subcontrol-origin:margin; left:12px; padding:0 5px; color:#17365D; }
            QLineEdit, QComboBox { background:#FFFFFF; border:1px solid #AEBCCC; border-radius:4px; padding:6px; min-width:80px; }
            QLineEdit:focus, QComboBox:focus { border:2px solid #0F6B78; }
            QPushButton { background:#E4ECF4; border:1px solid #C3D0DE; border-radius:5px; padding:7px; }
            QPushButton:hover { background:#D9EAF7; }
            QPushButton#primary { background:#0F6B78; color:white; border:none; font-weight:700; }
            QPushButton#primary:hover { background:#0B5964; }
            QTextEdit { background:#FBFCFE; border:1px solid #D6DEE8; border-radius:5px; padding:8px; font-family:Consolas; }
        """)

    def _field_definitions(self, kind):
        common = [
            ("Project name", "project", "Footing Project"),
            ("Column load P1 (kN)", "P1", "1000"),
            ("Moment Mx (kN·m)", "Mx", "0"),
            ("Moment My (kN·m)", "My", "0"),
            ("Footing length L (m)", "L", "2.5"),
            ("Footing width B (m)", "B", "2.5"),
            ("Overall depth D (m)", "D", "0.6"),
            ("Column size X (m)", "cx", "0.45"),
            ("Column size Y (m)", "cy", "0.45"),
            ("Allowable SBC (kN/m²)", "SBC", "200"),
            ("Concrete grade", "fck", "30"),
            ("Steel grade (MPa)", "fy", "500"),
            ("Footing self-weight factor", "swf", "1.1"),
        ]
        if "Combined" in kind:
            common[1] = ("Column 1 load P1 (kN)", "P1", "800")
            common.insert(2, ("Column 2 load P2 (kN)", "P2", "600"))
            common.insert(3, ("Column spacing (m)", "spacing", "3.0"))
            common.insert(4, ("Resultant offset e (m)", "ecc", "0.2"))
        elif "Eccentric" in kind:
            common.append(("Column eccentricity e (m)", "ecc", "0.25"))
        return common

    def _rebuild_inputs(self, *_):
        while self.input_layout.count():
            item = self.input_layout.takeAt(0)
            w = item.widget()
            if w: w.deleteLater()
        self.fields = {}
        kind = self.type_combo.currentText()
        defs = self._field_definitions(kind)
        for idx, (label, key, default) in enumerate(defs):
            lab = QLabel(label)
            edit = QLineEdit(default)
            edit.setMinimumWidth(110)
            self.fields[key] = edit
            row, col = divmod(idx, 2)
            self.input_layout.addWidget(lab, row, col*2)
            self.input_layout.addWidget(edit, row, col*2+1)
            edit.textChanged.connect(self.update_diagram)
        self.input_group.setMinimumHeight(330)
        self.update_diagram()

    def _load_defaults(self):
        pass

    def values(self):
        vals = {}
        for k, w in self.fields.items():
            if k == "project":
                vals[k] = w.text().strip() or "Footing Project"
            else:
                try:
                    vals[k] = float(w.text())
                except ValueError:
                    raise ValueError(f"'{k}' must be a numeric value.")
        return vals

    def update_diagram(self, *_):
        try:
            v = self.values()
        except Exception:
            v = {}
        self.canvas.update_model(self.type_combo.currentText(), v)

    def calculate(self):
        try:
            v = self.values()
            kind = self.type_combo.currentText()
            P1 = v.get("P1", 0)
            if P1 <= 0: raise ValueError("Column load P1 must be greater than zero.")
            L, B, D, SBC = v.get("L", 0), v.get("B", 0), v.get("D", 0), v.get("SBC", 0)
            if min(L, B, D, SBC) <= 0: raise ValueError("L, B, depth and SBC must be greater than zero.")
            area = L*B
            selfwt = area*D*25*max(0, v.get("swf", 1.1)-1.0)
            total = P1 + selfwt
            notes = []
            notes.append(f"PROJECT: {v.get('project','Footing Project')}")
            notes.append(f"FOOTING TYPE: {kind}")
            notes.append("-"*58)
            notes.append(f"Plan area = L × B = {L:.3f} × {B:.3f} = {area:.3f} m²")
            notes.append(f"Approx. footing self-weight allowance = {selfwt:.2f} kN")
            if "Combined" in kind:
                P2 = v.get("P2", 0)
                if P2 < 0: raise ValueError("P2 cannot be negative.")
                total = P1 + P2 + selfwt
                spacing = v.get("spacing", 0)
                ecc = v.get("ecc", 0)
                if spacing < 0: raise ValueError("Column spacing cannot be negative.")
                notes.append(f"Column loads total = P1 + P2 = {P1:.2f} + {P2:.2f} = {P1+P2:.2f} kN")
                notes.append(f"Column spacing = {spacing:.3f} m; entered resultant offset = {ecc:.3f} m")
                qavg = total/area
                notes.append(f"Average gross pressure (preliminary) = {total:.2f}/{area:.3f} = {qavg:.2f} kN/m²")
                notes.append("Combined footing pressure distribution and structural design are NOT fully calculated in this version.")
            elif "Eccentric" in kind:
                e = v.get("ecc", 0)
                if abs(e) >= L/2: raise ValueError("Absolute eccentricity must be less than L/2 for this simplified full-contact formula.")
                qavg = total/area
                qmax = qavg*(1+6*abs(e)/L)
                qmin = qavg*(1-6*abs(e)/L)
                notes.append(f"Entered eccentricity e = {e:.3f} m")
                notes.append(f"Average gross pressure = {qavg:.2f} kN/m²")
                notes.append(f"qmax = qavg × (1 + 6e/L) = {qmax:.2f} kN/m²")
                notes.append(f"qmin = qavg × (1 − 6e/L) = {qmin:.2f} kN/m²")
                if qmin < 0:
                    notes.append("WARNING: qmin < 0 indicates loss of full contact; this simplified equation is not valid for final design.")
                notes.append(f"SBC check on qmax: {'PASS' if qmax <= SBC else 'FAIL'} (SBC = {SBC:.2f} kN/m²)")
            else:
                qavg = total/area
                notes.append(f"Average gross pressure = total load / area = {total:.2f}/{area:.3f} = {qavg:.2f} kN/m²")
                notes.append(f"SBC check: {'PASS' if qavg <= SBC else 'FAIL'} (SBC = {SBC:.2f} kN/m²)")
                notes.append("Moment-based pressure variation is not included in this basic footing type check.")
            notes.append("")
            notes.append("DESIGN STATUS: PRELIMINARY CHECK ONLY")
            notes.append("Not included/verified here: complete flexure, one-way shear, punching shear, development length, dowels, settlement, sliding/overturning where applicable, and detailed reinforcement design.")
            notes.append("Use the relevant IS 456 / geotechnical design provisions and have the complete design independently checked before construction.")
            self.result_box.setPlainText("\n".join(notes))
        except Exception as e:
            QMessageBox.warning(self, "Input / Calculation Error", str(e))

    def project_data(self):
        return {"footing_type": self.type_combo.currentText(),
                "inputs": {k: w.text() for k,w in self.fields.items()},
                "last_results": self.result_box.toPlainText()}

    def save_project(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Footing Project", "footing_project.json", "Footing Project (*.json)")
        if not path: return
        try:
            Path(path).write_text(json.dumps(self.project_data(), indent=2), encoding="utf-8")
            QMessageBox.information(self, "Saved", f"Project saved:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))

    def open_project(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Footing Project", "", "Footing Project (*.json)")
        if not path: return
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            kind = data.get("footing_type", self.type_combo.currentText())
            idx = self.type_combo.findText(kind)
            if idx >= 0: self.type_combo.setCurrentIndex(idx)
            for k, val in data.get("inputs", {}).items():
                if k in self.fields: self.fields[k].setText(str(val))
            self.result_box.setPlainText(data.get("last_results", ""))
            self.update_diagram()
        except Exception as e:
            QMessageBox.critical(self, "Open Error", str(e))

    def export_report(self):
        if not self.result_box.toPlainText().strip():
            self.calculate()
        text = self.result_box.toPlainText()
        if not text.strip(): return
        path, _ = QFileDialog.getSaveFileName(self, "Export Calculation Summary", "footing_report.txt", "Text Report (*.txt)")
        if not path: return
        try:
            Path(path).write_text(text, encoding="utf-8")
            QMessageBox.information(self, "Exported", f"Report exported:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", str(e))


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_TITLE)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
