import torch
from enum import Enum
from collections import namedtuple
from typing import Dict
from PyQt5.QtCore import QTimer
from image_processing import process_image
from utils.listing_utils import generate_text

class ProcessingState(Enum):
    INIT = 0
    EXTRACT_COLORS = 1
    GENERATE_TITLE = 2
    PREDICT_CATEGORIES = 3
    GENERATE_TEXT = 4
    DONE = 5

Task = namedtuple('Task', ['state', 'progress', 'label'])

PROCESSING_TASKS = [
    Task(ProcessingState.EXTRACT_COLORS, 25, "Extracting colors from images..."),
    Task(ProcessingState.GENERATE_TITLE, 50, "Generating title..."),
    Task(ProcessingState.PREDICT_CATEGORIES, 75, "Predicting categories with BERT..."),
    Task(ProcessingState.GENERATE_TEXT, 100, "Generating text with LLM..."),
]

class Processor:
    def __init__(self, main_window):
        self.main_window = main_window
        self.current_task_index = 0

    def start(self):
        """Starts the processing pipeline, switching to the loading page."""
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.loading_page)
        self.main_window.submit_button.setEnabled(False)
        self.main_window.progress = 0
        self.main_window.color_results = []
        self.main_window.timer = QTimer()
        self.main_window.timer.timeout.connect(self.update)
        self.main_window.timer.start(100)

    def update(self):
        """Updates the progress bar and executes the current task."""
        if self.current_task_index >= len(PROCESSING_TASKS):
            self.main_window.timer.stop()
            self.main_window.stacked_widget.setCurrentWidget(self.main_window.review_page)
            self.main_window.submit_button.setEnabled(True)
            self.main_window.current_review_image_index = 0
            self.main_window.update_review_image_display()
            self.main_window.generate_listing()
            return

        task = PROCESSING_TASKS[self.current_task_index]
        self.main_window.progress_bar.setValue(task.progress)
        self.main_window.loading_label.setText(task.label)

        if task.state == ProcessingState.EXTRACT_COLORS:
            self.extract_colors()
        elif task.state == ProcessingState.GENERATE_TITLE:
            pass  
        elif task.state == ProcessingState.PREDICT_CATEGORIES:
            self.predict_categories()
        elif task.state == ProcessingState.GENERATE_TEXT:
            self.generate_text()

        self.current_task_index += 1

    def extract_colors(self):
        """Extracts dominant colors from images using SAM and KMeans."""
        for _, file_path in self.main_window.images:
            color_result = process_image(file_path, self.main_window.model)
            self.main_window.color_results.append(color_result)
        ebay_color_counts = {}
        vinted_color_counts = {}
        for color_result in self.main_window.color_results:
            if color_result:
                if self.main_window.checkbox1.isChecked():
                    ebay_color = color_result['ebay_color']
                    ebay_color_counts[ebay_color] = ebay_color_counts.get(ebay_color, 0) + 1
                if self.main_window.checkbox2.isChecked():
                    vinted_color = color_result['vinted_color']
                    vinted_color_counts[vinted_color] = vinted_color_counts.get(vinted_color, 0) + 1
        self.main_window.ebay_color = max(ebay_color_counts, key=ebay_color_counts.get, default="Unknown")
        self.main_window.vinted_color = max(vinted_color_counts, key=vinted_color_counts.get, default="Unknown")

    def predict_categories(self):
        """Predicts Vinted and eBay categories using the BERT model."""
        gender = self.main_window.gender_combo.currentText()
        description = self.main_window.description_input.text().strip()
        inputs = self.main_window.tokenizer(
            f'{gender}\'s {description}', return_tensors="pt", truncation=True, padding=True
        ).to(self.main_window.device)
        if 'token_type_ids' in inputs:
            del inputs['token_type_ids']
        with torch.no_grad():
            outputs = self.main_window.bert_model(**inputs)
        self.main_window.vinted_category = (
            self.main_window.vinted_encoder.inverse_transform(
                [torch.argmax(outputs['vinted_logits'], dim=1).cpu().numpy()[0]]
            )[0] if self.main_window.checkbox2.isChecked() else "N/A"
        )
        self.main_window.ebay_category = (
            self.main_window.ebay_encoder.inverse_transform(
                [torch.argmax(outputs['ebay_logits'], dim=1).cpu().numpy()[0]]
            )[0] if self.main_window.checkbox1.isChecked() else "N/A"
        )

        self.main_window.listing_attributes = {
            "product": description,
            "gender": gender,
            "color": self.main_window.ebay_color if self.main_window.checkbox2.isChecked() else self.main_window.vinted_color,
            "category": {
                "vinted": self.main_window.vinted_category,
                "ebay": self.main_window.ebay_category
            },
            "size": self.main_window.size,
            "condition": (
                "Fair" if self.main_window.radio1.isChecked() else
                "Good" if self.main_window.radio2.isChecked() else
                "Excellent"
            ),
            "price": self.main_window.price
        }

    def generate_text(self):
        """Generates listing text using the LLM."""
        self.main_window.listing_text = generate_text(self.main_window.listing_attributes)
        print('/', self.main_window.listing_attributes, '/')