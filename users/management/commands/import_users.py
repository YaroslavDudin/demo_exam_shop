# users/management/commands/import_users.py

import openpyxl
from pathlib import Path
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


class Command(BaseCommand):
    help = 'Импорт пользователей из Excel с ролями и добавление в группы'

    def handle(self, *args, **options):
        # Файл по умолчанию в папке import
        file_path = Path('import/user_import.xlsx')

        if not file_path.exists():
            self.stderr.write(f"Файл не найден: {file_path}")
            return

        # создаём английские группы
        groups = ['admin', 'manager', 'client']
        for group_name in groups:
            Group.objects.get_or_create(name=group_name)

        # сопоставление русских ролей из Excel → английские группы
        role_map = {
            'Администратор': 'admin',
            'Менеджер': 'manager',
            'Клиент': 'client',
        }

        try:
            wb = openpyxl.load_workbook(file_path)
            ws = wb.active
        except Exception as e:
            self.stderr.write(f"Не удалось открыть файл: {e}")
            return

        for idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            role_excel, full_name, username, password = row

            if not username:
                self.stdout.write(f"Строка {idx} пропущена — нет логина")
                continue

            # переводим роль на английский
            role = role_map.get(role_excel.strip() if role_excel else 'Клиент', 'client')

            # создаём пользователя
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': full_name or '',
                    'role': role  # кастомное поле
                }
            )

            if created:
                user.set_password(password or '123456')  # дефолтный пароль
                user.save()
                self.stdout.write(f"[{idx}] Добавлен пользователь {username}")

            # добавляем пользователя в группу
            group = Group.objects.get(name=role)
            user.groups.add(group)

        self.stdout.write(self.style.SUCCESS("Импорт пользователей завершён"))
