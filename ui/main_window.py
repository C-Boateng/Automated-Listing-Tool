import sys
import json
import torch
import joblib
from html import escape
from ultralytics import SAM
from processing import Processor
from ui.validator import Validator
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont
from transformers import BertTokenizer
from utils.config import (
    MAX_IMAGES, PROGRESS_INCREMENT, DEFAULT_STYLE, RED_BORDER_STYLE,
    IMAGE_LABEL_STYLE, SUBMIT_BUTTON_STYLE
)
from models.bert_classifier_model import BertForMultiTaskClassification
from ui.pages import setup_main_page, setup_loading_page, setup_review_page
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QComboBox, QLineEdit, QRadioButton, QCheckBox, QFileDialog,
    QProgressBar, QStackedWidget, QScrollArea, QTextEdit, QMessageBox
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.images = []  # Store tuples of (pixmap, file_path)
        # Keep track of current image for visualisation the image frame
        self.current_image_index = 0
        self.current_review_image_index = 0
        self.color_results = []  # Tally the color counts from all images
        # Store most frequently counted colors
        self.vinted_color = ""
        self.ebay_color = ""
        self.model = SAM('sam2_b.pt')  # Initialize SAM2 model
        self.size = None # Garment size
        self.processor = Processor(self) # Managing pipeline order and progressbar
        self.validator = Validator(self) # Validate user input

        # Load Fine-tuned BERT model
        with open('bert_category_classifier_complete/model_config.json', 'r') as f:
            config = json.load(f)
        num_vinted_classes = config['num_vinted_classes']
        num_ebay_classes = config['num_ebay_classes']
        self.bert_model = BertForMultiTaskClassification(num_vinted_classes, num_ebay_classes)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.bert_model.to(self.device)
        self.bert_model.load_state_dict(torch.load('bert_category_classifier_complete/best_bert_category_classifier.pth', map_location=torch.device(self.device)))
        self.bert_model.eval()
        self.tokenizer = BertTokenizer.from_pretrained('bert_category_classifier_complete/bert_category_classifier')
        self.vinted_encoder = joblib.load('bert_category_classifier_complete/vinted_encoder.pkl')
        self.ebay_encoder = joblib.load('bert_category_classifier_complete/ebay_encoder.pkl')

        self.initUI()

    def initUI(self):
        self.setWindowTitle('AI Listing Tool')
        self.resize(800, 650)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        setup_main_page(self)
        setup_loading_page(self)
        setup_review_page(self)
        self.center()
        self.show()

    def start_processing(self):
        if not self.validator.validate_inputs():
            return

        self.size = self.size_combo.currentText()
        self.price = self.price_input.value()

        self.processor.start()

    def update_progress(self):
        self.processor.update()

    def upload_image(self, event):
        file_names, _ = QFileDialog.getOpenFileNames(
            self, "Select Images", "",
            "Images (*.png *.jpg *.jpeg)"
        )
        if file_names:
            if len(self.images) + len(file_names) > MAX_IMAGES:
                QMessageBox.warning(
                    self, "Image Limit Reached",
                    f"You can upload a maximum of {MAX_IMAGES} images per listing."
                )
                remaining_slots = MAX_IMAGES - len(self.images)
                file_names = file_names[:remaining_slots]
            
            if file_names:
                for file_name in file_names:
                    pixmap = QPixmap(file_name)
                    if not pixmap.isNull():
                        self.images.append((pixmap, file_name))  # Store image and file path
                    else:
                        QMessageBox.warning(
                            self, "Invalid Image",
                            f"Failed to load image: {file_name}"
                        )
                
                if self.images:
                    self.current_image_index = len(self.images) - 1
                    self.update_image_display()
                    self.update_navigation()

    # Helper
    def _parse_listing_text(self, listing_text):
        try:
            platform_listings = {}
            sections = listing_text.split('=== ')[1:]
            for section in sections:
                platform, content = section.split(' ===\n', 1) # Exctract platform name and its title/description content
                title_start = content.index('Title: ') + len('Title: ')
                description_start = content.index('ion:') + len('ion:') # Tinyllama often outputs "Descripion:", instead of "Description:". We will permit only such slack.
                title_end = content.index('Descrip')
                description_end = content.index('=====')
                title = content[title_start:title_end].strip() # Exctract title with found indices and remove trailing whitespaces
                description = content[description_start:description_end].strip() # Same for description part of this platform's content
                platform_listings[platform] = {'title': escape(title), 'description': description}
        except:
            return None

        return platform_listings

    def generate_listing(self):
        """Generate a structured HTML listing for the review page."""
        # Parse LLM-generated text
        platform_listings = self._parse_listing_text(self.listing_text)
        
        # Determine selected platforms
        platforms = []
        if self.checkbox1.isChecked():
            platforms.append("eBay")
        if self.checkbox2.isChecked():
            platforms.append("Vinted")
        
        # Collect general data
        images_count = len(self.images)
        price = f"€{self.price:.2f}"
        
        # Build HTML with styling
        html = '<div style="font-family: Arial, sans-serif;">'
        
        # General information
        html += f'<b>Platforms:</b> {", ".join(platforms)}<br>'
        html += f'<b>Images:</b> {images_count} images uploaded<br>'
        html += f'<b>Price:</b> {price}<br><br>'
        # Platform-specific sections
        for platform in platforms:
            if platform in platform_listings:
                listing = platform_listings[platform]
                color = escape(self.ebay_color if platform == "eBay" else self.vinted_color)
                category = escape(self.ebay_category if platform == "eBay" else self.vinted_category)
                html += f'<div style="margin-bottom: 20px;">'
                html += f'<b>{platform}</b><br>'
                html += f'<b>Title:</b> {listing["title"]}<br>'
                html += f'<b>Description:</b> {listing["description"]}<br>'
                html += f'<b>Primary color:</b> {color}.<br>'
                html += f'<b>Category:</b> {category}.<br>'
                html += '</div>'
            else:
                html += f'<div style="color: red;">No listing generated for {platform}</div><br>'
        
        html += '</div>'
        
        # Set the HTML content
        self.listing_content.setHtml(html)
        self.current_review_image_index = 0
        self.update_review_image_display()

    def return_to_main(self):
        self.stacked_widget.setCurrentWidget(self.main_page)

    def finalize_listing(self):
        print("Listing finalized!")
        self.return_to_main()

    def confirm_remove_image(self):
        if self.images:
            reply = QMessageBox.question(
                self, "Confirm Deletion",
                "Are you sure you want to remove this image?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
            )
            if reply == QMessageBox.Yes:
                self.remove_image()

    def remove_image(self):
        if self.images:
            self.images.pop(self.current_image_index)
            if self.images:
                if self.current_image_index >= len(self.images):
                    self.current_image_index = len(self.images) - 1
            else:
                self.current_image_index = 0
            self.update_image_display()
            self.update_navigation()

    def update_image_display(self):
        if self.images:
            scaled_pixmap = self.images[self.current_image_index][0].scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setText("")
        else:
            self.image_label.setPixmap(QPixmap())
            self.image_label.setText("Click to upload an image")

    def update_review_image_display(self):
        if self.images:
            scaled_pixmap = self.images[self.current_review_image_index][0].scaled(
                self.review_image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.review_image_label.setPixmap(scaled_pixmap)
        else:
            self.review_image_label.setPixmap(QPixmap())
        self.update_review_navigation()

    def update_navigation(self):
        has_multiple_images = len(self.images) >= 2
        self.prev_button.setVisible(has_multiple_images)
        self.next_button.setVisible(has_multiple_images)
        self.dots_container.setVisible(has_multiple_images)
        self.remove_button.setVisible(len(self.images) > 0)
        
        for i in reversed(range(self.dots_layout.count())):
            self.dots_layout.itemAt(i).widget().deleteLater()
        
        for i in range(len(self.images)):
            dot = QLabel("●" if i == self.current_image_index else "○")
            dot.setStyleSheet(f"color: {'black' if i == self.current_image_index else 'gray'};")
            dot.setFont(QFont("Arial", 12))
            self.dots_layout.addWidget(dot)

    def update_review_navigation(self):
        has_multiple_images = len(self.images) >= 2
        self.review_prev_button.setVisible(has_multiple_images)
        self.review_next_button.setVisible(has_multiple_images)
        self.review_dots_container.setVisible(has_multiple_images)
        
        for i in reversed(range(self.review_dots_layout.count())):
            self.review_dots_layout.itemAt(i).widget().deleteLater()
        
        for i in range(len(self.images)):
            dot = QLabel("●" if i == self.current_review_image_index else "○")
            dot.setStyleSheet(f"color: {'black' if i == self.current_review_image_index else 'gray'};")
            dot.setFont(QFont("Arial", 12))
            self.review_dots_layout.addWidget(dot)

    def show_previous_image(self):
        if self.images:
            self.current_image_index = (self.current_image_index - 1) % len(self.images)
            self.update_image_display()
            self.update_navigation()

    def show_next_image(self):
        if self.images:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.update_image_display()
            self.update_navigation()

    def show_previous_review_image(self):
        if self.images:
            self.current_review_image_index = (self.current_review_image_index - 1) % len(self.images)
            self.update_review_image_display()

    def show_next_review_image(self):
        if self.images:
            self.current_review_image_index = (self.current_review_image_index + 1) % len(self.images)
            self.update_review_image_display()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y - 60)