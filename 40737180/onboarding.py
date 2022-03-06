from PyQt5.QtWidgets import (
    QDialog,
    QComboBox,
    QWidget,
)
from .gui.forms.anki21.onboarding import Ui_Onboarding
from .markets import markets

class OnboardingDialog(QDialog):

    def __init__(self, config, parent: QWidget):
        super().__init__(parent=parent)
        self._config = config
        self._mw = parent
        self._form = Ui_Onboarding()
        self._form.setupUi(self)


    def loadConfig(self):
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
        market_selector: QComboBox = getattr(self._form, 'marketId')
        selectedMarket = market_selector.currentText()

        for market in markets:
            if market['name'] == selectedMarket:
                self._config['marketId'] = market['id']

        self._config['onboardingSeen'] = 1

        self.writeConfig()

    def writeConfig(self):
        self._mw.addonManager.writeConfig(__name__, self._config)

    def accept(self):
        self.saveConfig()
        super().accept()

    def show(self):
        self.loadConfig()
        self.exec_()
