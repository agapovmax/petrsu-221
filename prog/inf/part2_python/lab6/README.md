### Использование

```bash
python3 dupl.py <dir>
```

### Создание тестового окружения

Для тестирования программы, необходимо подготовить каталоги с дубликатами для поиска одинаковых файлов (по хэшу)

1. Создание каталога new и файлов в нем
```bash
mkdir new && for i in {1..8}; do touch file$i.log; done
```

2. Создание каталога new2 в new с такими же файлами

```bash
mkdir new/new2 && for i in {1..8}; do touch file$i.log; done
```

3. После первого запуска и тестирования удаления, можно создавать дубликаты командами

```bash
for i in {1..8}; do touch new/file$i.log; done
for i in {1..8}; do touch new/new2/file$i.log; done
```
