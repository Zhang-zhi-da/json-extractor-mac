# -*- coding: utf-8 -*-
"""
JSON数据提取工具 - 支持粘贴JSON内容解析
现代化UI设计
"""

import json
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import platform

# macOS 没有 Microsoft YaHei / Consolas，这里做字体回退
FONT_UI = "PingFang SC" if platform.system() == "Darwin" else "Microsoft YaHei UI"
FONT_MONO = "Menlo" if platform.system() == "Darwin" else "Consolas"


class ModernUI:
    """自定义现代样式组件"""
    
    COLORS = {
        'primary': '#667EEA',
        'primary_dark': '#5A67D8',
        'success': '#48BB78',
        'danger': '#F56565',
        'warning': '#ED8936',
        'dark': '#2D3748',
        'gray': '#718096',
        'light': '#F7FAFC',
        'white': '#FFFFFF',
        'bg': '#EDF2F7',
        'input_bg': '#1A202C',
        'input_fg': '#E2E8F0',
    }
    
    @staticmethod
    def style_button(btn, color_type='primary'):
        colors = {
            'primary': (ModernUI.COLORS['primary'], ModernUI.COLORS['primary_dark']),
            'success': (ModernUI.COLORS['success'], '#38A169'),
            'danger': (ModernUI.COLORS['danger'], '#E53E3E'),
            'warning': (ModernUI.COLORS['warning'], '#DD6B20'),
            'gray': (ModernUI.COLORS['gray'], '#4A5568'),
        }
        bg, active_bg = colors.get(color_type, colors['primary'])
        
        btn.configure(
            font=(FONT_UI, 10, "bold"),
            bg=bg,
            fg=ModernUI.COLORS['white'],
            activebackground=active_bg,
            activeforeground=ModernUI.COLORS['white'],
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        btn.bind("<Enter>", lambda e: btn.configure(bg=active_bg))
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg))


class JsonExtractorUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("JSON 数据提取工具")
        self.window.geometry("1200x800")
        self.window.configure(bg=ModernUI.COLORS['bg'])
        
        # 设置窗口图标
        self.window.minsize(1000, 650)
        
        self.json_data = None
        self.df = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # ====== 顶部标题栏 ======
        header_frame = tk.Frame(self.window, bg=ModernUI.COLORS['primary'], height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # 标题内容
        header_inner = tk.Frame(header_frame, bg=ModernUI.COLORS['primary'])
        header_inner.pack(fill="both", expand=True, padx=30)
        
        tk.Label(
            header_inner, 
            text="JSON 数据提取工具", 
            font=(FONT_UI, 24, "bold"),
            fg=ModernUI.COLORS['white'], 
            bg=ModernUI.COLORS['primary']
        ).pack(side="left", anchor="center")
        
        tk.Label(
            header_inner, 
            text="rows + columns + values 数据拼接", 
            font=(FONT_UI, 11),
            fg="#CCDDEE", 
            bg=ModernUI.COLORS['primary']
        ).pack(side="left", anchor="center", padx=(20, 0))
        
        # ====== 主内容区 ======
        main_frame = tk.Frame(self.window, bg=ModernUI.COLORS['bg'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ====== JSON输入区 ======
        input_card = self.create_card(main_frame, "📋 JSON输入")
        
        # 输入说明
        tk.Label(
            input_card,
            text="粘贴JSON内容，工具将自动解析 rows 和 values 数据并进行列拼接",
            font=(FONT_UI, 9),
            fg=ModernUI.COLORS['gray'],
            bg=ModernUI.COLORS['white'],
            anchor="w"
        ).pack(fill="x", padx=15, pady=(12, 5))
        
        # 文本输入框
        text_container = tk.Frame(input_card, bg=ModernUI.COLORS['white'])
        text_container.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        
        self.json_text = tk.Text(
            text_container, 
            height=10, 
            font=(FONT_MONO, 11),
            bg=ModernUI.COLORS['input_bg'],
            fg=ModernUI.COLORS['input_fg'],
            insertbackground="#FFFFFF",
            relief="flat",
            wrap="none",
            bd=0,
            padx=15,
            pady=12,
            highlightthickness=0
        )
        self.json_text.pack(side="left", fill="both", expand=True)
        
        # 滚动条
        y_scroll = tk.Scrollbar(text_container, command=self.json_text.yview, bg=ModernUI.COLORS['dark'])
        y_scroll.pack(side="right", fill="y")
        self.json_text.config(yscrollcommand=y_scroll.set)
        
        x_scroll = tk.Scrollbar(self.window, orient="horizontal", command=self.json_text.xview)
        
        # 按钮区
        btn_frame = tk.Frame(input_card, bg=ModernUI.COLORS['white'])
        btn_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        # 解析按钮
        btn_parse = tk.Button(
            btn_frame, 
            text="🚀 解析JSON", 
            command=self.parse_json,
            width=12
        )
        ModernUI.style_button(btn_parse, 'primary')
        btn_parse.pack(side="left", padx=(0, 10))
        
        # 清空按钮
        btn_clear = tk.Button(
            btn_frame, 
            text="🗑️ 清空", 
            command=self.clear_text,
            width=10
        )
        ModernUI.style_button(btn_clear, 'gray')
        btn_clear.pack(side="left")
        
        # ====== 操作按钮区 ======
        action_card = self.create_card(main_frame, "📤 数据导出")
        
        action_inner = tk.Frame(action_card, bg=ModernUI.COLORS['white'])
        action_inner.pack(fill="x", padx=15, pady=15)
        
        # 导出Excel按钮
        btn_export = tk.Button(
            action_inner, 
            text="📊 导出Excel", 
            command=self.export_excel,
            width=12
        )
        ModernUI.style_button(btn_export, 'success')
        btn_export.pack(side="left", padx=(0, 10))
        
        # 复制按钮
        btn_copy = tk.Button(
            action_inner, 
            text="📋 复制数据", 
            command=self.copy_to_clipboard,
            width=12
        )
        ModernUI.style_button(btn_copy, 'warning')
        btn_copy.pack(side="left")
        
        tk.Label(
            action_inner,
            text="提示：导出的Excel文件可直接用Excel打开",
            font=(FONT_UI, 9),
            fg=ModernUI.COLORS['gray'],
            bg=ModernUI.COLORS['white']
        ).pack(side="left", padx=(20, 0))
        
        # ====== 数据预览区 ======
        preview_card = self.create_card(main_frame, "📋 数据预览")
        
        # 列信息标签
        info_frame = tk.Frame(preview_card, bg=ModernUI.COLORS['white'])
        info_frame.pack(fill="x", padx=15, pady=(12, 5))
        
        self.info_label = tk.Label(
            info_frame, 
            text="等待解析JSON数据...",
            font=(FONT_UI, 10, "bold"),
            fg=ModernUI.COLORS['dark'],
            bg=ModernUI.COLORS['white'],
            anchor="w"
        )
        self.info_label.pack(side="left")
        
        # 表格容器
        table_container = tk.Frame(preview_card, bg=ModernUI.COLORS['white'])
        table_container.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        
        # 创建表格
        tree_frame = tk.Frame(table_container)
        tree_frame.pack(fill="both", expand=True)
        
        y_scroll_tree = ttk.Scrollbar(tree_frame, orient="vertical")
        y_scroll_tree.pack(side="right", fill="y")
        
        x_scroll_tree = ttk.Scrollbar(tree_frame, orient="horizontal")
        x_scroll_tree.pack(side="bottom", fill="x")
        
        # 初始化表格列
        columns = ("#0",) + tuple([f"col{i}" for i in range(14)])
        self.tree = ttk.Treeview(
            tree_frame, 
            columns=columns, 
            show="tree headings",
            yscrollcommand=y_scroll_tree.set,
            xscrollcommand=x_scroll_tree.set,
            style="Custom.Treeview"
        )
        y_scroll_tree.config(command=self.tree.yview)
        x_scroll_tree.config(command=self.tree.xview)
        
        # 表格样式
        style = ttk.Style()
        style.configure("Custom.Treeview", font=(FONT_UI, 9))
        style.configure("Custom.Treeview.Heading", font=(FONT_UI, 9, "bold"))
        style.map("Custom.Treeview", background=[("selected", "#E2E8F0")])
        
        self.tree.column("#0", width=60, anchor="center", minwidth=50)
        self.tree.heading("#0", text="#")
        
        for i in range(14):
            col_id = f"col{i}"
            self.tree.column(col_id, width=120, anchor="center", minwidth=80)
            self.tree.heading(col_id, text=f"列{i+1}")
        
        self.tree.pack(fill="both", expand=True)
        
        # ====== 状态栏 ======
        status_frame = tk.Frame(self.window, bg=ModernUI.COLORS['dark'], height=40)
        status_frame.pack(fill="x", side="bottom")
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame, 
            text="✅ 就绪 - 请在上方粘贴JSON内容并点击「解析JSON」", 
            font=(FONT_UI, 10),
            fg=ModernUI.COLORS['white'],
            bg=ModernUI.COLORS['dark'],
            anchor="w",
            padx=20
        )
        self.status_label.pack(fill="x", anchor="center")
    
    def create_card(self, parent, title):
        """创建卡片容器"""
        card = tk.Frame(parent, bg=ModernUI.COLORS['bg'])
        card.pack(fill="x", pady=(0, 15))
        
        # 卡片内部白色区域
        inner = tk.Frame(card, bg=ModernUI.COLORS['white'], highlightbackground="#E2E8F0", highlightthickness=1)
        inner.pack(fill="x")
        
        # 卡片标题
        title_frame = tk.Frame(inner, bg=ModernUI.COLORS['white'])
        title_frame.pack(fill="x", padx=15, pady=(10, 0))
        
        tk.Label(
            title_frame,
            text=title,
            font=(FONT_UI, 11, "bold"),
            fg=ModernUI.COLORS['dark'],
            bg=ModernUI.COLORS['white']
        ).pack(side="left")
        
        return inner
    
    def clear_text(self):
        self.json_text.delete("1.0", "end")
        self.tree.delete(*self.tree.get_children())
        self.df = None
        self.info_label.config(text="等待解析JSON数据...", fg=ModernUI.COLORS['dark'])
        self.status_label.config(text="✅ 已清空", fg=ModernUI.COLORS['success'])
    
    def parse_json(self):
        json_str = self.json_text.get("1.0", "end").strip()
        
        if not json_str:
            messagebox.showwarning("提示", "请先粘贴JSON内容")
            return
        
        try:
            self.json_data = json.loads(json_str)
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON解析错误", f"JSON格式错误:\n{str(e)}\n\n请检查JSON语法是否正确")
            return
        
        self.parse_and_display()
    
    def parse_and_display(self):
        if not self.json_data:
            return
        
        rows = self.json_data.get("rows", [])
        columns = self.json_data.get("columns", [])
        values = self.json_data.get("values", [])
        
        if not rows:
            messagebox.showwarning("提示", "JSON中未找到rows数据")
            return
        
        # 提取列名（从columns）
        col_names = []
        for col in columns:
            if col.get("cells") and len(col["cells"]) > 0:
                cell = col["cells"][0]
                col_names.append(str(cell.get("value", f"指标{len(col_names)+1}")))
        
        # 如果没有columns，使用默认值
        if not col_names:
            col_names = [f"指标{i+1}" for i in range(7)]
        
        # 提取行数据
        all_data = []
        for idx, row in enumerate(rows):
            cells = row.get("cells", [])
            row_values = [str(cell.get("value", "")) for cell in cells]
            
            # 拼接values中的数值数据
            if idx < len(values):
                val_row = values[idx]
                num_values = [str(v.get("v", "")) for v in val_row]
            else:
                num_values = [""] * len(col_names)
            
            all_data.append(row_values + num_values)
        
        # 生成列名
        max_cols = max(len(row) for row in all_data) if all_data else 14
        row_labels = [f"字段{i+1}" for i in range(max(0, max_cols - len(col_names)))]
        all_columns = row_labels + col_names
        
        # 创建DataFrame
        self.df = pd.DataFrame(all_data)
        
        # 调整列名
        if len(self.df.columns) > len(all_columns):
            extra_cols = [f"额外{i+1}" for i in range(len(self.df.columns) - len(all_columns))]
            all_columns = extra_cols + all_columns
        
        # 确保列数一致
        if len(self.df.columns) != len(all_columns):
            if len(self.df.columns) < len(all_columns):
                for i in range(len(self.df.columns), len(all_columns)):
                    self.df[i] = ""
            else:
                self.df = self.df.iloc[:, :len(all_columns)]
        
        self.df.columns = all_columns[:len(self.df.columns)]
        
        # 更新表格
        num_cols = len(self.df.columns)
        
        # 重新配置列
        self.tree["columns"] = ("#0",) + tuple([f"col{i}" for i in range(num_cols)])
        self.tree.heading("#0", text="#")
        self.tree.column("#0", width=50, anchor="center")
        
        for i, col_name in enumerate(self.df.columns):
            col_id = f"col{i}"
            self.tree.heading(col_id, text=str(col_name))
            self.tree.column(col_id, width=130, anchor="center")
        
        # 清除旧数据
        self.tree.delete(*self.tree.get_children())
        
        # 插入数据
        for row_idx, row_data in self.df.iterrows():
            values_list = [str(row_idx + 1)] + [str(v) if pd.notna(v) else "" for v in row_data]
            self.tree.insert("", "end", text=str(row_idx + 1), values=values_list)
        
        self.info_label.config(
            text=f"✅ 解析完成 - 共 {len(self.df)} 行 × {len(self.df.columns)} 列 | rows数据({len(row_labels)}列) + 指标({len(col_names)}列)",
            fg=ModernUI.COLORS['success']
        )
        self.status_label.config(
            text=f"✅ 解析成功 - {len(self.df)}行数据已加载 | 可导出Excel或复制数据",
            fg=ModernUI.COLORS['success']
        )
    
    def export_excel(self):
        if self.df is None or self.df.empty:
            messagebox.showwarning("提示", "请先解析JSON数据")
            return
        
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(
            title="导出Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")],
            initialfile="json_export"
        )
        
        if file_path:
            try:
                self.df.to_excel(file_path, index=False, engine='openpyxl')
                messagebox.showinfo("成功", f"✅ 已导出到:\n{file_path}")
                self.status_label.config(text=f"✅ 已导出: {file_path.split('/')[-1]}", fg=ModernUI.COLORS['success'])
            except Exception as e:
                messagebox.showerror("错误", f"导出失败:\n{str(e)}")
    
    def copy_to_clipboard(self):
        if self.df is None or self.df.empty:
            messagebox.showwarning("提示", "请先解析JSON数据")
            return
        
        try:
            clipboard_data = self.df.to_csv(sep='\t', index=False)
            self.window.clipboard_clear()
            self.window.clipboard_append(clipboard_data)
            messagebox.showinfo("成功", "✅ 表格数据已复制到剪贴板\n可使用 Ctrl+V 粘贴到Excel")
            self.status_label.config(text="✅ 数据已复制到剪贴板", fg=ModernUI.COLORS['success'])
        except Exception as e:
            messagebox.showerror("错误", f"复制失败:\n{str(e)}")
    
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = JsonExtractorUI()
    app.run()
