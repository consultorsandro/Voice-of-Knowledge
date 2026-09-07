import sys

from PySide6.QtCore import QThread

from voice_of_knowledge.gui.conversion_worker import ConversionWorker
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
    QMessageBox,
)

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Voice of Knowledge")
        self.resize(760, 420)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        title = QLabel("VOICE OF KNOWLEDGE")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold; margin-bottom: 20px;"
        )

        main_layout.addWidget(title)

        form_layout = QGridLayout()

        self.input_file_edit = QLineEdit()
        self.input_file_button = QPushButton("Selecionar")
        self.output_dir_edit = QLineEdit()
        self.output_dir_button = QPushButton("Selecionar")

        self.max_words_spin = QSpinBox()
        self.max_words_spin.setRange(50, 2000)
        self.max_words_spin.setValue(350)
        self.max_words_spin.setSuffix(" palavras")

        form_layout = QGridLayout()

        form_layout.addWidget(QLabel("Arquivo:"), 0, 0)
        form_layout.addWidget(self.input_file_edit, 0, 1)
        form_layout.addWidget(self.input_file_button, 0, 2)

        form_layout.addWidget(QLabel("Pasta de destino:"), 1, 0)
        form_layout.addWidget(self.output_dir_edit, 1, 1)
        form_layout.addWidget(self.output_dir_button, 1, 2)

        form_layout.addWidget(QLabel("Tamanho das partes:"), 2, 0)
        form_layout.addWidget(self.max_words_spin, 2, 1)

        main_layout.addLayout(form_layout)

        self.convert_button = QPushButton("CONVERTER PARA ÁUDIO")
        self.convert_button.setMinimumHeight(45)
        self.convert_button.clicked.connect(self.validate_conversion)

        main_layout.addWidget(self.convert_button)

        self.progress_label = QLabel("Progresso:")
        self.status_label = QLabel("Aguardando conversão.")

        main_layout.addWidget(self.progress_label)
        main_layout.addWidget(self.status_label)

        main_layout.addStretch()

        self.output_dir_button.clicked.connect(self.select_output_dir)
        self.input_file_button.clicked.connect(self.select_input_file)

    def select_output_dir(self) -> None:
        directory = QFileDialog.getExistingDirectory(
            self,
            "Selecionar pasta de destino",
        )

        if directory:
            self.output_dir_edit.setText(directory)

    def validate_conversion(self) -> None:
        input_file = self.input_file_edit.text().strip()
        output_dir = self.output_dir_edit.text().strip()

        if not input_file:
            QMessageBox.warning(
                self,
                "Arquivo não selecionado",
                "Selecione um arquivo TXT ou PDF.",
            )
            return

        if not output_dir:
            QMessageBox.warning(
                self,
                "Pasta não selecionada",
                "Selecione a pasta de destino dos arquivos de áudio.",
            )
            return

        self.start_conversion(
            input_file,
            output_dir,
            self.max_words_spin.value(),
        )

    def start_conversion(
        self,
        input_file: str,
        output_dir: str,
        max_words: int,
    ) -> None:
        self.convert_button.setEnabled(False)
        self.status_label.setText("Iniciando conversão...")

        self.thread = QThread()

        self.worker = ConversionWorker(
            input_file,
            output_dir,
            max_words,
        )

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)

        self.worker.finished.connect(self.conversion_finished)
        self.worker.error.connect(self.conversion_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)

        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def conversion_finished(self, output_paths: list) -> None:
        self.convert_button.setEnabled(True)

        self.status_label.setText(
            f"Conversão concluída. {len(output_paths)} arquivo(s) gerado(s)."
        )

        QMessageBox.information(
            self,
            "Conversão concluída",
            f"{len(output_paths)} arquivo(s) de áudio foram gerados.",
        )

    def conversion_error(self, message: str) -> None:
        self.convert_button.setEnabled(True)
        self.status_label.setText("Erro durante a conversão.")

        QMessageBox.critical(
            self,
            "Erro na conversão",
            message,
        )

    def select_input_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar arquivo",
            "",
            "Arquivos suportados (*.txt *.pdf);;Texto (*.txt);;PDF (*.pdf)",
        )

        if file_path:
            self.input_file_edit.setText(file_path)


def main() -> None:
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()