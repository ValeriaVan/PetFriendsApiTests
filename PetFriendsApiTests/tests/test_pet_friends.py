from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Валенок', animal_type='коттерьер',
                                     age='2', pet_photo='CatImg.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Ледышка", "Волкособ", "2", "Volkosob.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Булка', animal_type='Котяра', age=3):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    assert len(my_pets['pets']) > 0, "Список питомцев пуст"
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_valid_data_without_photo (name='Котстик', animal_type='кот',
                                     age='3', pet_photo=''):
    """Проверяем что можно добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert result['pet_photo'] == pet_photo, "Фото отсутствует!"
    assert status == 200

def test_add_new_pet_without_name(name='', animal_type='кототерьер',
                                     age='2', pet_photo='CatImg.jpg'):
    """Проверяем что можно добавить питомца с корректными данными, но без имени"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200, "Нельзя добавить питомца без имени!"
    assert result['name'] == name

def test_update_photo_to_nonphoto_pet(pet_photo='scale.jpg'):
    """Проверяем, что можно добавить фото питомца в ранее созданного питомца без фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if pet_photo in my_pets['pets'][0]['id']:
        # Добавляем нового питомца без фото
        _, my_pets = pf.add_new_pet_without_pic(auth_key,'Ящерица', 'Новодобавленная', '1')
        # Запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берем последнего добавленного питомца и меняем его фото
    status, result = pf.add_new_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
    # Проверяем что статус ответа = 200 и есть фото питомца
    assert status == 200
    assert result['pet_photo'] != ''

def test_get_api_key_for_invalid_user(email=invalid_email, password=valid_password):
    """ Проверяем что при запросе api ключа с инвалидными данными почты невозможен"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200, "Пользователь не найден!"
    assert 'key' in result

def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    """ Проверяем что при запросе api ключа с инвалидными данными пароля невозможен"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200, "Пользователь не найден!"
    assert 'key' in result

def test_add_pet_with_invalid_huge_age(name='Кукушка', animal_type='крыша',
                                     age='120', pet_photo='images/cat1.jpg'):
    """Проверка на несуществующий возраст питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    assert int(age) < 32, "Значение возраста питомца слишком большое"
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_add_pet_with_invalid_negative_age(name='Кукушка', animal_type='крыша',
                                     age='-8', pet_photo='images/cat1.jpg'):
    """Проверка на невозможный возраст питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    assert int(age) < 0, "Недопустимое значение возраста питомца"
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_invalid_delete_self_pet():
    """Проверяем невозможность удаления питомца при неверном ID питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Ледышка", "Волкособ", "2", "Volkosob.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id несуществующего питомца и отправляем запрос на удаление
    pet_id = "d1413877f3691a3731380e733e877b0a"
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200, "Ошибка при попытке удалить питомца"
    assert pet_id not in my_pets.values()

def test_search_missing_pet(filter=''):
    """Проверяем возможность проверки несуществующего питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём несуществующего питомца
    pet_id = "dc6508a7-3190-4b83-a02e-45312cc16447"
    # Проверяем наличие в списке питомцев id питомца
    assert pet_id in my_pets.values()

def test_invalid_update_self_pet_info(name='Булка', animal_type='Котяра', age="летний01№"):
    """Проверяем возможность обновления информации о питомце на некорректную"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    assert len(my_pets['pets']) > 0, "Список питомцев пуст"
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200, "Недопустимые значения для добавления!"
    assert result['name'] == name
