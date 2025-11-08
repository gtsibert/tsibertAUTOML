#!/usr/bin/env python3
"""
Скрипт для автоматической загрузки и запуска Olympiad AutoML
Использование: python download_and_run.py
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil
from pathlib import Path

def run_command(cmd, check=True):
    """Выполнить команду в shell"""
    print(f"🚀 Выполняю: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка: {e}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False

def download_github_repo():
    """Скачать репозиторий с GitHub"""
    repo_url = "https://github.com/yourusername/olympiad-image-automl/archive/refs/heads/main.zip"
    download_path = "olympiad-automl.zip"
    
    print("📥 Скачиваю Olympiad AutoML...")
    try:
        urllib.request.urlretrieve(repo_url, download_path)
        print("✅ Репозиторий скачан")
        return download_path
    except Exception as e:
        print(f"❌ Ошибка скачивания: {e}")
        return None

def extract_and_setup(zip_path):
    """Распаковать и настроить проект"""
    print("📦 Распаковываю...")
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(".")
    
    # Находим распакованную папку
    extracted_dir = None
    for item in os.listdir("."):
        if item.startswith("olympiad-image-automl") and os.path.isdir(item):
            extracted_dir = item
            break
    
    if not extracted_dir:
        print("❌ Не найдена распакованная папка")
        return False
    
    # Перемещаем файлы в текущую директорию
    for item in os.listdir(extracted_dir):
        shutil.move(os.path.join(extracted_dir, item), ".")
    
    # Удаляем временные файлы
    shutil.rmtree(extracted_dir)
    os.remove(zip_path)
    
    print("✅ Проект распакован и настроен")
    return True

def install_dependencies():
    """Установить зависимости"""
    print("🔧 Устанавливаю зависимости...")
    
    # Проверяем наличие requirements.txt
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt не найден")
        return False
    
    return run_command(f"{sys.executable} -m pip install -r requirements.txt")

def run_demo():
    """Запустить демо-пример"""
    print("🎯 Запускаю демо-пример...")
    
    demo_script = """
import sys
import os
sys.path.append('src')

from automl import FastPyTorchAutoML
import torch

# Проверка установки
print("✅ AutoML успешно установлен!")
print(f"🎯 PyTorch версия: {torch.__version__}")
print(f"🚀 CUDA доступен: {torch.cuda.is_available()}")

# Создаем экземпляр AutoML
automl = FastPyTorchAutoML()
print("🎉 Всё готово к использованию!")
"""
    
    with open("check_installation.py", "w") as f:
        f.write(demo_script)
    
    return run_command(f"{sys.executable} check_installation.py")

def main():
    """Основная функция"""
    print("=" * 60)
    print("🎯 OLYMPIAD IMAGE AUTOML - АВТОМАТИЧЕСКАЯ УСТАНОВКА")
    print("=" * 60)
    
    # Скачать репозиторий
    zip_path = download_github_repo()
    if not zip_path:
        return
    
    # Распаковать
    if not extract_and_setup(zip_path):
        return
    
    # Установить зависимости
    if not install_dependencies():
        print("⚠️ Продолжаем без установки зависимостей...")
    
    # Запустить демо
    run_demo()
    
    print("\\n" + "=" * 60)
    print("🎉 УСТАНОВКА ЗАВЕРШЕНА!")
    print("=" * 60)
    print("📚 Как использовать:")
    print("1. Поместите данные в папку 'dataset/'")
    print("2. Запустите: python examples/basic_usage.py")
    print("3. Или используйте в своем коде:")
    print("""
from automl import FastPyTorchAutoML

automl = FastPyTorchAutoML()
train_loader, val_loader = automl.smart_data_loader('dataset/')
automl.quick_benchmark(train_loader, val_loader)
    """)

if __name__ == "__main__":
    main()
