from django.core.management.base import BaseCommand
from django.apps import apps
from django.template import Template, Context
import os


class Command(BaseCommand):
    help = 'Generate Vue3 + Element Plus admin pages for models'

    def add_arguments(self, parser):
        # 修改app_label为可选参数
        parser.add_argument('app_label', nargs='?', help='App label of an application to generate pages for')
        parser.add_argument('model_name', nargs='?', help='Model name to generate page for')
        parser.add_argument(
            '--output-dir',
            default='./web/src/views/',
            help='Output directory for generated Vue files'
        )

    def handle(self, *args, **options):
        app_label = options['app_label']
        model_name = options['model_name']
        output_dir = options['output_dir']

        try:
            # 如果没有提供app_label，则处理所有非Django自带的应用
            if not app_label:
                app_configs = [app_config for app_config in apps.get_app_configs()
                               if not app_config.name.startswith('django.contrib')]

                for app_config in app_configs:
                    self.process_app(app_config, output_dir, model_name)

                self.stdout.write(
                    self.style.SUCCESS(f'Successfully generated Vue pages in {output_dir}')
                )
                return

            # 如果提供了app_label，则按原来逻辑处理单个应用
            app_config = apps.get_app_config(app_label)

            # 过滤掉Django自带的组件
            if app_config.name.startswith('django.contrib'):
                self.stdout.write(
                    self.style.ERROR(f'Cannot generate pages for Django built-in app "{app_label}"')
                )
                return

            # 创建输出目录
            os.makedirs(output_dir, exist_ok=True)

            # 如果指定了模型，只生成该模型的页面
            if model_name:
                try:
                    model = app_config.get_model(model_name)
                    self.generate_model_page(model, output_dir)
                except LookupError:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Model "{model_name}" not found in app "{app_label}". Available models: {", ".join([m.__name__ for m in app_config.get_models()])}')
                    )
                    return
            else:
                # 为应用中的所有模型生成页面
                models = app_config.get_models()
                for model in models:
                    self.generate_model_page(model, output_dir)

            self.stdout.write(
                self.style.SUCCESS(f'Successfully generated Vue pages in {output_dir}')
            )

        except LookupError:
            self.stdout.write(
                self.style.ERROR(
                    f'App "{app_label}" not found. Available apps: {", ".join([app.label for app in apps.get_app_configs() if not app.name.startswith("django.contrib")])}')
            )
            return

    # 新增方法：处理单个应用
    def process_app(self, app_config, output_dir, model_name=None):
        self.stdout.write(f'Processing app: {app_config.label}')

        if model_name:
            try:
                model = app_config.get_model(model_name)
                self.generate_model_page(model, output_dir)
            except LookupError:
                self.stdout.write(
                    self.style.ERROR(
                        f'Model "{model_name}" not found in app "{app_config.label}". Available models: {", ".join([m.__name__ for m in app_config.get_models()])}')
                )
        else:
            models = app_config.get_models()
            for model in models:
                self.generate_model_page(model, output_dir)

    def generate_model_page(self, model, output_dir):
        """
        为单个模型生成Vue页面
        """
        model_name = model.__name__
        app_label = model._meta.app_label

        # 创建模型对应的目录
        model_dir = os.path.join(output_dir, app_label, model_name.lower())
        os.makedirs(model_dir, exist_ok=True)

        # 生成列表页面
        list_page_content = self.generate_list_page(model)
        list_page_path = os.path.join(model_dir, 'List.vue')
        with open(list_page_path, 'w', encoding='utf-8') as f:
            f.write(list_page_content)

        # 生成表单页面
        form_page_content = self.generate_form_page(model)
        form_page_path = os.path.join(model_dir, 'Form.vue')
        with open(form_page_path, 'w', encoding='utf-8') as f:
            f.write(form_page_content)

        self.stdout.write(f'  Generated pages for {app_label}.{model_name}')

    def generate_list_page(self, model):
        """
        生成列表页面Vue组件
        """
        model_name = model.__name__
        fields = model._meta.get_fields()

        # 过滤出可显示的字段
        display_fields = []
        for field in fields:
            if hasattr(field, 'name') and not field.name.endswith('_ptr'):
                display_fields.append(field)

        # 获取模板文件路径
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        list_template_path = os.path.join(template_dir, 'list_page_template.txt')

        # 读取模板文件
        with open(list_template_path, 'r', encoding='utf-8') as f:
            template_str = f.read()

        template = Template(template_str)
        context = Context({
            'model_name': model_name,
            'display_fields': display_fields[:5]  # 限制显示前5个字段
        })
        return template.render(context)

    def generate_form_page(self, model):
        """
        生成表单页面Vue组件
        """
        model_name = model.__name__
        fields = [f for f in model._meta.fields if f.name != 'id']

        # 获取模板文件路径
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        form_template_path = os.path.join(template_dir, 'form_page_template.txt')

        # 读取模板文件
        with open(form_template_path, 'r', encoding='utf-8') as f:
            template_str = f.read()

        template = Template(template_str)
        context = Context({
            'model_name': model_name,
            'fields': fields[:10]  # 限制显示前10个字段
        })
        return template.render(context)
