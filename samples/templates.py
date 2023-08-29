UNAUTHORIZED_USER_START_MESSAGE = """
    *Вітаю, користувач!* Ви неавторизовані, щоб користуватися ботом потрібно пройти авторизацію
"""
AUTHORIZED_USER_START_MESSAGE = """
    Доброго вам дня, {user}! Ви вже авторизовані! 
"""
UNAUTHORIZED_USER_ACCOUNT_MESSAGE = """
    Ви ще не авторизовані, для того щоб авторизуватися викличіть команду /start
"""
AUTHORIZED_USER_ACCOUNT_MESSAGE = """
    Для початку операції натисніть кнопку (Змінити поля акаунту)
"""
SUBJECT_AUTHORIZED_STUDENT_MESSAGE = """
    Для початку операції натисніть кнопку (Отримати)
"""
UNAUTHORIZED_USER_GROUP_MESSAGE = """
    Ви ще не авторизовані, зареєструйтеся як вчитель, якщо ви ще цього не зробили, та пройдіть авторизацію викликавши комунду /start
"""
STUDENT_MESSAGE = """
    Цією командую можуть користуватись тільки вчителі
"""
TEACHER_MESSAGE = """
    Цією командую можуть користуватись тільки учні
"""
TEACHER_GROUP_MESSAGE = """
    Для створення нової групи натисніть кнопку (Створити нову групу) \n Для оновлення вже створеної введіть її назву та натисніть кнопку (Оновити)
"""

LOGOUT_USER_MESSAGE = """
    Ви впевнені що хочете вийти з акаунту?
"""
LOGOUT_USER_CANCEL_MESSAGE = """
    Відміна операції
"""

NO_FOUND_ERROR = """
    Нічого не знайдено
"""

ERROR_MESSAGE = """
    Сталася помилка: \n\n{errors}
"""
UNTRACKED_ERROR_MESSAGE = """
    Виникла невідома помилка
"""
AUTHORIZATION_PASSWORD_MESSAGE = """
    Авторизація пройшла успішно!
"""

ABORT_MESSAGE = """
    Дію було скасовано!
"""
AUTHORIZED_USER_MESSAGE = """
    Доброго вам дня, {user}! Ви вже авторизовані та можете без проблем користуватись ботом! 
"""
UNAUTHORIZED_USER_MESSAGE = """
    Доброго дня! Ви поки не здійснили авторизаціюдо системи, щоб це зробити пройдіть авторизацію як викладач або учень! 
"""

AUTHORIZTION_USER_MESSAGE = """
    Введіть свій email адрес
"""

AUTHORIZATION_USER_PASS_ENTERING = """
    Введіть свій пароль
"""
EMAIL_AUNTHORIZATION_FAILED_MESSAGE = """
    Щось пішло не так, перевірте введені вами дані, та спробуйте ще раз ввести свій email
"""

EMAIL_AUNTHORIZATION_FAILED_MESSAGE = """
    Щось пішло не так, перевірте введені вами дані, та спробуйте ще раз ввести свій email
"""

START_REGISTRATION_MESSAGE = """
Для початку реєстрації введіть email адресу!
"""

EMAIL_REGISTRATION_MESSAGE = """
Тепер введіть ваше ім'я(можлива кількість символів від 1 до 100, можливі тільки буквені символи)
"""

NAME_REGISTRATION_MESSAGE = """
Тепер введіть ваше прізвище(можлива кількість символів від 1 до 100, можливі тільки буквені символи)
"""

LAST_NAME_REGISTRATION_MESSAGE = """
Тепер введіть ваше ім'я по батькові (можлива кількість символів від 1 до 100, можливі тільки буквені символи)
"""
SURNAME_REGISTRATION_MESSAGE = """
Тепер введіть ваш пароль (він повинен містити не меньше 7 символів, вньому маєбути щонайменше одна літера верхньго регістру,
одна цифра та один з наведених имволів: @#$%^&+=*)
"""
PASSWORD_TEACHER_REGISTRATION_MESSAGE = """
Зараз вам потрібно буде ввести верифікаційний код, який вам мав надати андміністратор
"""
VERIF_CODE_REGISTRATION_MESSAGE = """
Вітаю! Ви супішно пройшли реєстрацію та верифікацію, тепер авторизуйтеся в систему
"""


PASSWORD_STUDENT_REGISTRATION_MESSAGE = """
Вітаю! Ви супішно пройшли реєстрацію, тепер авторизуйтеся в систему
"""

EMAIL_REGISTRATION_FAILED_MESSAGE = """
Email адресу було введено некоректо, спробуйте ще раз!
"""

NAME_REGISTRATION_FAILED_MESSAGE = """
Ім'я було введено некоректо, спробуйте ще раз! \n\nВимоги: можлива кількість символів від 1 до 100, можливі тільки буквені символи
"""

LAST_NAME_REGISTRATION_FAILED_MESSAGE = """
Прізвище було введено некоректо, спробуйте ще раз! \n\nВимоги: можлива кількість символів від 1 до 100, можливі тільки буквені символи
"""

SURNAME_REGISTRATION_FAILED_MESSAGE = """
Ім'я по батькові було введено некоректо, спробуйте ще раз! \n\nВимоги: можлива кількість символів від 1 до 100, можливі тільки буквені символи
"""

PASSWORD_REGISTRATION_FAILED_MESSAGE = """
    Пароль було введено некоректо, спробуйте ще раз! \n\nВимоги: доробити!
"""
VERIF_CODE_FAILED_MESSAGE = """
    Код верифікації не підійшов, спробуйте ще раз!
"""
START_UPDATING_MESSAGE = """
 Спочатку якщо хочете змінити email адресу, введіть її!
"""

EMAIL_UPDATING_MESSAGE = """
 Тепер якщо хочете змінити ім'я, введіть його!
"""
NAME_UPDATING_MESSAGE = """
 Тепер якщо хочете змінити призвіще, введіть його!
"""
LAST_NAME_UPDATING_MESSAGE = """
 Тепер якщо хочете змінити ім'я побатькові, введіть його!
"""
SURNAME_UPDATING_MESSAGE = """
 Ваші дані оновлено!
"""

RESULT_TEACHER_START_MESSAGE = """
 Введіть назву результату, який хочете переглянути \n список результатів: {result_string}
"""
RESULT_TEACHER_GET_MESSAGE = """
 Якщо хочете змінити якусь оцінку, введіть текст запитання \n Результат:{result_string}
"""
RESULT_TEACHER_GET_FAILED_MESSAGE = """
 Назву результату було введено невірно
"""
RESULT_TEACHER_QUESTION_MESSAGE = """
 Тепер введіть нову оцінку \n Результат:{result_string}
"""
RESULT_TEACHER_QUESTION_FAILED_MESSAGE = """
Текст запитання було введено некоректно
"""
RESULT_TEACHER_MARK_MESSAGE = """
 Оцінку змінено, ви можете продовжити зміни, або натиснути кнопку(Завершити) \n Результат:{result_string}
"""
RESULT_TEACHER_MARK_FAILED_MESSAGE = """
Оцінку було введено некоректно
"""

RESULT_STUDENT_STRAT_MESSAGE = """
Для отримання списку результатів натисніть клавішу
"""
RESULT_STUDENT_LIST_START_MESSAGE = """
 Введіть назву результату, який хочете переглянути \n список результатів: {result_string}
"""
RESULT_STUDENT_GET_MESSAGE = """
 Загальна оцінка:{final_mark} \n Ваш результат: \n {result_string}
"""
RESULT_STUDENT_GET_FAILED_MESSAGE = """
Назву результату було введено неправильно
"""

SUBJECT_TEACHER_STRAT_MESSAGE = """
Якщо хочете створити новий предмет, натисніть (Створити)\n Якщо додати запитання до вже існуючого, натисніть (Додати запитання) \n Якщо отримати список тестів, натисніть(Отримати)
"""
SUBJECT_TEACHER_CREATE_MESSAGE = """
Введіть назву предмета
"""
TEST_ADD_SUBJECT_TITLE_ENTER_MESSAGE = """
Тепер введіть назву тесту
"""
SUBJECT_TITLE_ENTER_MESSAGE = """
Тепер введіть назву групи,до якої буде відноситись цей предмет
"""
SUBJECT_TITLE_ENTER_FAILED_MESSAGE = """
Назву предмета було вказано некоректно
"""
SUBJECT_GROUP_ENTER_MESSAGE = """
Тепер введіть назву тесту, якщо не хочете зараз додавати тест, натисніть кнопку(Вихід)
"""
SUBJECT_GROUP_ENTER_FAILED_MESSAGE = """
Назву групи було вказано некоректно
"""
TEST_TITLE_ENTER_MESSAGE = """
Тепер введіть оцінку за тест
"""
TEST_TITLE_ENTER_FAILED_MESSAGE = """
Назву тесту було вказано некоректно
"""
TEST_MAX_MARK_ENTER_MESSAGE = """
Тепер введіть кількість спроб здачі тесту
"""
TEST_MAX_MARK_ENTER_FAILED_MESSAGE = """
Оцінку за тест було вказано некоректно
"""
TEST_NUMBER_OF_ATTEMPS_ENTER_MESSAGE = """
Тепер виберіть чи буде видно цей тест студентам
"""
TEST_NUMBER_OF_ATTEMPS_ENTER_FAILED_MESSAGE = """
Кількість спроб здачі тесту було вказано некоректно
"""
TEST_PENALTY_ENTER_MESSAGE = """
Тепер введіть поріг перескладання(від 1 до 100)
"""
TEST_PENALTY_ENTER_FAILED_MESSAGE = """
Штраф за перескладання(від 1 до 100) було вказано некоректно
"""
TEST_LEVEL_ENTER_MESSAGE = """
Тепер введіть час на складання тесту в такому форматі \n ГГ:ХХ:СС - де г - години, х - хвилини, с - секунди
"""
TEST_LEVEL_ENTER_FAILED_MESSAGE = """
Поріг перескладанн(від 1 до 100) було вказано некоректно
"""
TEST_DURATION_ENTER_MESSAGE = """
Тепер введіть дату початку тесту у такому форматі \n Приклад: 2023-06-02 15:30:00
"""
TEST_DURATION_ENTER_FAILED_MESSAGE = """
Час на складання тесту було вказано некоректно \n ГГ:ХХ:СС - де г - години, х - хвилини, с - секунд
"""
TEST_START_DATE_ENTER_MESSAGE = """
Тепер введіть дату закінчення тесту у такому форматі \n Приклад: 2023-06-02 15:30:00
"""
TEST_START_DATE_ENTER_FAILED_MESSAGE = """
Дату початку тесту було вказано некоректно \n Приклад: 2023-06-02 15:30:00
"""
TEST_END_DATE_ENTER_MESSAGE = """
Тепер введіть кількість питань
"""
TEST_END_DATE_ENTER_FAILED_MESSAGE = """
Дату закінчення тесту було вказано некоректно \n Приклад: 2023-06-02 15:30:00
"""
TEST_COUNT_OF_QUESTION_ENTER_MESSAGE = """
Вітаю! Тест створено! Тепер можете створити питання, введіть текст питання
"""
TEST_COUNT_OF_QUESTION_ENTER_FAILED_MESSAGE = """
Кількість питань тесту було вказано некоректно 
"""

TEST_VISIBILITY_ENTER_MESSAGE = """
Тепер виберіть чи буде включена автоматична перевірка
"""
TEST_AUTOMATE_CHECKING_ENTER_MESSAGE = """
Тепер виберіть чи будуть питання у випадковому порядку
"""
TEST_QUESTION_RANDOMIZER_ENTER_MESSAGE = """
Тепер виберіть чи можна буде повертатися до попередніх запитань
"""
TEST_BACKSTEP_ENTER_MESSAGE = """
Тепер введіть штраф за перескладання(від 1 до 100)
"""
QUESTION_ADD_MESSAGE = """
Тепер можете створити питання, введіть текст питання
"""
QUESTION_TEXT_ENTER_MESSAGE = """
Тепер оберіть тип відповіді на питання
"""
QUESTION_TEXT_ENTER_FAILED_MESSAGE = """
Текст було введено неправильно
"""
QUESTION_MARK_ENTER_MESSAGE = """
Тепер можете завантажити зображення, якщо хочете
"""
QUESTION_MARK_ENTER_FAILED_MESSAGE = """
Кількість балів було введено неправильно
"""
QUESTION_IMAGE_ENTER_MESSAGE = """
Тепер можете завантажити файл, якщо хочете
"""
QUESTION_IMAGE_ENTER_FAILED_MESSAGE = """
Помилка завантаження
"""
QUESTION_FILE_ENTER_MESSAGE = """
Вітаю! Тепер можете додати відповіді до цього запитання
"""
QUESTION_FILE_ENTER_FAILED_MESSAGE = """
Помилка завантаження
"""
ANSWER_TEST_START_MESSAGE = """
Тепер введіть відповідь
"""
ANSWER_TEST_TEXT_MESSAGE = """
Тепер введіть кількість балів за цю відповідь 
"""
ANSWER_TEST_TEXT_FAILED_MESSAGE = """
Відповідь було введено некоректно
"""
ANSWER_TEST_MARK_ENTER_MESSAGE = """
Тепер оберіть чи правильна ця відповідь
"""
ANSWER_TEST_MARK_ENTER_FAILED_MESSAGE = """
Оцінку було введено некоректно
"""
ANSWER_TEST_IS_CORRECT_MESSAGE = """
Вітаю! тепер можете додати ще відповідей
"""
ANSWER_MULTITEST_START_MESSAGE = """
Тепер введіть відповідь
"""
ANSWER_TEXT_START_MESSAGE = """
Вітаю! Тепер можете додати ще запитання
"""
ANSWER_MULTITEST_TEST_TEXT_MESSAGE = """
Тепер напишіть оцінку за цю відповідь
"""

TEST_ADD_SUBJECT_MESSAGE = """
 Тепер ви можете вибрати предмет, тест до якого ви хочете додати \n список предметів: {result_string}
"""

SUBJECT_UPDATE_MESSAGE = """
 Тепер ви можете вибрати предмет, який хочете змінити \n список предметів: {result_string}
"""
SUBJECT_UPDATE_START_MESSAGE = """
 Введіть оновлену оцінку за тест
"""

SUBJECT_STUDENT_MESSAGE = """
 Тепер ви можете вибрати предмет щоб переглянути його тести \n список предметів: {result_string}
"""
SUBJECT_STUDENT_TITLE_MESSAGE = """
 Тепер ви можете вибрати тест, який хочете пройти \n список тестів: {result_string}
"""
SUBJECT_STUDENT_TITLE_ENTER_MESSAGE = """
 Тест розпочато, надавайте відповіді на питання \n {question_text} \n {result_string}
"""
SUBJECT_STUDENT_TEST_TITLE_ENTER_FAILED_MESSAGE = """
 Цей тест недоступний
"""
SUBJECT_STUDENT_ANSWER_ENTER_MESSAGE = """
 Тест розпочато, надавайте відповіді на питання \n {question_text} \n {result_string} \n Відповідь записано!
"""

SUBJECT_STUDENT_TITLE_ENTER_FAILED_MESSAGE = """
 Назву тесту було введено некоректно
"""
SUBJECT_TEACHER_TITLE_ENTER_MESSAGE = """
 Тепер введіть ім'я тесту, який ви хочете отримати \n список тестів: {result_string}
"""
SUBJECT_TEACHER_TITLE_ENTER_FAILED_MESSAGE = """
 Назва предмету була введена неправильно
"""

SUBJECT_TEACHER_TEST_TITLE_ENTER_MESSAGE = """
 Тепер, якщо хочете змінити налаштування тесту, натисніть (Оновити)\n якщо хочете переглянути результати, натисніть (Переглянути результати)
"""
SUBJECT_TEACHER_TEST_TITLE_ENTER_FAILED_MESSAGE = """
 Назву тесту було введено неправильно
"""
SUBJECT_TEACHER_TEST_MAX_MARK_ENTER_MESSAGE = """
 Введіть оновлені кількість спроб
"""
SUBJECT_TEACHER_TEST_MAX_MARK_ENTER_FAILED_MESSAGE = """
Оцінку було введено неправильно
"""
SUBJECT_TEACHER_TEST_NUMBER_OF_ATTEMPS_ENTER_MESSAGE = """
  Оберіть оновлену видимість тесту, виберіть Так чи Ні
"""
SUBJECT_TEACHER_TEST_NUMBER_OF_ATTEMPS_ENTER_FAILED_MESSAGE = """
Кількість спроб було введено неправильно
"""
SUBJECT_TEACHER_TEST_VISIBILITY_ENTER_MESSAGE = """
 Оберіть оновлену автоматичну перевірку тесту, виберіть Так чи Ні,
"""
SUBJECT_TEACHER_TEST_AUTO_CHECK_ENTER_MESSAGE = """
 Оберіть оновлений порядок питань, виберіть Так чи Ні,
"""
SUBJECT_TEACHER_TEST_QUESTION_RANDOMIZER_ENTER_MESSAGE = """
 Оберіть оновлене повернення , виберіть Так чи Ні
"""
SUBJECT_TEACHER_TEST_BACKSTEP_ENTER_MESSAGE = """
  Введіть оновлений штраф за перескладання
"""
SUBJECT_TEACHER_TEST_PENALTY_ENTER_MESSAGE = """
 Введіть оновлений рівень складання
"""
SUBJECT_TEACHER_TEST_PENALTY_ENTER_FAILED_MESSAGE = """
Штраф за перескладання було введено неправильно
"""
SUBJECT_TEACHER_TEST_LEVEL_ENTER_MESSAGE = """
 Тепер введіть час на складання тесту в такому форматі \n ГГ:ХХ:СС - де г - години, х - хвилини, с - секунди
"""
SUBJECT_TEACHER_TEST_LEVEL_ENTER_FAILED_MESSAGE = """
Поріг складання було введено неправильно
"""
SUBJECT_TEACHER_TEST_DURATION_ENTER_MESSAGE = """
 Тепер введіть дату початку тесту у такому форматі \n Приклад: 2023-06-02 15:30:00
"""
SUBJECT_TEACHER_TEST_DURATION_ENTER_FAILED_MESSAGE = """
Час на складання тесту було вказано некоректно \n ГГ:ХХ:СС - де г - години, х - хвилини, с - секунд
"""
SUBJECT_TEACHER_TEST_START_DATE_ENTER_MESSAGE = """
 Тепер введіть дату закінчення тесту у такому форматі \n Приклад: 2023-06-02 15:30:00
"""
SUBJECT_TEACHER_TEST_START_DATE_ENTER_FAILED_MESSAGE = """
Дату початку тесту було введено неправильно  \n Приклад: 2023-06-02 15:30:00
"""
SUBJECT_TEACHER_TEST_END_DATE_ENTER_MESSAGE = """
 Тепер введіть кількість запитань, якщо не хочете
"""
SUBJECT_TEACHER_TEST_END_DATE_ENTER_FAILED_MESSAGE = """
Дату закінчення тесту було введено неправильно  \n Приклад: 2023-06-02 15:30:00
"""
SUBJECT_TEACHER_TEST_COUNT_QUEST_ENTER_MESSAGE = """
 Вітаю! Тепер можете додати ще питань до цього тесту, якщо не хочете, натисніть на клавішу (Завершити)
"""
SUBJECT_TEACHER_TEST_COUNT_QUEST_ENTER_FAILED_MESSAGE = """
кількість запитань тесту було введено неправильно  
"""


GROUP_START_MESSAGE = """
 Спочатку введіть ім'я групи, воно повинно бути унікальним і має містити від 1 до 10 літер
"""
GROUP_UPDATE_START_MESSAGE = """
 Спочатку введіть ім'я групи, яку ви хочете змінити \n список груп: {result_string}
"""
GROUP_ADD_STUDENT_START_MESSAGE = """
 Спочатку введіть ім'я групи, в яку ви хочете додати студента \n список груп: {result_string}
"""
GROUP_NAME_UPDATE_MESSAGE = """
Тепер введіть ім'я групи, на яке ви хочете його змінити
"""

GROUP_NAME_FAILED_MESSAGE = """
 Ім'я групи було введено некоректно, воно повинно бути унікальним і має містити від 1 до 10 літер
"""
GROUP_NAME_MESSAGE = """
 Тепер ви можете додати студентів до цієї групи, для цього введіть емейл адресу студента \n список студентів: {result_string}
"""
GROUP_STUDENT_UPDATE_MESSAGE = """
 Тепер ви можете додати студента, ввівши його електронну адресу
"""

GROUP_ADD_STUDENT_MESSAGE = """
 Ви успішно додали студента, тепер ви можете зробити це ще раз або закінчити додавання натиснувши на кнопку(Закінчити) \n, для цього введіть емейл адресу студента \n список студентів: {result_string}
"""
GROUP_ADD_STUDENT_FAILED_MESSAGE = """
 Емейл адресу було вказано неправильно
"""
GROUP_END_MESSAGE = """
 Операцію завершено
"""
