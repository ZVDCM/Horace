from Admin.Misc.Functions.is_blank import is_blank
from PyQt5 import QtCore


class Get(QtCore.QThread):
    operation = QtCore.pyqtSignal(object)

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = ()

    def run(self):
        res = self.fn(*self.val)
        self.operation.emit(res)
        self.quit()


class Operation(QtCore.QThread):
    operation = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(str)

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = ()

    def run(self):
        res = self.fn(*self.val)
        if res == 'successful':
            self.operation.emit()
        else:
            self.error.emit(res)
        self.quit()


class BlacklistURL:

    def __init__(self, Model, View, Contoller):
        self.Model = Model
        self.View = View
        self.Contoller = Contoller

        self.target_url_row = None
        self.TargetUrl = None

        self.connect_signals()


    def connect_signals(self):
        self.View.lv_url.clicked.connect(self.list_url_clicked)
        self.View.btn_init_add_url.clicked.connect(self.init_add_url)
        self.View.btn_init_edit_url.clicked.connect(self.init_edit_url)
        self.View.btn_add_edit_url.clicked.connect(
            self.init_add_edit_url)
        self.View.btn_cancel_url.clicked.connect(self.cancel_url)
        self.View.btn_delete_url.clicked.connect(self.init_delete_url)

        self.View.txt_url.returnPressed.connect(self.set_url)
        self.View.web_viewer.loadStarted.connect(self.View.URLViewerLoadingScreen.run)
        self.View.web_viewer.loadFinished.connect(self.View.URLViewerLoadingScreen.hide)

        self.View.btn_clear_url_table.clicked.connect(self.init_clear_url_table)

        self.View.txt_search_url.returnPressed.connect(self.search_url)
        self.View.btn_search_url.clicked.connect(self.search_url)

    def search_url(self):
        target_url = self.View.txt_search_url.text()
        if target_url.lower() == "null":
            return
        url_model = self.View.lv_url.model()
        urls = url_model.data
        target_indices = []
        for index, url in enumerate(urls):
            if target_url in url:
                target_indices.append(index)
            self.View.lv_url.setRowHidden(index, True)

        for target_index in target_indices:
            self.View.lv_url.setRowHidden(target_index, False)

        self.View.txt_search_url.clear()

    def set_url(self):
        domain = f'https://{self.View.txt_url.text()}'
        self.View.web_viewer.setUrl(QtCore.QUrl(domain))

    # Operations
    def GetAllURL(self):
        handler = Get(self.Model.get_all_url)
        handler.started.connect(self.View.URLSLoadingScreen.run)
        handler.operation.connect(self.set_url_list)
        handler.finished.connect(self.View.URLSLoadingScreen.hide)
        return handler

    def AddURL(self):
        handler = Operation(self.Model.create_url)
        handler.started.connect(self.View.URLLoadingScreen.run)
        handler.error.connect(self.url_error)
        handler.finished.connect(self.View.URLLoadingScreen.hide)
        handler.finished.connect(self.View.btn_cancel_url.click)
        return handler

    def EditURL(self):
        handler = Operation(self.Model.edit_url)
        handler.started.connect(self.View.URLLoadingScreen.run)
        handler.error.connect(self.url_error)
        handler.finished.connect(self.View.URLLoadingScreen.hide)
        handler.finished.connect(self.View.btn_cancel_url.click)
        return handler

    def DeleteURL(self):
        handler = Operation(self.Model.delete_url)
        handler.started.connect(self.View.URLLoadingScreen.run)
        handler.finished.connect(self.View.URLLoadingScreen.hide)
        return handler

    def TruncateTable(self):
        handler = Operation(self.Model.truncate_url_table)
        handler.started.connect(self.View.URLSLoadingScreen.run)
        handler.finished.connect(self.View.URLSLoadingScreen.hide)
        return handler

    # List
    def list_url_clicked(self, index):
        row = index.row()
        self.set_target_url(self.Model.Url(
            None, self.View.lv_url.model().getRowData(row)))

    def set_target_url(self, Url):
        self.TargetUrl = Url
        self.select_target_url_row()

    def select_target_url_row(self):
        try:
            url_model = self.View.lv_url.model()
            self.target_url_row = url_model.findRow(
                self.TargetUrl.Domain)
            index = url_model.createIndex(self.target_url_row, 0)
            self.View.lv_url.setCurrentIndex(index)
            self.View.lv_url.setFocus(True)
            self.set_url_inputs()
        except AttributeError:
            return
        except TypeError:
            return

    def set_url_inputs(self):
        self.View.txt_url.setText(self.TargetUrl.Domain)
        self.View.web_viewer.setUrl(QtCore.QUrl(f'https://{self.TargetUrl.Domain}'))

    def set_url_list(self, urls):
        if not urls:
            self.View.web_viewer.setUrl(QtCore.QUrl("https://www.google.com"))
            self.View.disable_url_edit_delete()
            self.View.btn_clear_url_table.setDisabled(True)
            self.View.lbl_url_status.setText("URL: 0")
        else:
            self.View.enable_url_edit_delete()
            self.View.btn_clear_url_table.setDisabled(False)

        url_model = self.Model.ListModel(
            self.View.lv_url, urls)
        self.View.lv_url.setModel(url_model)
        self.View.lbl_url_status.setText(f"URL: {len(urls)}")

    def empty_url_list(self):
        try:
            if self.View.lv_url.model().rowCount() != 0:
                self.View.lv_url.model().removeRows(
                    0, self.View.lv_url.model().rowCount())
        except AttributeError:
            return

    def select_latest_url(self, domain):
        url_model = self.View.lv_url.model()
        self.set_target_url(self.Model.Url(
            None, url_model.getRowData(url_model.findRow(domain))))

    def get_latest_url(self):
        try:
            class_model = self.View.lv_url.model()
            self.set_target_url(self.Model.Url(
                None, class_model.getRowData(0)))
        except IndexError:
            self.View.clear_url_inputs()

    # Buttons
    def init_add_url(self):
        self.View.clear_url_inputs()
        self.View.disable_url_buttons()
        self.View.enable_url_inputs()
        self.View.set_url('Add')

    def init_edit_url(self):
        self.View.disable_url_buttons()
        self.View.enable_url_inputs()
        self.View.set_url('Edit')

    def cancel_url(self):
        self.View.clear_url_inputs()
        self.select_target_url_row()
        self.View.enable_url_buttons()
        self.View.disable_url_inputs()
        self.View.set_url('Read')

    def init_add_edit_url(self):
        if self.View.url_state == "Add":
            self.add_url()
        elif self.View.url_state == "Edit":
            self.edit_url()

    # URL Error
    def url_error(self, error):
        if error == 'exists':
            self.View.run_popup(f'URL exists')

    # URL Add
    def add_url(self):
        domain = self.View.txt_url.text()
        if is_blank(domain):
            self.View.run_popup(f'URL fields must be filled')
            return

        self.get_all_url_handler = self.GetAllURL()
        self.add_url_handler = self.AddURL()
        
        self.add_url_handler.val = domain,
        self.add_url_handler.operation.connect(self.get_all_url_handler.start)

        self.get_all_url_handler.finished.connect(lambda: self.select_latest_url(domain))
        self.add_url_handler.start()

    # URL Edit
    def edit_url(self):
        domain = self.View.txt_url.text()
        if is_blank(domain):
            self.View.run_popup(f'URL fields must be filled')
            return

        if domain == self.TargetUrl.Domain:
            self.View.btn_cancel_url.click()
            return

        self.get_all_url_handler = self.GetAllURL()
        self.edit_url_handler = self.EditURL()
        
        self.edit_url_handler.val = self.TargetUrl.Domain, domain
        self.edit_url_handler.operation.connect(self.get_all_url_handler.start)

        self.get_all_url_handler.finished.connect(lambda: self.select_latest_url(domain))
        self.edit_url_handler.start()

    def init_delete_url(self):
        self.View.show_confirm(self.delete_url)

    # URL Delete
    def delete_url(self):
        self.get_all_url_handler = self.GetAllURL()
        self.delete_url_handler = self.DeleteURL()

        self.delete_url_handler.val = self.TargetUrl,
        self.delete_url_handler.operation.connect(self.get_all_url_handler.start)

        self.get_all_url_handler.finished.connect(self.get_latest_url)
        self.delete_url_handler.start()

    def init_clear_url_table(self):
        self.View.show_confirm(self.clear_url_table, "Are you sure you want to remove everything?")

    def clear_url_table(self):
        self.get_all_url_handler = self.GetAllURL()
        self.truncate_url_handler = self.TruncateTable()
        self.truncate_url_handler.operation.connect(self.get_all_url_handler.start)
        self.get_all_url_handler.finished.connect(lambda: self.View.web_viewer.setUrl(QtCore.QUrl("https://www.google.com")))
        self.get_all_url_handler.finished.connect(self.get_latest_url)
        self.truncate_url_handler.start()
