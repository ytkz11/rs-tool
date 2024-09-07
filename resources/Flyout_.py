#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: Flyout_.py
# time: 2024/9/7 20:13


from PyQt5.QtWidgets import QVBoxLayout
from qfluentwidgets import (PushButton, Flyout, InfoBarIcon, setTheme, Theme, FlyoutView, FlyoutViewBase,
                            BodyLabel, setFont, PrimaryPushButton, FlyoutAnimationType)
class CustomFlyoutView(FlyoutViewBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.label = BodyLabel(
            '处理已完成')
        self.button = PrimaryPushButton('关闭')

        self.button.setFixedWidth(140)
        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(20, 16, 20, 16)
        self.vBoxLayout.addWidget(self.label)
        self.vBoxLayout.addWidget(self.button)

        self.button.clicked.connect(self.close)
    def close(self):
            """关闭窗口的方法"""
            super().close()  # 调用基类的关闭方法
            print("窗口已关闭")
