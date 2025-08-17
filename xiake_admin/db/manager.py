from django.db import connections
from django.apps import apps
from django.core.management import execute_from_command_line
import sys


class DatabaseManager:
    """
    数据库管理器，提供数据库操作的便捷方法
    """

    def __init__(self, database='default'):
        self.database = database
        self.connection = connections[database]

    def get_tables(self):
        """获取所有表名"""
        with self.connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            return [row[0] for row in cursor.fetchall()]

    def table_exists(self, table_name):
        """检查表是否存在"""
        tables = self.get_tables()
        return table_name in tables

    def drop_table(self, table_name):
        """删除表"""
        with self.connection.cursor() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.connection.commit()

    def execute_sql(self, sql):
        """执行原生SQL"""
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def syncdb(self):
        """同步数据库"""
        # 这里调用我们自定义的syncdb命令
        sys.argv = ['manage.py', 'syncdb', '--database', self.database]
        execute_from_command_line(sys.argv)

    def reset_db(self):
        """重置数据库（删除所有表并重新创建）"""
        tables = self.get_tables()
        for table in tables:
            self.drop_table(table)

        # 重新同步
        self.syncdb()


# 使用示例的管理命令
class DatabaseCommand:
    """
    数据库管理命令
    """

    @staticmethod
    def syncdb():
        """同步数据库命令"""
        db_manager = DatabaseManager()
        db_manager.syncdb()

    @staticmethod
    def reset():
        """重置数据库"""
        db_manager = DatabaseManager()
        db_manager.reset_db()

    @staticmethod
    def show_tables():
        """显示所有表"""
        db_manager = DatabaseManager()
        tables = db_manager.get_tables()
        print("Database tables:")
        for table in tables:
            print(f"  - {table}")
