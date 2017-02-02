#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from main_window_ui import Ui_MainWindow


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)
    quit()

import sys
sys.excepthook = log_uncaught_exceptions


def search_manga_on_readmanga(query_text, sort=True):
    import requests
    rs = requests.get('http://readmanga.me/search/suggestion?query=' + query_text)

    search_result_list = rs.json()['suggestions']

    # Фильтрация ссылок: удаление тех, что ведут на авторов
    manga_list = list(filter(lambda item: '/list/person/' not in item['data']['link'], search_result_list))

    # Относительные ссылки на главы делаем абсолютными
    for manga_obj in manga_list:
        rel_url = manga_obj['data']['link']

        from urllib.parse import urljoin
        url = urljoin(rs.url, rel_url)

        manga_obj['data']['link'] = url

    if sort:
        manga_list.sort(key=lambda item: item['value'])

    return manga_list


def get_url_images_from_chapter(html_chapter):
    """
    Функция для вытаскивания ссылок на страницы (картинки) главы.

    """

    # Пример данных: rm_h.init( [['auto/09/79','http://e5.postfact.ru/',"/80/1.jpg_res.jpg",690,21869],['auto/09/79','http://e2.postfact.ru/',"/80/2.jpg_res.jpg",690,19560]], 0, false);
    # То, что в квадратных скобках в init можно распарсить как JSON, осталось регуляркой это вытащить
    re_expr = r'init\(.*(\[\[.+\]\]).*\)'

    import re
    match = re.search(re_expr, html_chapter)
    if match:
        json_text = match.group(1)

        # Замена одинарных кавычек на двойные
        json_text = json_text.replace("'", '"')

        import json
        json_data = json.loads(json_text)

        from urllib.parse import urljoin
        return [urljoin(data_url[1], data_url[0] + data_url[2]) for data_url in json_data]

    raise Exception('Не получилось из страницы вытащить список картинок главы. '
                    'Используемое регулярное выражение: ', re_expr)


class ImageViewer(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)

        self._image = None

    def set_image(self, image):
        self._image = image

        self._update_image()

    def _update_image(self):
        pix = QPixmap.fromImage(self.scaled_image())
        self.setPixmap(pix)

    def scaled_image(self):
        img = self._image.copy()

        # Следим чтобы по ширине изображение корректировалось под ширину виджета
        if self.width() < self._image.width():
            img = self._image.scaledToWidth(self.width(), Qt.SmoothTransformation)

        return img

    def resizeEvent(self, *args, **kwargs):
        if self._image:
            self._update_image()

        super().resizeEvent(*args, **kwargs)


class MainWindow(QMainWindow):
    ROLE_MANGA_OBJ = Qt.UserRole
    ROLE_MANGA_URL = Qt.UserRole + 1
    ROLE_MANGA_TITLE = Qt.UserRole + 2

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # NOTE: методом подбора получились эти значения
        self.ui.splitter_main.setSizes([80, 500])

        self.setWindowTitle('Client http://readmanga.me')

        self.ui.line_edit_search.textEdited.connect(self.on_manga_search)
        self.ui.list_widget_search_result.itemDoubleClicked.connect(self.on_search_item_double_clicked)

        self.ui.push_button_next_page.clicked.connect(self.next_page)
        self.ui.push_button_prev_page.clicked.connect(self.prev_page)

        self.ui.combo_box_manga_chapters.currentIndexChanged.connect(self.on_manga_chapters_current_index_changed)
        self.ui.combo_box_pages.currentIndexChanged.connect(self.set_chapter_page)

        self.url_images_chapter = list()

        # Кэш страниц манги, чтобы не качать их каждый раз при смене страницы на просмотренную в главе
        self.cache_page_chapter_by_image = dict()

        self.last_item_chapter = None
        self.last_page_number = -1

        self.image_viewer = ImageViewer()
        self.ui.scroll_area_image_page.setWidget(self.image_viewer)

        self.ui.scroll_area_image_page.setWidgetResizable(True)
        self.ui.scroll_area_image_page.installEventFilter(self)

        self.download_progress_bar = QProgressBar()
        self.download_progress_bar.hide()
        self.ui.statusbar.addPermanentWidget(self.download_progress_bar)

        self._update_states()

    def _clear_states(self):
        self.last_page_number = -1
        self.last_item_chapter = None
        self.url_images_chapter.clear()
        self.cache_page_chapter_by_image.clear()
        self.ui.combo_box_manga_chapters.clear()
        self.ui.combo_box_pages.clear()
        self.image_viewer.clear()
        self._update_states()

    def _update_states(self):
        pages = self.ui.combo_box_pages.count()
        current_page = self.ui.combo_box_pages.currentIndex()

        self.ui.push_button_next_page.setEnabled(current_page < pages - 1)
        self.ui.push_button_prev_page.setEnabled(current_page > 0)

    def on_manga_search(self, query_text):
        self.ui.list_widget_search_result.clear()

        manga_list = search_manga_on_readmanga(query_text)

        for manga_obj in manga_list:
            data = manga_obj['data']

            # Думаю, у любой манги найдется автор, иначе игнорируем
            if 'authors' not in data:
                continue

            text = manga_obj['value']

            another_names = data['names']
            if another_names:
                text += " | " + ', '.join(another_names)

            authors = data['authors']
            if authors:
                text += " (" + authors + ")"

            url = data['link']

            item = QListWidgetItem(text)
            item.setData(self.ROLE_MANGA_OBJ, manga_obj)
            item.setData(self.ROLE_MANGA_URL, url)
            item.setData(self.ROLE_MANGA_TITLE, text)

            self.ui.list_widget_search_result.addItem(item)

    def next_page(self):
        current_index = self.ui.combo_box_pages.currentIndex()

        if current_index < self.ui.combo_box_pages.maxCount():
            self.ui.combo_box_pages.setCurrentIndex(current_index + 1)

        self._update_states()

    def prev_page(self):
        current_index = self.ui.combo_box_pages.currentIndex()

        if current_index > 0:
            self.ui.combo_box_pages.setCurrentIndex(current_index - 1)

        self._update_states()

    def on_manga_chapters_current_index_changed(self, index):
        if not self.ui.combo_box_manga_chapters.count():
            return

        url = self.ui.combo_box_manga_chapters.itemData(index)
        self.fill_chapter_viewer(url)

    def on_search_item_double_clicked(self, item):
        # Чтобы нельзя было выбрать повторно мангу
        if item == self.last_item_chapter:
            return

        self.last_item_chapter = item

        self._clear_states()

        url = item.data(self.ROLE_MANGA_URL)
        title = item.data(self.ROLE_MANGA_TITLE)

        content_as_bytes = self._download_by_url(url)

        from bs4 import BeautifulSoup
        root = BeautifulSoup(content_as_bytes, 'lxml')

        description = root.select_one('.manga-description').text.strip()

        # Удаление множества подряд идущих пробелов
        import re
        description = re.sub(r'\s{2,}', ' ', description)

        self.ui.label_manga_name.setText(title)
        self.ui.text_edit_description.setText(description)

        url_first_chapter = root.select_one('.read-first > a[href]')
        if not url_first_chapter:
            QMessageBox.information(self, "Внимание", "Похоже у манги нет глав")
            return

        url_first_chapter = url_first_chapter['href']

        from urllib.parse import urljoin
        url_first_chapter = urljoin(url, url_first_chapter)

        self.fill_chapter_viewer(url_first_chapter)

    def fill_chapter_viewer(self, url_chapter):
        self._clear_states()

        # Загрузка первой главы для получения списка глав и показа первой страницы главы
        content_as_bytes = self._download_by_url(url_chapter)

        from bs4 import BeautifulSoup
        root = BeautifulSoup(content_as_bytes, 'lxml')

        from urllib.parse import urljoin
        chapter_list = [(option.text.strip(), urljoin(url_chapter, option['value'])) for option in
                        root.select('#chapterSelectorSelect > option')]

        # Чтобы напрасно не вызывался сигнал currentIndexChanged при настройке комбобокса
        self.ui.combo_box_manga_chapters.blockSignals(True)

        # Заполнение списка глав
        for title_chapter, _url_chapter in chapter_list:
            self.ui.combo_box_manga_chapters.addItem(title_chapter, _url_chapter)

        # Выбор текущей главы в комбобоксе
        index = -1

        for i in range(self.ui.combo_box_manga_chapters.count()):
            item_url = self.ui.combo_box_manga_chapters.itemData(i)
            if item_url.startswith(url_chapter):
                index = i
                break

        self.ui.combo_box_manga_chapters.setCurrentIndex(index)
        self.ui.combo_box_manga_chapters.blockSignals(False)

        # Для получения ссылок на картинки глав:
        html = str(root)
        self.url_images_chapter = get_url_images_from_chapter(html)

        # Заполнение списка с страницами главы
        self.ui.combo_box_pages.blockSignals(True)
        for i in range(len(self.url_images_chapter)):
            self.ui.combo_box_pages.addItem(str(i + 1))

        self.ui.combo_box_pages.blockSignals(False)

        current_page = self.ui.combo_box_pages.currentIndex()
        self.set_chapter_page(current_page)

        self._update_states()

    def _download_by_url(self, url):
        import requests
        rs = requests.get(url, stream=True)

        self.download_progress_bar.show()

        if 'Content-Length' in rs.headers:
            img_size = int(rs.headers['Content-Length'])
            self.download_progress_bar.setMaximum(img_size)
        else:
            # Прогресс бар становится бесконечным
            self.download_progress_bar.setMaximum(0)

        size = 0

        byte_array_img = bytearray()

        for buf in rs.iter_content(1024):
            if buf:
                byte_array_img += buf
                size += len(buf)

                self.download_progress_bar.setValue(size)

        self.download_progress_bar.hide()

        return bytes(byte_array_img)

    def set_chapter_page(self, page_number):
        if page_number == -1 or page_number == self.last_page_number:
            return

        self.last_page_number = page_number

        # Возврат ползунка на положенное место
        self.ui.scroll_area_image_page.verticalScrollBar().setValue(0)

        if page_number not in self.cache_page_chapter_by_image:
            url_first_page = self.url_images_chapter[page_number]

            content_as_bytes = self._download_by_url(url_first_page)
            img = QImage.fromData(content_as_bytes)

            self.cache_page_chapter_by_image[page_number] = img

        else:
            img = self.cache_page_chapter_by_image[page_number]

        self.image_viewer.set_image(img)

        self._update_states()

    def eventFilter(self, obj, event):
        # Для изменения ширины картинки
        if obj == self.ui.scroll_area_image_page and event.type() == QEvent.Resize:
            # Чтобы был небольшой отступ по краям
            margin = 40
            self.image_viewer.setFixedWidth(self.ui.scroll_area_image_page.width() - margin)

        return super().eventFilter(obj, event)


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.show()
    mw.resize(1400, 800)

    # Move window on center
    rect = mw.frameGeometry()
    rect.moveCenter(QDesktopWidget().availableGeometry().center())
    mw.move(rect.topLeft())

    app.exec()
