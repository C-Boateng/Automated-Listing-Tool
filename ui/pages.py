from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils.config import DEFAULT_STYLE, IMAGE_LABEL_STYLE, SUBMIT_BUTTON_STYLE
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit,
    QRadioButton, QCheckBox, QProgressBar, QStackedWidget, QScrollArea, QTextEdit, 
    QDoubleSpinBox
)

def setup_main_page(main_window):
    main_window.main_page = QWidget()
    main_layout = QVBoxLayout(main_window.main_page)
    main_layout.setAlignment(Qt.AlignTop)
    main_layout.setContentsMargins(20, 20, 20, 20)

    # Image upload area with navigation
    image_container = QWidget()
    image_layout = QHBoxLayout(image_container)
    
    main_window.prev_button = QPushButton("<")
    main_window.prev_button.setFixedSize(30, 30)
    main_window.prev_button.clicked.connect(main_window.show_previous_image)
    main_window.prev_button.setVisible(False)
    image_layout.addWidget(main_window.prev_button)

    main_window.image_label = QLabel("Click to upload an image")
    main_window.image_label.setFixedSize(200, 200)
    main_window.image_label.setStyleSheet(IMAGE_LABEL_STYLE)
    main_window.image_label.setAlignment(Qt.AlignCenter)
    main_window.image_label.setCursor(Qt.PointingHandCursor)
    main_window.image_label.mousePressEvent = main_window.upload_image
    image_layout.addWidget(main_window.image_label)

    main_window.next_button = QPushButton(">")
    main_window.next_button.setFixedSize(30, 30)
    main_window.next_button.clicked.connect(main_window.show_next_image)
    main_window.next_button.setVisible(False)
    image_layout.addWidget(main_window.next_button)

    main_layout.addWidget(image_container, alignment=Qt.AlignCenter)

    # Indicator dots and remove button container
    main_window.controls_container = QWidget()
    main_window.controls_layout = QVBoxLayout(main_window.controls_container)
    main_window.controls_layout.setContentsMargins(0, 0, 0, 0)
    
    main_window.dots_container = QWidget()
    main_window.dots_layout = QHBoxLayout(main_window.dots_container)
    main_window.dots_layout.setContentsMargins(0, 0, 0, 0)
    main_window.dots_layout.setAlignment(Qt.AlignCenter)
    main_window.dots_container.setVisible(False)
    main_window.controls_layout.addWidget(main_window.dots_container)

    main_window.remove_button = QPushButton("Remove Image")
    main_window.remove_button.setFixedWidth(100)
    main_window.remove_button.clicked.connect(main_window.confirm_remove_image)
    main_window.remove_button.setVisible(False)
    main_window.controls_layout.addWidget(main_window.remove_button, alignment=Qt.AlignCenter)
    
    main_layout.addWidget(main_window.controls_container)

    # Other inputs
    gender_label = QLabel("Gender:")
    gender_label.setFont(QFont("Arial", 10, QFont.Bold))
    main_layout.addWidget(gender_label)
    main_window.gender_combo = QComboBox()
    main_window.gender_combo.addItems(["Men", "Women"])
    main_window.gender_combo.setStyleSheet(DEFAULT_STYLE)
    main_layout.addWidget(main_window.gender_combo)

    # Price input
    price_label = QLabel("Price (€):")
    price_label.setFont(QFont("Arial", 10, QFont.Bold))
    main_layout.addWidget(price_label)
    main_window.price_input = QDoubleSpinBox()
    main_window.price_input.setRange(0.0, 3000.0) # Range
    main_window.price_input.setDecimals(2)  # Two decimals
    main_window.price_input.setValue(0.0)  # Default value
    main_window.price_input.setStyleSheet(DEFAULT_STYLE)
    main_window.price_input.setFixedWidth(100)
    main_layout.addWidget(main_window.price_input)

    product_label = QLabel("Product:")
    product_label.setFont(QFont("Arial", 10, QFont.Bold))
    main_layout.addWidget(product_label)
    main_window.description_input = QLineEdit()
    main_window.description_input.setPlaceholderText("Enter short description")
    main_window.description_input.setStyleSheet(DEFAULT_STYLE)
    main_layout.addWidget(main_window.description_input)

    radio_label = QLabel("Quality Rating:")
    radio_label.setFont(QFont("Arial", 10, QFont.Bold))
    main_layout.addWidget(radio_label)
    main_window.radio_container = QWidget()
    main_window.radio_layout = QHBoxLayout(main_window.radio_container)
    main_window.radio_container.setStyleSheet(DEFAULT_STYLE)
    main_window.radio1 = QRadioButton("* - Fair")
    main_window.radio2 = QRadioButton("** - Good")
    main_window.radio3 = QRadioButton("*** - Excellent")
    main_window.radio_layout.addWidget(main_window.radio1)
    main_window.radio_layout.addWidget(main_window.radio2)
    main_window.radio_layout.addWidget(main_window.radio3)
    main_layout.addWidget(main_window.radio_container)

    size_label = QLabel("Size:")
    size_label.setFont(QFont("Arial", 10, QFont.Bold))
    main_layout.addWidget(size_label)
    main_window.size_combo = QComboBox()
    main_window.size_combo.addItems(["Enter size:", "XS", "S", "M", "L", "XL"])
    main_window.size_combo.setStyleSheet(DEFAULT_STYLE)
    main_layout.addWidget(main_window.size_combo)

    checkbox_label = QLabel("List to:")
    checkbox_label.setFont(QFont("Arial", 10, QFont.Bold))
    main_layout.addWidget(checkbox_label)
    main_window.checkbox_container = QWidget()
    main_window.checkbox_layout = QVBoxLayout(main_window.checkbox_container)
    main_window.checkbox_container.setStyleSheet(DEFAULT_STYLE)
    main_window.checkbox1 = QCheckBox("eBay")
    main_window.checkbox2 = QCheckBox("Vinted")
    main_window.checkbox1.setChecked(True)
    main_window.checkbox2.setChecked(True)
    main_window.checkbox_layout.addWidget(main_window.checkbox1)
    main_window.checkbox_layout.addWidget(main_window.checkbox2)
    main_layout.addWidget(main_window.checkbox_container)

    main_layout.addStretch()

    button_container = QWidget()
    button_layout = QHBoxLayout(button_container)
    button_layout.addStretch()
    main_window.submit_button = QPushButton("Generate Listings")
    main_window.submit_button.setFixedWidth(150)
    main_window.submit_button.setStyleSheet(SUBMIT_BUTTON_STYLE)
    main_window.submit_button.clicked.connect(main_window.start_processing)
    button_layout.addWidget(main_window.submit_button)
    main_layout.addWidget(button_container)

    main_window.stacked_widget.addWidget(main_window.main_page)

def setup_loading_page(main_window):
    main_window.loading_page = QWidget()
    loading_layout = QVBoxLayout(main_window.loading_page)
    loading_layout.setAlignment(Qt.AlignCenter)
    main_window.loading_label = QLabel("Generating listing...")
    main_window.loading_label.setFont(QFont("Arial", 12))
    loading_layout.addWidget(main_window.loading_label)
    main_window.progress_bar = QProgressBar()
    main_window.progress_bar.setMaximum(100)
    main_window.progress_bar.setValue(0)
    loading_layout.addWidget(main_window.progress_bar)
    loading_layout.addStretch()
    main_window.stacked_widget.addWidget(main_window.loading_page)

def setup_review_page(main_window):
    main_window.review_page = QWidget()
    review_layout = QVBoxLayout(main_window.review_page)
    review_layout.setContentsMargins(20, 20, 20, 20)

    review_image_container = QWidget()
    review_image_layout = QHBoxLayout(review_image_container)
    
    main_window.review_prev_button = QPushButton("<")
    main_window.review_prev_button.setFixedSize(30, 30)
    main_window.review_prev_button.clicked.connect(main_window.show_previous_review_image)
    main_window.review_prev_button.setVisible(False)
    review_image_layout.addWidget(main_window.review_prev_button)

    main_window.review_image_label = QLabel()
    main_window.review_image_label.setFixedSize(200, 200)
    main_window.review_image_label.setStyleSheet("border: 2px solid gray;")
    main_window.review_image_label.setAlignment(Qt.AlignCenter)
    review_image_layout.addWidget(main_window.review_image_label)

    main_window.review_next_button = QPushButton(">")
    main_window.review_next_button.setFixedSize(30, 30)
    main_window.review_next_button.clicked.connect(main_window.show_next_review_image)
    main_window.review_next_button.setVisible(False)
    review_image_layout.addWidget(main_window.review_next_button)

    review_layout.addWidget(review_image_container, alignment=Qt.AlignCenter)

    main_window.review_dots_container = QWidget()
    main_window.review_dots_layout = QHBoxLayout(main_window.review_dots_container)
    main_window.review_dots_layout.setAlignment(Qt.AlignCenter)
    main_window.review_dots_container.setVisible(False)
    review_layout.addWidget(main_window.review_dots_container)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_content = QWidget()
    main_window.scroll_layout = QVBoxLayout(scroll_content)
    main_window.scroll_layout.setAlignment(Qt.AlignTop)

    main_window.listing_content = QTextEdit()
    main_window.listing_content.setReadOnly(True)
    main_window.listing_content.setMinimumHeight(300)
    main_window.scroll_layout.addWidget(main_window.listing_content)
    scroll_area.setWidget(scroll_content)
    review_layout.addWidget(scroll_area)

    review_button_container = QWidget()
    review_button_layout = QHBoxLayout(review_button_container)
    review_button_layout.addStretch()
    main_window.redo_button = QPushButton("Redo")
    main_window.redo_button.setFixedWidth(100)
    main_window.redo_button.clicked.connect(main_window.return_to_main)
    review_button_layout.addWidget(main_window.redo_button)
    main_window.list_button = QPushButton("List")
    main_window.list_button.setFixedWidth(100)
    main_window.list_button.clicked.connect(main_window.finalize_listing)
    review_button_layout.addWidget(main_window.list_button)
    review_layout.addWidget(review_button_container)

    main_window.stacked_widget.addWidget(main_window.review_page)