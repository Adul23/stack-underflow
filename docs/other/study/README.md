# Материалы для учебной защиты

Начните с [отчёта Word](REPORT_RU.docx) или [отчёта HTML](REPORT_RU.html): все пять пунктов задания, диаграммы, объяснения и примеры результатов. HTML содержит встроенные диаграммы и открывается без интернета. Редактируемый текст — [REPORT_RU.md](REPORT_RU.md).

| Материал | Файлы |
| --- | --- |
| Структура PostgreSQL | [Mermaid](database.mmd), [SVG](database.svg), [PNG](database.png) |
| CRUD вопроса | [Mermaid](question_crud.mmd), [SVG](question_crud.svg), [PNG](question_crud.png) |
| Текущий поиск | [Mermaid](search.mmd), [SVG](search.svg), [PNG](search.png) |
| 15 SQL-запросов | [check_tables.sql](check_tables.sql) |
| Фактические результаты | [sql_results.md](sql_results.md), [psql_results.txt](psql_results.txt), [verification.json](verification.json) |
| Проверки Django и тесты | [django_checks.txt](django_checks.txt), [backend_tests.txt](backend_tests.txt) |
| Примеры поиска | [search_examples.json](search_examples.json) |

Повторный запуск из корня проекта, при работающем Docker Desktop:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\docs\study\run-demo.ps1 -RunTests
```

Скрипт использует отдельный Compose-проект `stack-underflow-study`, БД `stack_underflow_study`, порт `127.0.0.1:55432` и том `stack-underflow-study_study_data`. Секреты лежат в игнорируемом `.env.study`. Учебные данные остаются в БД после проверки. Тестовые аккаунты Alice/Bob имеют неиспользуемый пароль: это записи для SQL-демонстрации, не готовые логины для сайта. Для проверки регистрации и входа скрипт создаёт отдельный временный аккаунт с настоящим JWT и откатывает его транзакцию.

Повторное создание изображений и отчётов после редактирования исходников:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\docs\study\render-diagrams.ps1
.\.venv\Scripts\python.exe -m pip install -r .\docs\study\report-requirements.txt
.\.venv\Scripts\python.exe .\docs\study\build_report.py
```

Рендер диаграмм требует Node/npm и Chrome. Если Chrome установлен по другому пути, передайте `-ChromePath`; подходит и установленный Edge. Готовые SVG/PNG, Word и HTML можно использовать без установки этих инструментов. Числовые итоги в основном отчёте описывают сохранённый учебный набор; если вручную изменить его, обновите текст отчёта по новым результатам.
