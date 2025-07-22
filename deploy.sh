#!/bin/bash

echo "🚀 Начинаем деплой Freelance Lena Bot..."

# Переходим в директорию проекта
PROJECT_DIR="/opt/freelance_lena_bot"

# Создаем директорию если её нет
sudo mkdir -p $PROJECT_DIR

# Копируем файлы
echo "📁 Копируем файлы..."
sudo cp -r . $PROJECT_DIR/
cd $PROJECT_DIR

# Создаем виртуальное окружение
echo "🐍 Создаем виртуальное окружение..."
python3 -m venv venv
source venv/bin/activate

# Устанавливаем зависимости
echo "📦 Устанавливаем зависимости..."
pip install -r requirements.txt

# Создаем директории
sudo mkdir -p data logs

# Копируем systemd сервис
echo "⚙️ Настраиваем systemd сервис..."
sudo cp freelance-bot.service /etc/systemd/system/
sudo systemctl daemon-reload

# Настраиваем nginx
echo "🌐 Настраиваем nginx..."
sudo cp nginx-freelance-bot.conf /etc/nginx/sites-available/freelance-bot
sudo ln -sf /etc/nginx/sites-available/freelance-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Запускаем бота
echo "▶️ Запускаем бота..."
sudo systemctl enable freelance-bot
sudo systemctl start freelance-bot

# Проверяем статус
echo "✅ Проверяем статус..."
sudo systemctl status freelance-bot

echo "🎉 Деплой завершен! Бот доступен на http://109.73.194.190/freelance-bot/"
echo "📊 Логи: sudo journalctl -u freelance-bot -f"
echo "🔄 Перезапуск: sudo systemctl restart freelance-bot"
