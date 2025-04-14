**Описание проекта "Warehouse Bot"**

Проект представляет собой Telegram-бота для управленческого учета остатков на складе. С его помощью можно:

- Добавлять данные о поступлениях и отгрузках;
- Просматривать текущие остатки и формировать отчёты;
- Автоматически обновлять Excel-файл склада.

Бот разработан на Python с использованием `aiogram`, данные хранятся в Excel-файле, а работа логируется. Приложение упаковано в Docker-контейнер, что позволяет удобно запускать его на сервере 24/7.

==============================================================================
  README.txt — Инструкция по запуску приложения "Warehouse Bot"
==============================================================================

Предварительные требования:
---------------------------
1. Установлены Docker и, при необходимости, Docker Desktop на тестирующем сервере/машине.
2. Исходный код приложения, включая следующие файлы, находится в каталоге проекта:
   - Dockerfile
   - requirements.txt
   - bot.py, config.py, decorators.py, excel_manager.py, handlers.py, reports.py, utils.py
   - Excel-файл: ESP_sklad_2.xlsx (и сопутствующие файлы, если есть)

Инструкция по запуску:
---------------------

Шаг 1. Сборка Docker-образа
---------------------------
1. Откройте терминал и перейдите в корневой каталог проекта.
   Пример (Windows CMD):
       cd C:\Путь\к\проекту\For_Warehouse
2. Выполните команду для сборки образа:
       docker build --no-cache -t my-warehouse-app .
   Эта команда создаст Docker-образ с тегом "my-warehouse-app".
   
Шаг 2. Создание именованного volume (для сохранения данных)
-----------------------------------------------------------
Если volume "warehouse_data" ещё не создан, создайте его:
       docker volume create warehouse_data

Шаг 3. Запуск контейнера с volume
----------------------------------
Для запуска контейнера с сохранением данных (Excel, логи и т.п.) выполните следующую команду:
       
   Windows CMD (однострочная команда):
       docker run -d --name warehouse_bot --restart unless-stopped -v warehouse_data:/app my-warehouse-app
       
Пояснения:
 - -d                       : запуск контейнера в фоновом режиме;
 - --name warehouse_bot      : задание имени контейнера;
 - --restart unless-stopped  : автоматический перезапуск контейнера после сбоя или перезагрузки сервера;
 - -v warehouse_data:/app     : монтирует именованный volume "warehouse_data" в каталог /app внутри контейнера;
 - my-warehouse-app          : имя собранного образа.

Шаг 4. Проверка работы приложения
----------------------------------
1. Просмотр запущенных контейнеров:
       docker ps
   Убедитесь, что контейнер с именем "warehouse_bot" запущен.

2. Просмотр логов контейнера:
       docker logs -f warehouse_bot
   Логи покажут, что бот успешно запустился и работает.

3. (Опционально) Вход в контейнер для проверки файлов:
       docker exec -it warehouse_bot /bin/sh
   После входа выполните команду:
       ls -l /app
   Вы должны увидеть, что в каталоге /app присутствуют все необходимые файлы, включая Excel-файл ESP_sklad_2.xlsx.

Шаг 5. Управление контейнером
-----------------------------
- Перезапуск контейнера:
       docker restart warehouse_bot

- Остановка контейнера:
       docker stop warehouse_bot

- Удаление контейнера (при необходимости):
       docker rm warehouse_bot

- Если потребуется удалить также volume (данные будут утеряны):
       docker volume rm warehouse_data

Дополнительные примечания:
--------------------------
• Все изменения, внесённые приложением (например, обновление Excel-файла или логов), сохраняются в volume "warehouse_data". При пересоздании контейнера данные сохранятся, если volume не удалён.
• Если приложение в процессе разработки, после изменений в коде можно пересобрать образ с командой:
       docker build --no-cache -t my-warehouse-app .
  и затем перезапустить контейнер (не забудьте удалить старый контейнер, если требуется).

==============================================================================
Конец инструкции.
==============================================================================
