from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
from django.apps import apps
import os


class Command(BaseCommand):
    help = 'Sync database tables without using migrations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--database',
            default='default',
            help='Nominates a database to sync. Defaults to the "default" database.',
        )

    def handle(self, *args, **options):
        database = options['database']
        self.stdout.write(f'Syncing database: {database}')
        
        # 获取所有已安装的应用
        app_configs = apps.get_app_configs()
        
        # 创建所有模型的表
        for app_config in app_configs:
            self.stdout.write(f'Processing app: {app_config.label}')
            try:
                self.create_tables_for_app(app_config, database)
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating tables for {app_config.label}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully synced database')
        )

    def create_tables_for_app(self, app_config, database):
        # 获取应用中的所有模型
        models = app_config.get_models()
        
        for model in models:
            self.create_table_for_model(model, database)

    def create_table_for_model(self, model, database):
        # 获取数据库连接
        connection = connections[database]
        
        # 获取模型对应的创建表SQL
        with connection.schema_editor() as schema_editor:
            try:
                # 检查表是否已存在
                table_name = model._meta.db_table
                if self.table_exists(connection, table_name):
                    self.stdout.write(f'  Table {table_name} already exists')
                else:
                    schema_editor.create_model(model)
                    self.stdout.write(f'  Created table {table_name}')
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'    Error creating table {model._meta.db_table}: {str(e)}')
                )

    def table_exists(self, connection, table_name):
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT 1 FROM {table_name} LIMIT 1")
                return True
        except Exception:
            return False
