class BaseView(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setWindowIcon(get_app_icon())
        self.setup_base_styles()
        self.init_ui()
    
    def setup_base_styles(self):
        # 统一的基础样式
        pass
    
    def init_ui(self):
        # 子类重写
        raise NotImplementedError