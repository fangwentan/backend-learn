import json
import os
books = []  # 用列表存储所有图书信息
data_file = "books.json"  # 数据文件路径

def load_books():
    """程序启动时从文件读取图书信息"""
    global books
    if os.path.exists(data_file):
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                books = json.load(f)
        except json.JSONDecodeError:
            print("数据文件损坏，将创建新的图书列表")
            books = []
    else:
        books = []

def save_books():
    """保存图书信息到文件"""
    try:
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"保存失败：{e}")
        return False

# ---------------------- 功能模块函数 ----------------------
def add_book():
    """添加图书信息"""
    print("\n===== 添加图书 =====")
    # 1. 输入图书编号，检查重复
    while True:
        book_id = input("请输入图书编号（字符串）：").strip()
        if not book_id:
            print("编号不能为空！")
            continue
        # 检查是否重复
        exists = any(book["id"] == book_id for book in books)
        if exists:
            print("该编号已存在，请重新输入！")
        else:
            break

    # 2. 输入书名
    while True:
        title = input("请输入书名：").strip()
        if title:
            break
        print("书名不能为空！")

    # 3. 输入作者
    while True:
        author = input("请输入作者：").strip()
        if author:
            break
        print("作者不能为空！")

    # 4. 输入数量（整数）
    while True:
        count_str = input("请输入数量（整数）：").strip()
        try:
            count = int(count_str)
            if count < 0:
                print("数量不能为负数！")
                continue
            break
        except ValueError:
            print("输入格式错误，请输入整数！")

    # 5. 添加到列表
    new_book = {
        "id": book_id,
        "title": title,
        "author": author,
        "count": count
    }
    books.append(new_book)
    print("图书添加成功！")

def show_all_books():
    """查看所有图书"""
    print("\n===== 所有图书 =====")
    if not books:
        print("暂无图书信息")
        return
    # 格式化输出
    print(f"{'编号':<10}{'书名':<20}{'作者':<15}{'数量':<5}")
    print("-" * 50)
    for book in books:
        print(f"{book['id']:<10}{book['title']:<20}{book['author']:<15}{book['count']:<5}")

def search_book():
    """查询图书（按编号或书名）"""
    print("\n===== 查询图书 =====")
    keyword = input("请输入图书编号或书名关键词：").strip()
    if not keyword:
        print("关键词不能为空！")
        return

    results = []
    for book in books:
        if keyword in book["id"] or keyword in book["title"]:
            results.append(book)

    if not results:
        print("未找到匹配的图书")
        return

    print(f"{'编号':<10}{'书名':<20}{'作者':<15}{'数量':<5}")
    print("-" * 50)
    for book in results:
        print(f"{book['id']:<10}{book['title']:<20}{book['author']:<15}{book['count']:<5}")

def update_book_count():
    """修改图书数量"""
    print("\n===== 修改图书数量 =====")
    book_id = input("请输入要修改的图书编号：").strip()
    if not book_id:
        print("编号不能为空！")
        return

    # 查找图书
    target_book = None
    for book in books:
        if book["id"] == book_id:
            target_book = book
            break
    if not target_book:
        print("未找到该编号的图书")
        return

    # 输入新数量
    while True:
        count_str = input("请输入新的数量（整数）：").strip()
        try:
            new_count = int(count_str)
            if new_count < 0:
                print("数量不能为负数！")
                continue
            break
        except ValueError:
            print("输入格式错误，请输入整数！")

    target_book["count"] = new_count
    print("数量修改成功！")

def delete_book():
    """删除图书"""
    print("\n===== 删除图书 =====")
    book_id = input("请输入要删除的图书编号：").strip()
    if not book_id:
        print("编号不能为空！")
        return

    global books
    original_len = len(books)
    # 过滤掉要删除的图书
    books = [book for book in books if book["id"] != book_id]

    if len(books) == original_len:
        print("未找到该编号的图书")
    else:
        print("图书删除成功！")

# ---------------------- 菜单交互主程序 ----------------------
def main_menu():
    print("\n===== 图书管理系统 =====")
    print("1. 添加图书信息")
    print("2. 查看所有图书")
    print("3. 查询图书（按编号或书名）")
    print("4. 修改图书数量")
    print("5. 删除图书")
    print("6. 保存并退出")
    print("-" * 20)

def main():
    # 程序启动时加载数据
    load_books()
    while True:
        main_menu()
        choice = input("请输入您的选择（1-6）：").strip()
        if choice == "1":
            add_book()
        elif choice == "2":
            show_all_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            update_book_count()
        elif choice == "5":
            delete_book()
        elif choice == "6":
            if save_books():
                print("数据已保存，程序退出")
            break
        else:
            print("无效的选项，请输入1-6之间的数字！")

if __name__ == "__main__":
    main()


    """从这段代码中可以学到以下核心知识点：

1. 文件与JSON操作
   json.load() / json.dump() 读写结构化数据
   文件存在性检查 (os.path.exists)
   异常处理 (try-except) 应对文件损坏或保存失败
2. 数据存储结构
   使用列表存储多本图书，每本图书为字典（键：id, title, author, count）
   全局变量 books 承载应用数据
3. 函数式模块化设计
   按功能拆分函数（增删改查、数据加载/保存、菜单展示）
   global 关键字在函数内修改全局变量
4. 用户输入验证与循环
   while True 配合 break 实现重复输入直至合法
   非空校验、类型转换（int()）、非负判断、重复ID检测
5. 列表推导与查找
   any() 判断重复
   列表推导式过滤删除元素
   遍历列表匹配目标数据
6. 格式化输出
   f"{变量:<宽度}" 实现左对齐表格
   分隔线打印
7. 主程序流程控制
   if __name__ == "__main__": 入口保护
   菜单循环与 if-elif 分支选择
8. 异常捕获
   JSONDecodeError 处理文件损坏
   ValueError 处理非数字输入
   通用 Exception 捕获保存错误
9. 持久化思维
   启动加载 + 退出保存，保证数据不丢失"""