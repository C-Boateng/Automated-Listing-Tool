from utils.config import RED_BORDER_STYLE, IMAGE_LABEL_STYLE, DEFAULT_STYLE
from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QCheckBox, QWidget, QDoubleSpinBox

class Validator:
    def __init__(self, main_window):
        self.main_window = main_window

    def validate_inputs(self) -> bool:
        """Validates all user inputs, highlighting invalid fields with red borders."""
        is_valid = True
        self.reset_styles()

        if not self.main_window.images:
            self.main_window.image_label.setStyleSheet(RED_BORDER_STYLE)
            is_valid = False
        if not self.main_window.description_input.text().strip():
            self.main_window.description_input.setStyleSheet(RED_BORDER_STYLE)
            is_valid = False
        if not (self.main_window.checkbox1.isChecked() or self.main_window.checkbox2.isChecked()):
            self.main_window.checkbox_container.setStyleSheet(RED_BORDER_STYLE)
            is_valid = False
        if not (self.main_window.radio1.isChecked() or self.main_window.radio2.isChecked() or self.main_window.radio3.isChecked()):
            self.main_window.radio_container.setStyleSheet(RED_BORDER_STYLE)
            is_valid = False
        if self.main_window.size_combo.currentText() == "Enter size:":
            self.main_window.size_combo.setStyleSheet(RED_BORDER_STYLE)
            is_valid = False
        if self.main_window.price_input.value() <= 0.0:
            self.main_window.price_input.setStyleSheet(RED_BORDER_STYLE)
            is_valid = False

        return is_valid

    def reset_styles(self) -> None:
        """Resets all input field styles to default."""
        self.main_window.image_label.setStyleSheet(IMAGE_LABEL_STYLE)
        self.main_window.description_input.setStyleSheet(DEFAULT_STYLE)
        self.main_window.radio_container.setStyleSheet(DEFAULT_STYLE)
        self.main_window.checkbox_container.setStyleSheet(DEFAULT_STYLE)
        self.main_window.size_combo.setStyleSheet(DEFAULT_STYLE)
        self.main_window.price_input.setStyleSheet(DEFAULT_STYLE)