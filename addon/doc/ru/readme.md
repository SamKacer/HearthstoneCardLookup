# Hearthstone Card Lookup (Поиск карт Hearthstone)

Это дополнение для NVDA, которое позволяет пользователям быстро искать информацию о конкретной карте Hearthstone по её названию.

- [скачать стабильную версию](https://github.com/SamKacer/HearthstoneCardLookup/releases/download/v0.10.2/HearthstoneCardLookup-0.10.2.nvda-addon)

## Использование

Выделите текст названия карты или скопируйте его в буфер обмена, затем нажмите NVDA + H, и дополнение попытается найти информацию о карте и отобразить её во всплывающем окне с возможностью просмотра.

Также вы можете нажать NVDA + shift + H, что вызовет диалог, в котором вы можете ввести название карты для поиска.

### Пример вывода

```
Тирион Фордринг
8 маны
6 6
Божественный щит. Нападение. Смертельный грохот: Экипируйте 5/3 Эшбрингера.
Миньон
Паладин
Легендарный
Наследие
Если вы не слышали песню Тириона Фордринга, то это потому, что её не существует.
``` 	

## Журнал изменений

### v0.10.4
- исправлена HTTP-ошибка 403 при получении карты

### v0.10.3
- добавлена русская локализация (спасибо @Kostenkov-2021)

### v0.10.2
- исправлено не отображение классов на многоклассовых картах
- обновлена последняя протестированная версия NVDA до 2024.4.1

### v0.10.1
- исправлено отображение не всех рун для карт, имеющих несколько типов рун, например, «Кульминационный некротический взрыв»

### v0.10
- исправление дополнения, не работающего после переезда вики Hearthstone на новый сайт

### v0.9
- показывать все руны для карт с более чем одной руной, например, Кульминационный некротический взрыв

### v0.8
- обновлено для работы с NVDA 2023
- исправлена ошибка, из-за которой дополнение перестало работать после того, как вики фэндома Hearthstone изменила свой макет
- исправлено не отображение типов миньонов и мультиклассов

### v0.7
- при открытии диалога поиска карты допускается существование только одного такого диалога
- совместимо с NVDA версии 2022.1

### v0.6
- исправлены некоторые карты, не получаемые в результате поиска, например, Удар молотком Гнолла и Суматоха (ранг 1)

### v0.5
- ускорено получение информации о картах в некоторых случаях
- добавлена новая команда для поиска информации о карте из пользовательского ввода (NVDA + shift + H)

### v0.4
- отображение мультикласса, если он доступен для карты

### v0.3

- Исправлено не отображение статистики для оружия
- Не отображать стоимость маны для карт без затрат
- Сделать возможным просмотр карт, перечисленных в верхних колодах

###v0.2

- отображать тип миньона
- исправить странное отображение символов для некоторых карт

### v0.1

- первоначальный релиз

## [Домашняя страница](https://github.com/SamKacer/HearthstoneCardLookup)

Используйте этот github для публикации проблем дополнения.

