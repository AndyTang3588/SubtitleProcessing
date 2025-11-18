# -*- coding: utf-8 -*-

# 语言字典
LANG_DATA = {
    "zh": {
        "WINDOW_TITLE": "字幕处理工具集 Launcher",
        "SELECT_FILE": "选择输入文件:",
        "BTN_BROWSE": "浏览",
        "BTN_SETTINGS": "设置",
        "CHECK_OUTPUT": "输出至原目录",
        "BTN_GENERATE": "生成转换结果",
        "STATUS_WAIT": "等待",
        "STATUS_RUNNING": "运行中...",
        "STATUS_SUCCESS": "成功",
        "STATUS_WAIT_RESULT": "等待生成结果",
        
        # 分组标题
        "GROUP_PREPROCESS": "输入预处理",
        "GROUP_REFINE": "文字内容精细处理",
        "GROUP_OUTPUT": "输出处理",
        
        # 卡片标题
        "CARD_A1": "A1 - 输入转字幕",
        "CARD_A2": "A2 - 去重处理",
        "CARD_A3": "A3 - 时间调整",
        "CARD_B1": "B1 - AI翻译（计划中）",
        "CARD_C1": "C1 - 格式转换",
        "CARD_C2": "C2 - 多语言字幕（计划中）",
        
        # 内部标签
        "LABEL_VERSION": "选择版本:",
        "LABEL_DELAY": "延时(毫秒):",
        "BTN_RUN": "运行",
        "LABEL_PLANNED": "功能开发中...",
        "BTN_PLACEHOLDER": "占位按钮",
        
        # StepA1 相关
        "MSG_SELECT_FILE": "请选择输入文件",
        "MSG_USE_JSON2MIDFORM": "将使用 1json2midform.py",
        "MSG_FORMAT_NOT_SUPPORTED": "暂不支持该格式",
        
        # 消息框
        "MSG_WARNING": "警告",
        "MSG_PLEASE_SELECT_FILE": "请先选择输入文件",
        "MSG_SUCCESS": "成功",
        "MSG_SETTINGS_SAVED": "设置已保存",
        "MSG_GENERATED_FILES": "成功生成 {count} 个文件",
        
        # 文件对话框
        "DIALOG_SELECT_FILE": "选择字幕文件",
        "DIALOG_FILE_TYPES_TEXT": "文本文件",
        "DIALOG_FILE_TYPES_JSON": "JSON 文件",
        "DIALOG_FILE_TYPES_ALL": "所有文件",
        
        # 设置窗口
        "SETTINGS_TITLE": "设置",
        "SETTINGS_SAVE": "保存",
        "SETTINGS_CHATGPT_API": "ChatGPT API:",
        "SETTINGS_GROQ_API": "Groq Platform API:",
        
        # B1 和 C2 相关
        "LABEL_AI_TRANSLATE": "自动翻译字幕（计划中）",
        "BTN_START_TRANSLATE": "开始翻译（占位）",
        "LABEL_MULTILANG": "设置为指定语言字幕(更改文件名后缀)（计划中）",
        "BTN_START_PROCESS": "开始处理（占位）",
    },
    "en": {
        "WINDOW_TITLE": "Subtitle Toolkit Launcher",
        "SELECT_FILE": "Input File:",
        "BTN_BROWSE": "Browse",
        "BTN_SETTINGS": "Settings",
        "CHECK_OUTPUT": "Output to source dir",
        "BTN_GENERATE": "Generate Result",
        "STATUS_WAIT": "Waiting",
        "STATUS_RUNNING": "Running...",
        "STATUS_SUCCESS": "Success",
        "STATUS_WAIT_RESULT": "Waiting for result",
        
        # Groups
        "GROUP_PREPROCESS": "Preprocessing",
        "GROUP_REFINE": "Content Refinement",
        "GROUP_OUTPUT": "Output Processing",
        
        # Cards
        "CARD_A1": "A1 - Input to Sub",
        "CARD_A2": "A2 - Dedup",
        "CARD_A3": "A3 - Time Shift",
        "CARD_B1": "B1 - AI Trans (Planned)",
        "CARD_C1": "C1 - Format Convert",
        "CARD_C2": "C2 - Multi-lang (Planned)",
        
        # Inner
        "LABEL_VERSION": "Version:",
        "LABEL_DELAY": "Delay (ms):",
        "BTN_RUN": "Run",
        "LABEL_PLANNED": "Under Dev...",
        "BTN_PLACEHOLDER": "Placeholder",
        
        # StepA1 related
        "MSG_SELECT_FILE": "Please select input file",
        "MSG_USE_JSON2MIDFORM": "Will use 1json2midform.py",
        "MSG_FORMAT_NOT_SUPPORTED": "Format not supported",
        
        # Message boxes
        "MSG_WARNING": "Warning",
        "MSG_PLEASE_SELECT_FILE": "Please select input file first",
        "MSG_SUCCESS": "Success",
        "MSG_SETTINGS_SAVED": "Settings saved",
        "MSG_GENERATED_FILES": "Successfully generated {count} files",
        
        # File dialogs
        "DIALOG_SELECT_FILE": "Select subtitle file",
        "DIALOG_FILE_TYPES_TEXT": "Text files",
        "DIALOG_FILE_TYPES_JSON": "JSON files",
        "DIALOG_FILE_TYPES_ALL": "All files",
        
        # Settings window
        "SETTINGS_TITLE": "Settings",
        "SETTINGS_SAVE": "Save",
        "SETTINGS_CHATGPT_API": "ChatGPT API:",
        "SETTINGS_GROQ_API": "Groq Platform API:",
        
        # B1 and C2 related
        "LABEL_AI_TRANSLATE": "Auto translate subtitles (Planned)",
        "BTN_START_TRANSLATE": "Start translate (Placeholder)",
        "LABEL_MULTILANG": "Set as specified language subtitle (Change file suffix) (Planned)",
        "BTN_START_PROCESS": "Start process (Placeholder)",
    },
    "fr": {
        "WINDOW_TITLE": "Lanceur de l'outil de sous-titres",
        "SELECT_FILE": "Fichier d'entrée :",
        "BTN_BROWSE": "Parcourir",
        "BTN_SETTINGS": "Paramètres",
        "CHECK_OUTPUT": "Exporter vers le dossier source",
        "BTN_GENERATE": "Générer le résultat",
        "STATUS_WAIT": "En attente",
        "STATUS_RUNNING": "En cours...",
        "STATUS_SUCCESS": "Succès",
        "STATUS_WAIT_RESULT": "En attente du résultat",
        
        # Groupes
        "GROUP_PREPROCESS": "Prétraitement",
        "GROUP_REFINE": "Affinage du contenu",
        "GROUP_OUTPUT": "Traitement de sortie",
        
        # Cartes
        "CARD_A1": "A1 - Entrée vers sous-titres",
        "CARD_A2": "A2 - Déduplication",
        "CARD_A3": "A3 - Décalage temporel",
        "CARD_B1": "B1 - Traduction IA (prévu)",
        "CARD_C1": "C1 - Conversion de format",
        "CARD_C2": "C2 - Sous-titres multilingues (prévu)",
        
        # Interne
        "LABEL_VERSION": "Version :",
        "LABEL_DELAY": "Décalage (ms) :",
        "BTN_RUN": "Exécuter",
        "LABEL_PLANNED": "En développement...",
        "BTN_PLACEHOLDER": "Bouton factice",
        
        # StepA1
        "MSG_SELECT_FILE": "Veuillez sélectionner un fichier",
        "MSG_USE_JSON2MIDFORM": "Utilisera 1json2midform.py",
        "MSG_FORMAT_NOT_SUPPORTED": "Format non pris en charge",
        
        # Boîtes de dialogue
        "MSG_WARNING": "Avertissement",
        "MSG_PLEASE_SELECT_FILE": "Veuillez d'abord sélectionner un fichier",
        "MSG_SUCCESS": "Succès",
        "MSG_SETTINGS_SAVED": "Paramètres enregistrés",
        "MSG_GENERATED_FILES": "Généré {count} fichier(s)",
        
        # Dialogue de fichiers
        "DIALOG_SELECT_FILE": "Choisir un fichier de sous-titres",
        "DIALOG_FILE_TYPES_TEXT": "Fichiers texte",
        "DIALOG_FILE_TYPES_JSON": "Fichiers JSON",
        "DIALOG_FILE_TYPES_ALL": "Tous les fichiers",
        
        # Fenêtre des paramètres
        "SETTINGS_TITLE": "Paramètres",
        "SETTINGS_SAVE": "Enregistrer",
        "SETTINGS_CHATGPT_API": "API ChatGPT :",
        "SETTINGS_GROQ_API": "API Groq Platform :",
        
        # B1 et C2
        "LABEL_AI_TRANSLATE": "Traduction automatique des sous-titres (prévu)",
        "BTN_START_TRANSLATE": "Lancer la traduction (factice)",
        "LABEL_MULTILANG": "Définir comme sous-titres d'une langue donnée (change l'extension) (prévu)",
        "BTN_START_PROCESS": "Lancer le traitement (factice)",
    }
}
