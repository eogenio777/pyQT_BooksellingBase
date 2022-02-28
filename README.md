#  Bookselling Base
## Что такое Bookselling Base
**Bookselling Base** - это университетский проект по предмету СУБД, целью является реализовать систему для автоматизации работы книготорговой базы в качестве десктоп приложения с использованием СУБД MSQL Server. 
В системе должно быть 3 типа пользователей: 
 - [x] **Администратор** - имеет возможность добавлять новых сотрудников, изменять их учетные записи, добавлять или изменять заказы, добавлять, удалять или изменять товары.
 - [x] **Менеджер** - может отредактировать заказ, получить список всех заказов, добавить или изменить товар.
 - [x] **Покупатель** - может оформить заказ через добавление товаров в корзину.
Информационная система должна хранить информацию о заказах, сотрудниках, товаре на складе.

## Схема БД
![](https://sun9-70.userapi.com/impg/BJ2rA4jIijxMmJxn-zMVky7eifAz5rYZuurZlw/sT3sELxSpMI.jpg?size=725x756&quality=96&sign=6b5d300744822b1d3488744b19eeed04&type=album)

## Создание БД
https://drive.google.com/file/d/1HJln5iMSE4HPk82X_7-OSKP3m7uJpwOx/view?usp=sharing

## Запуск проекта
Для запуска проекта требуется:

 - установить MSQL Server
 - создать БД в среде разработки (используя приложенный файл)
 - склонировать репозиторий: `git clone https://github.com/eogenio777/pyQT_BooksellingBase.git`
 - создать виртуальное окружение: `pipenv shell`
 - собрать пакеты из файла `requirements.txt`:  `pipenv install requirements.txt`
 - запустить:  `python main.py`

## Скриншоты
Стартовая страница

![](https://sun9-15.userapi.com/impg/uHs-lMiXsOp5Mo4nPfi4n2uck2HxpB3LiQb6Lw/vENYwgHv5G8.jpg?size=708x323&quality=96&sign=e362ad22d219a819778f5fbbe12ed482&type=album)

Страница регистрации

![](https://sun9-66.userapi.com/impg/6loldP0PCteYcUXDGyoBp4l9GQhe6yiDwqkA7Q/3dDAouRiRVg.jpg?size=565x586&quality=96&sign=35f6bc18a9aa5229465c421f388ee7d7&type=album)

Каталог (покупатель)

![](https://sun9-51.userapi.com/impg/8M-797Re8wzspUMG5I6MZZcax3BzRQpWSLIUrw/Q4AtsILARC0.jpg?size=747x741&quality=96&sign=8b8cc28b36700bd09efe6b5086d43e76&type=album)

Заказы (покупатель)

![](https://sun9-8.userapi.com/impg/JEl-b1oBwJyDUnR0IdMAGno2I4jag7NaibBxCg/XqMsn2f7XWM.jpg?size=863x851&quality=96&sign=9a696da1a67aee6bad170a316a7cc5ab&type=album)

Корзина (покупатель)

![](https://sun9-30.userapi.com/impg/9MM9ThlanllHIrGjBn6oEWhPfcUC_8AQP53M6A/sK_-F5lirf8.jpg?size=891x973&quality=96&sign=4ff3e945e9633439409f87ff86a6a978&type=album)

Каталог (менеджер)

![](https://sun9-73.userapi.com/impg/4y9OiHnLkvSqyxhUl_ynjZ1meRz4XFCePbJoqw/Sv88jMg8RiM.jpg?size=1127x728&quality=96&sign=49c03ab56a61d2039d70d41329eaebb6&type=album)

Каталог (админ)

![](https://sun9-26.userapi.com/impg/rcqlmH2kTv4IqR3efN9b1nR5C-Zv9SVmYuolRA/b9A94lBAnzw.jpg?size=875x908&quality=96&sign=4d73d77fc204f3bd4c1bd0d8a97be65a&type=album)

Статистика по сотрудникам (админ)

![](https://sun9-54.userapi.com/impg/B-hFXqoTK4UBeeNoUeTesrbDb_ddocgE_LFljg/6IiHJpeLb1Q.jpg?size=1046x1090&quality=96&sign=ea83286bbe3aaa267f147b661b503148&type=album)

Список сотрудников (админ)

![](https://sun9-6.userapi.com/impg/NtX0dsTYdlPQio03tev3OCjQvGgEZw2b_hgN0g/qInFeBhEZfE.jpg?size=1057x1055&quality=96&sign=1d4ae0b973eaaf7d782fd724d7147dfa&type=album)

Статистика по базе (админ)

![](https://sun9-2.userapi.com/impg/vIzwQeqmaaz7_XL4_zH36enjHIf4NKISDZIHqQ/KaPbUyKqMjE.jpg?size=1072x585&quality=96&sign=2afdaa514aef4d9a49ccb102461cb780&type=album)

## Выполнил
Проект выполнен студентом СПбПУ Подружинским Евгением - гр. 3530202/90202
