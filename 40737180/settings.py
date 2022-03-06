from typing import Optional
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QDialog,
    QCheckBox,
    QSlider,
    QComboBox,
    QWidget,
    QDialogButtonBox,
    QColorDialog,
    QPushButton,
)
from .gui.forms.anki21.settings import Ui_Settings
from .markets import markets


class QColorButton(QPushButton):
    def __init__(self, parent: QWidget = None, color: str = "#000000"):
        super().__init__(parent=parent)
        self._setButtonColor(color)
        self.clicked.connect(self._chooseColor)

    def color(self) -> str:
        """Get current color

        :return: HTML color code
        :rtype: str
        """
        return self._color

    def setColor(self, color: str):
        """Set current color

        :param color: HTML color code
        :type color: str
        """
        self._setButtonColor(color)

    def _chooseColor(self) -> Optional[bool]:
        dialog = QColorDialog(parent=self)
        color = dialog.getColor(QColor(self._color))
        if not color.isValid():
            return False
        self._setButtonColor(color.name())

    def _setButtonColor(self, color: str):
        """Set preview color"""
        pixmap = QPixmap(128, 18)
        qcolor = QColor(0, 0, 0)
        qcolor.setNamedColor(color)
        pixmap.fill(qcolor)
        self.setIcon(QIcon(pixmap))
        self.setIconSize(QSize(128, 18))
        self._color = color

class SettingsDialog(QDialog):

    def __init__(self, config, parent: QWidget):
        super().__init__(parent=parent)
        self._config = config
        self._mw = parent
        self._form = Ui_Settings()
        self._form.setupUi(self)
        # connect restore defaults button to function
        self._form.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(
            self.restoreDefaults
        )
        # setup color picker
        self.setupColorPicker()

    def restoreDefaults(self):
        self._config['underlineColor'] = '#00B6FF'
        self._config['whenPopupConflictsShowLogo'] = True
        self._config['logoOpacity'] = 0.8
        self._config['marketId'] = 100
        self.writeConfig()
        self.loadConfig()

    def loadConfig(self):
        show_eye: QCheckBox = getattr(self._form, 'whenPopupConflictsShowLogo')
        show_eye.setChecked(self._config['whenPopupConflictsShowLogo'])

        u_color: QColorButton = getattr(self._form, 'underlineColor')
        u_color.setColor(self._config['underlineColor'])

        eye_opacity: QSlider = getattr(self._form, 'logoOpacity')
        eye_opacity.setValue(self._config['logoOpacity'] * 10)

        market_selector: QComboBox = getattr(self._form, 'marketId')

        if market_selector.count() < 1:
            for market in markets:
                market_selector.addItem(market['name'])

        i = 0
        for market in markets:
            if self._config['marketId'] == market['id']:
                market_selector.setCurrentIndex(i)
            i += 1

    def saveConfig(self):
        show_eye: QCheckBox = getattr(self._form, 'whenPopupConflictsShowLogo')
        self._config['whenPopupConflictsShowLogo'] = show_eye.isChecked()

        u_color: QColorButton = getattr(self._form, 'underlineColor')
        self._config['underlineColor'] = u_color.color()

        eye_opacity: QSlider = getattr(self._form, 'logoOpacity')
        self._config['logoOpacity'] = eye_opacity.value() / 10

        market_selector: QComboBox = getattr(self._form, 'marketId')
        selectedMarket = market_selector.currentText()

        for market in markets:
            if market['name'] == selectedMarket:
                self._config['marketId'] = market['id']

        self.writeConfig()

    def writeConfig(self):
        self._mw.addonManager.writeConfig(__name__, self._config)

    def setupColorPicker(self):
        self._form.underlineColor = QColorButton(self)
        self._form.underlineColorContainer.addWidget(
            self._form.underlineColor
        )

    def accept(self):
        self.saveConfig()
        super().accept()

    def show(self):
        self.loadConfig()
        self.exec_()
