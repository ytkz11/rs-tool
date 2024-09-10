from resources.document_setting import Document_Form
from PyQt5.QtWidgets import QFrame


class DocumentWidget(QFrame,Document_Form):
    def __init__(self, text, parent=None):
        super(DocumentWidget, self).__init__(parent=parent)
        # self.unpack_ui = Document_Form()
        # self.unpack_ui.setupUi(self)
        self.setupUi(self)
        self.setObjectName(text.replace(' ', '-'))
