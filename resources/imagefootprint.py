# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
from qfluentwidgets import IndeterminateProgressBar

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(804, 609)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.CardWidget = CardWidget(Form)
        self.CardWidget.setObjectName("CardWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.CardWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(self.CardWidget)
        self.frame.setMinimumSize(QtCore.QSize(0, 40))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.TitleLabel_3 = TitleLabel(self.frame)
        self.TitleLabel_3.setAlignment(QtCore.Qt.AlignCenter)
        self.TitleLabel_3.setObjectName("TitleLabel_3")
        self.verticalLayout_3.addWidget(self.TitleLabel_3)
        self.verticalLayout_2.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.CardWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(-1, 10, 0, -1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.imagefootprint_prompt = PushButton(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.imagefootprint_prompt.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/message.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.imagefootprint_prompt.setIcon(icon)
        self.imagefootprint_prompt.setIconSize(QtCore.QSize(20, 20))
        self.imagefootprint_prompt.setObjectName("imagefootprint_prompt")
        self.verticalLayout_5.addWidget(self.imagefootprint_prompt)
        spacerItem = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(10, 20, 10, 10)
        self.verticalLayout_4.setSpacing(15)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.imagefootprint_filepath_line = LineEdit(self.frame_2)
        self.imagefootprint_filepath_line.setMinimumSize(QtCore.QSize(500, 40))
        self.imagefootprint_filepath_line.setObjectName("imagefootprint_filepath_line")
        self.horizontalLayout.addWidget(self.imagefootprint_filepath_line)
        self.imagefootprint_filepath_btn = PrimaryPushButton(self.frame_2)
        self.imagefootprint_filepath_btn.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.imagefootprint_filepath_btn.setFont(font)
        self.imagefootprint_filepath_btn.setStyleSheet("PushButton, ToolButton, ToggleButton, ToggleToolButton {\n"
"    color: black;\n"
"    background: rgba(255, 255, 255, 0.7);\n"
"    border: 1px solid rgba(0, 0, 0, 0.073);\n"
"    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
"    border-radius: 20px;\n"
"    /* font: 14px \'Segoe UI\', \'Microsoft YaHei\'; */\n"
"    padding: 5px 12px 6px 12px;\n"
"    outline: none;\n"
"}\n"
"\n"
"ToolButton {\n"
"    padding: 5px 9px 6px 8px;\n"
"}\n"
"\n"
"PushButton[hasIcon=false] {\n"
"    padding: 5px 12px 6px 12px;\n"
"}\n"
"\n"
"PushButton[hasIcon=true] {\n"
"    padding: 5px 12px 6px 36px;\n"
"}\n"
"\n"
"DropDownToolButton, PrimaryDropDownToolButton {\n"
"    padding: 5px 31px 6px 8px;\n"
"}\n"
"\n"
"DropDownPushButton[hasIcon=false],\n"
"PrimaryDropDownPushButton[hasIcon=false] {\n"
"    padding: 5px 31px 6px 12px;\n"
"}\n"
"\n"
"DropDownPushButton[hasIcon=true],\n"
"PrimaryDropDownPushButton[hasIcon=true] {\n"
"    padding: 5px 31px 6px 36px;\n"
"}\n"
"\n"
"PushButton:hover, ToolButton:hover, ToggleButton:hover, ToggleToolButton:hover {\n"
"    background: rgba(249, 249, 249, 0.5);\n"
"}\n"
"\n"
"PushButton:pressed, ToolButton:pressed, ToggleButton:pressed, ToggleToolButton:pressed {\n"
"    color: rgba(0, 0, 0, 0.63);\n"
"    background: rgba(249, 249, 249, 0.3);\n"
"    border-bottom: 1px solid rgba(0, 0, 0, 0.073);\n"
"}\n"
"\n"
"PushButton:disabled, ToolButton:disabled, ToggleButton:disabled, ToggleToolButton:disabled {\n"
"    color: rgba(0, 0, 0, 0.36);\n"
"    background: rgba(249, 249, 249, 0.3);\n"
"    border: 1px solid rgba(0, 0, 0, 0.06);\n"
"    border-bottom: 1px solid rgba(0, 0, 0, 0.06);\n"
"}\n"
"\n"
"\n"
"PrimaryPushButton,\n"
"PrimaryToolButton,\n"
"ToggleButton:checked,\n"
"ToggleToolButton:checked {\n"
"    color: white;\n"
"    background-color: #009faa;\n"
"    border: 1px solid #00a7b3;\n"
"    border-bottom: 1px solid #007780;\n"
"}\n"
"\n"
"PrimaryPushButton:hover,\n"
"PrimaryToolButton:hover,\n"
"ToggleButton:checked:hover,\n"
"ToggleToolButton:checked:hover {\n"
"    background-color: #00a7b3;\n"
"    border: 1px solid #2daab3;\n"
"    border-bottom: 1px solid #007780;\n"
"}\n"
"\n"
"PrimaryPushButton:pressed,\n"
"PrimaryToolButton:pressed,\n"
"ToggleButton:checked:pressed,\n"
"ToggleToolButton:checked:pressed {\n"
"    color: rgba(255, 255, 255, 0.63);\n"
"    background-color: #3eabb3;\n"
"    border: 1px solid #3eabb3;\n"
"}\n"
"\n"
"PrimaryPushButton:disabled,\n"
"PrimaryToolButton:disabled,\n"
"ToggleButton:checked:disabled,\n"
"ToggleToolButton:checked:disabled {\n"
"    color: rgba(255, 255, 255, 0.9);\n"
"    background-color: rgb(205, 205, 205);\n"
"    border: 1px solid rgb(205, 205, 205);\n"
"}\n"
"\n"
"SplitDropButton,\n"
"PrimarySplitDropButton {\n"
"    border-left: none;\n"
"    border-top-left-radius: 0;\n"
"    border-bottom-left-radius: 0;\n"
"}\n"
"\n"
"#splitPushButton,\n"
"#splitToolButton,\n"
"#primarySplitPushButton,\n"
"#primarySplitToolButton {\n"
"    border-top-right-radius: 0;\n"
"    border-bottom-right-radius: 0;\n"
"}\n"
"\n"
"#splitPushButton:pressed,\n"
"#splitToolButton:pressed,\n"
"SplitDropButton:pressed {\n"
"    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
"}\n"
"\n"
"PrimarySplitDropButton:pressed {\n"
"    border-bottom: 1px solid #007780;\n"
"}\n"
"\n"
"#primarySplitPushButton, #primarySplitToolButton {\n"
"    border-right: 1px solid #3eabb3;\n"
"}\n"
"\n"
"#primarySplitPushButton:pressed, #primarySplitToolButton:pressed {\n"
"    border-bottom: 1px solid #007780;\n"
"}\n"
"\n"
"HyperlinkButton {\n"
"    /* font: 14px \'Segoe UI\', \'Microsoft YaHei\'; */\n"
"    padding: 6px 12px 6px 12px;\n"
"    color: #009faa;\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"HyperlinkButton[hasIcon=false] {\n"
"    padding: 6px 12px 6px 12px;\n"
"}\n"
"\n"
"HyperlinkButton[hasIcon=true] {\n"
"    padding: 6px 12px 6px 36px;\n"
"}\n"
"\n"
"HyperlinkButton:hover {\n"
"    color: #009faa;\n"
"    background-color: rgba(0, 0, 0, 10);\n"
"    border: none;\n"
"}\n"
"\n"
"HyperlinkButton:pressed {\n"
"    color: #009faa;\n"
"    background-color: rgba(0, 0, 0, 6);\n"
"    border: none;\n"
"}\n"
"\n"
"HyperlinkButton:disabled {\n"
"    color: rgba(0, 0, 0, 0.43);\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"\n"
"\n"
"RadioButton {\n"
"    min-height: 24px;\n"
"    max-height: 24px;\n"
"    background-color: transparent;\n"
"    font: 14px \'Segoe UI\', \'Microsoft YaHei\', \'PingFang SC\';\n"
"    color: black;\n"
"}\n"
"\n"
"RadioButton::indicator {\n"
"    width: 18px;\n"
"    height: 18px;\n"
"    border-radius: 11px;\n"
"    border: 2px solid #999999;\n"
"    background-color: rgba(0, 0, 0, 5);\n"
"    margin-right: 4px;\n"
"}\n"
"\n"
"RadioButton::indicator:hover {\n"
"    background-color: rgba(0, 0, 0, 0);\n"
"}\n"
"\n"
"RadioButton::indicator:pressed {\n"
"    border: 2px solid #bbbbbb;\n"
"    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
"            stop:0 rgb(255, 255, 255),\n"
"            stop:0.5 rgb(255, 255, 255),\n"
"            stop:0.6 rgb(225, 224, 223),\n"
"            stop:1 rgb(225, 224, 223));\n"
"}\n"
"\n"
"RadioButton::indicator:checked {\n"
"    height: 22px;\n"
"    width: 22px;\n"
"    border: none;\n"
"    border-radius: 11px;\n"
"    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
"            stop:0 rgb(255, 255, 255),\n"
"            stop:0.5 rgb(255, 255, 255),\n"
"            stop:0.6 #009faa,\n"
"            stop:1 #009faa);\n"
"}\n"
"\n"
"RadioButton::indicator:checked:hover {\n"
"    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
"            stop:0 rgb(255, 255, 255),\n"
"            stop:0.6 rgb(255, 255, 255),\n"
"            stop:0.7 #009faa,\n"
"            stop:1 #009faa);\n"
"}\n"
"\n"
"RadioButton::indicator:checked:pressed {\n"
"    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
"            stop:0 rgb(255, 255, 255),\n"
"            stop:0.5 rgb(255, 255, 255),\n"
"            stop:0.6 #009faa,\n"
"            stop:1 #009faa);\n"
"}\n"
"\n"
"RadioButton:disabled {\n"
"    color: rgba(0, 0, 0, 110);\n"
"}\n"
"\n"
"RadioButton::indicator:disabled {\n"
"    border: 2px solid #bbbbbb;\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"RadioButton::indicator:disabled:checked {\n"
"    border: none;\n"
"    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
"            stop:0 rgb(255, 255, 255),\n"
"            stop:0.5 rgb(255, 255, 255),\n"
"            stop:0.6 rgba(0, 0, 0, 0.2169),\n"
"            stop:1 rgba(0, 0, 0, 0.2169));\n"
"}\n"
"\n"
"TransparentToolButton,\n"
"TransparentToggleToolButton,\n"
"TransparentDropDownToolButton,\n"
"TransparentPushButton,\n"
"TransparentDropDownPushButton,\n"
"TransparentTogglePushButton {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"    border-radius: 5px;\n"
"    margin: 0;\n"
"}\n"
"\n"
"TransparentToolButton:hover,\n"
"TransparentToggleToolButton:hover,\n"
"TransparentDropDownToolButton:hover,\n"
"TransparentPushButton:hover,\n"
"TransparentDropDownPushButton:hover,\n"
"TransparentTogglePushButton:hover {\n"
"    background-color: rgba(0, 0, 0, 9);\n"
"    border: none;\n"
"}\n"
"\n"
"TransparentToolButton:pressed,\n"
"TransparentToggleToolButton:pressed,\n"
"TransparentDropDownToolButton:pressed,\n"
"TransparentPushButton:pressed,\n"
"TransparentDropDownPushButton:pressed,\n"
"TransparentTogglePushButton:pressed {\n"
"    background-color: rgba(0, 0, 0, 6);\n"
"    border: none;\n"
"}\n"
"\n"
"TransparentToolButton:disabled,\n"
"TransparentToggleToolButton:disabled,\n"
"TransparentDropDownToolButton:disabled,\n"
"TransprentPushButton:disabled,\n"
"TransparentDropDownPushButton:disabled,\n"
"TransprentTogglePushButton:disabled {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"\n"
"\n"
"PillPushButton,\n"
"PillPushButton:hover,\n"
"PillPushButton:pressed,\n"
"PillPushButton:disabled,\n"
"PillPushButton:checked,\n"
"PillPushButton:checked:hover,\n"
"PillPushButton:checked:pressed,\n"
"PillPushButton:disabled:checked,\n"
"PillToolButton,\n"
"PillToolButton:hover,\n"
"PillToolButton:pressed,\n"
"PillToolButton:disabled,\n"
"PillToolButton:checked,\n"
"PillToolButton:checked:hover,\n"
"PillToolButton:checked:pressed,\n"
"PillToolButton:disabled:checked {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"")
        self.imagefootprint_filepath_btn.setObjectName("imagefootprint_filepath_btn")
        self.horizontalLayout.addWidget(self.imagefootprint_filepath_btn)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.imagefootprint_process_btn = PrimaryPushButton(self.frame_2)
        self.imagefootprint_process_btn.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.imagefootprint_process_btn.setFont(font)
        self.imagefootprint_process_btn.setStyleSheet("PushButton, ToolButton, ToggleButton, ToggleToolButton {\n"
"    color: black;\n"
"    background: rgba(255, 255, 255, 0.7);\n"
"    border: 1px solid rgba(0, 0, 0, 0.073);\n"
"    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
"    border-radius: 20px;\n"
"    /* font: 14px \'Segoe UI\', \'Microsoft YaHei\'; */\n"
"    padding: 5px 12px 6px 12px;\n"
"    outline: none;\n"
"}\n"
"\n"
"ToolButton {\n"
"    padding: 5px 9px 6px 8px;\n"
"}\n"
"\n"
"PushButton[hasIcon=false] {\n"
"    padding: 5px 12px 6px 12px;\n"
"}\n"
"\n"
"PushButton[hasIcon=true] {\n"
"    padding: 5px 12px 6px 36px;\n"
"}\n"
"\n"
"DropDownToolButton, PrimaryDropDownToolButton {\n"
"    padding: 5px 31px 6px 8px;\n"
"}\n"
"\n"
"DropDownPushButton[hasIcon=false],\n"
"PrimaryDropDownPushButton[hasIcon=false] {\n"
"    padding: 5px 31px 6px 12px;\n"
"}\n"
"\n"
"DropDownPushButton[hasIcon=true],\n"
"PrimaryDropDownPushButton[hasIcon=true] {\n"
"    padding: 5px 31px 6px 36px;\n"
"}\n"
"\n"
"PushButton:hover, ToolButton:hover, ToggleButton:hover, ToggleToolButton:hover {\n"
"    background: rgba(249, 249, 249, 0.5);\n"
"}\n"
"\n"
"PushButton:pressed, ToolButton:pressed, ToggleButton:pressed, ToggleToolButton:pressed {\n"
"    color: rgba(0, 0, 0, 0.63);\n"
"    background: rgba(249, 249, 249, 0.3);\n"
"    border-bottom: 1px solid rgba(0, 0, 0, 0.073);\n"
"}\n"
"\n"
"PushButton:disabled, ToolButton:disabled, ToggleButton:disabled, ToggleToolButton:disabled {\n"
"    color: rgba(0, 0, 0, 0.36);\n"
"    background: rgba(249, 249, 249, 0.3);\n"
"    border: 1px solid rgba(0, 0, 0, 0.06);\n"
"    border-bottom: 1px solid rgba(0, 0, 0, 0.06);\n"
"}\n"
"\n"
"\n"
"PrimaryPushButton,\n"
"PrimaryToolButton,\n"
"ToggleButton:checked,\n"
"ToggleToolButton:checked {\n"
"    color: white;\n"
"    background-color: #009faa;\n"
"    border: 1px solid #00a7b3;\n"
"    border-bottom: 1px solid #007780;\n"
"}\n"
"\n"
"PrimaryPushButton:hover,\n"
"PrimaryToolButton:hover,\n"
"ToggleButton:checked:hover,\n"
"ToggleToolButton:checked:hover {\n"
"    background-color: #00a7b3;\n"
"    border: 1px solid #2daab3;\n"
"    border-bottom: 1px solid #007780;\n"
"}\n"
"\n"
"PrimaryPushButton:pressed,\n"
"PrimaryToolButton:pressed,\n"
"ToggleButton:checked:pressed,\n"
"ToggleToolButton:checked:pressed {\n"
"    color: rgba(255, 255, 255, 0.63);\n"
"    background-color: #3eabb3;\n"
"    border: 1px solid #3eabb3;\n"
"}\n"
"\n"
"PrimaryPushButton:disabled,\n"
"PrimaryToolButton:disabled,\n"
"ToggleButton:checked:disabled,\n"
"ToggleToolButton:checked:disabled {\n"
"    color: rgba(255, 255, 255, 0.9);\n"
"    background-color: rgb(205, 205, 205);\n"
"    border: 1px solid rgb(205, 205, 205);\n"
"}\n"
"\n"
"SplitDropButton,\n"
"PrimarySplitDropButton {\n"
"    border-left: none;\n"
"    border-top-left-radius: 0;\n"
"    border-bottom-left-radius: 0;\n"
"}\n"
"\n"
"#splitPushButton,\n"
"#splitToolButton,\n"
"#primarySplitPushButton,\n"
"#primarySplitToolButton {\n"
"    border-top-right-radius: 0;\n"
"    border-bottom-right-radius: 0;\n"
"}\n"
"\n"
"#splitPushButton:pressed,\n"
"#splitToolButton:pressed,\n"
"SplitDropButton:pressed {\n"
"    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
"}\n"
"\n"
"PrimarySplitDropButton:pressed {\n"
"    border-bottom: 1px solid #007780;\n"
"}\n"
"\n"
"#primarySplitPushButton, #primarySplitToolButton {\n"
"    border-right: 1px solid #3eabb3;\n"
"}\n"
"\n"
"#primarySplitPushButton:pressed, #primarySplitToolButton:pressed {\n"
"    border-bottom: 1px solid #007780;\n"
"}\n"
"\n"
"HyperlinkButton {\n"
"    /* font: 14px \'Segoe UI\', \'Microsoft YaHei\'; */\n"
"    padding: 6px 12px 6px 12px;\n"
"    color: #009faa;\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"HyperlinkButton[hasIcon=false] {\n"
"    padding: 6px 12px 6px 12px;\n"
"}\n"
"\n"
"HyperlinkButton[hasIcon=true] {\n"
"    padding: 6px 12px 6px 36px;\n"
"}\n"
"\n"
"HyperlinkButton:hover {\n"
"    color: #009faa;\n"
"    background-color: rgba(0, 0, 0, 10);\n"
"    border: none;\n"
"}\n"
"\n"
"HyperlinkButton:pressed {\n"
"    color: #009faa;\n"
"    background-color: rgba(0, 0, 0, 6);\n"
"    border: none;\n"
"}\n"
"\n"
"HyperlinkButton:disabled {\n"
"    color: rgba(0, 0, 0, 0.43);\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"\n"
"\n"
"RadioButton {\n"
"    min-height: 24px;\n"
"    max-height: 24px;\n"
"    background-color: transparent;\n"
"    font: 14px \'Segoe UI\', \'Microsoft YaHei\', \'PingFang SC\';\n"
"    color: black;\n"
"}\n"
"\n"
"RadioButton::indicator {\n"
"    width: 18px;\n"
"    height: 18px;\n"
"    border-radius: 11px;\n"
"    border: 2px solid #999999;\n"
"    background-color: rgba(0, 0, 0, 5);\n"
"    margin-right: 4px;\n"
"}\n"
"\n"
"RadioButton::indicator:hover {\n"
"    background-color: rgba(0, 0, 0, 0);\n"
"}\n"
"\n"
"RadioButton::indicator:pressed {\n"
"    border: 2px solid #bbbbbb;\n"
"    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
"            stop:0 rgb(255, 255, 255),\n"
"            stop:0.5 rgb(255, 255, 255),\n"
"            stop:0.6 rgb(225, 224, 223),\n"
"            stop:1 rgb(225, 224, 223));\n"
"}\n"
"\n"
"RadioButton::indicator:checked {\n"
"    height: 22px;\n"
"    width: 22px;\n"
"    border: none;\n"
"    border-radius: 11px;\n"
"    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
"            stop:0 rgb(255, 255, 255),\n"
"            stop:0.5 rgb(255, 255, 255),\n"
"            stop:0.6 #009faa,\n"
"            stop:1 #009faa);\n"
"}\n"
"\n"
"RadioButton::indicator:checked:hover {\n"
"    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
"            stop:0 rgb(255, 255, 255),\n"
"            stop:0.6 rgb(255, 255, 255),\n"
"            stop:0.7 #009faa,\n"
"            stop:1 #009faa);\n"
"}\n"
"\n"
"RadioButton::indicator:checked:pressed {\n"
"    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
"            stop:0 rgb(255, 255, 255),\n"
"            stop:0.5 rgb(255, 255, 255),\n"
"            stop:0.6 #009faa,\n"
"            stop:1 #009faa);\n"
"}\n"
"\n"
"RadioButton:disabled {\n"
"    color: rgba(0, 0, 0, 110);\n"
"}\n"
"\n"
"RadioButton::indicator:disabled {\n"
"    border: 2px solid #bbbbbb;\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"RadioButton::indicator:disabled:checked {\n"
"    border: none;\n"
"    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
"            stop:0 rgb(255, 255, 255),\n"
"            stop:0.5 rgb(255, 255, 255),\n"
"            stop:0.6 rgba(0, 0, 0, 0.2169),\n"
"            stop:1 rgba(0, 0, 0, 0.2169));\n"
"}\n"
"\n"
"TransparentToolButton,\n"
"TransparentToggleToolButton,\n"
"TransparentDropDownToolButton,\n"
"TransparentPushButton,\n"
"TransparentDropDownPushButton,\n"
"TransparentTogglePushButton {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"    border-radius: 5px;\n"
"    margin: 0;\n"
"}\n"
"\n"
"TransparentToolButton:hover,\n"
"TransparentToggleToolButton:hover,\n"
"TransparentDropDownToolButton:hover,\n"
"TransparentPushButton:hover,\n"
"TransparentDropDownPushButton:hover,\n"
"TransparentTogglePushButton:hover {\n"
"    background-color: rgba(0, 0, 0, 9);\n"
"    border: none;\n"
"}\n"
"\n"
"TransparentToolButton:pressed,\n"
"TransparentToggleToolButton:pressed,\n"
"TransparentDropDownToolButton:pressed,\n"
"TransparentPushButton:pressed,\n"
"TransparentDropDownPushButton:pressed,\n"
"TransparentTogglePushButton:pressed {\n"
"    background-color: rgba(0, 0, 0, 6);\n"
"    border: none;\n"
"}\n"
"\n"
"TransparentToolButton:disabled,\n"
"TransparentToggleToolButton:disabled,\n"
"TransparentDropDownToolButton:disabled,\n"
"TransprentPushButton:disabled,\n"
"TransparentDropDownPushButton:disabled,\n"
"TransprentTogglePushButton:disabled {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"\n"
"\n"
"PillPushButton,\n"
"PillPushButton:hover,\n"
"PillPushButton:pressed,\n"
"PillPushButton:disabled,\n"
"PillPushButton:checked,\n"
"PillPushButton:checked:hover,\n"
"PillPushButton:checked:pressed,\n"
"PillPushButton:disabled:checked,\n"
"PillToolButton,\n"
"PillToolButton:hover,\n"
"PillToolButton:pressed,\n"
"PillToolButton:disabled,\n"
"PillToolButton:checked,\n"
"PillToolButton:checked:hover,\n"
"PillToolButton:checked:pressed,\n"
"PillToolButton:disabled:checked {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"")
        self.imagefootprint_process_btn.setObjectName("imagefootprint_process_btn")
        self.verticalLayout_4.addWidget(self.imagefootprint_process_btn)


        self.progressBar = IndeterminateProgressBar(self.frame_2, start=0)

        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_4.addWidget(self.progressBar)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        spacerItem3 = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.verticalLayout.addWidget(self.CardWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.TitleLabel_3.setText(_translate("Form", "栅格影像的有效范围轮廓矢量生成"))
        self.imagefootprint_prompt.setText(_translate("Form", "用前必看(请点击)"))
        self.imagefootprint_filepath_btn.setText(_translate("Form", "获取路径"))
        self.imagefootprint_process_btn.setText(_translate("Form", "开始转换"))
from qfluentwidgets import CardWidget, LineEdit, PrimaryPushButton, PushButton, TitleLabel
