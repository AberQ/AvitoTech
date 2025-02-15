import requests

BASE_URL_REGISTER = "http://127.0.0.1:8080/api/auth"  
BASE_URL_PURCHASE = "http://127.0.0.1:8080/api/buy/cup" 
BASE_URL_TRANSFER = "http://127.0.0.1:8080/api/sendCoin"  

def test_register(username, password):
    """Регистрирует пользователя и возвращает access-токен"""
    data = {"username": username, "password": password}
    response = requests.post(BASE_URL_REGISTER, json=data)

    assert response.status_code == 200, f"Ошибка регистрации {username}: {response.json()}"
    json_response = response.json()

    assert "access" in json_response, f"Ответ не содержит access-токен для {username}"
    assert "refresh" in json_response, f"Ответ не содержит refresh-токен для {username}"

    print(f"✅ {username} успешно зарегистрирован!")
    return json_response["access"] 


def test_purchase(username, access_token):
    """Отправляет запрос на покупку мерча"""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(BASE_URL_PURCHASE, headers=headers)

    assert response.status_code == 200, f"Ошибка покупки для {username}: {response.json()}"
    json_response = response.json()

    assert json_response.get("description") == "Успешный ответ.", f"Ошибка API для {username}"
    
    print(f"✅ {username} успешно купил cup!")


def test_transfer(sender_name, sender_token, recipient_name, amount):
    """Переводит монеты от одного пользователя другому"""
    headers = {"Authorization": f"Bearer {sender_token}"}
    data = {"toUser": recipient_name, "amount": amount}

    response = requests.post(BASE_URL_TRANSFER, json=data, headers=headers)

    assert response.status_code == 200, f"Ошибка перевода от {sender_name} к {recipient_name}: {response.json()}"
    json_response = response.json()

    assert json_response.get("description") == "Успешный ответ!", f"Ошибка API при переводе от {sender_name} к {recipient_name}"

    print(f"✅ {sender_name} успешно перевел {amount} монеток пользователю {recipient_name}!")


if __name__ == "__main__":
    
    token_user1 = test_register("test_user", "test_password123")
    token_user2 = test_register("test_user2", "test_password123")

   
    test_purchase("test_user", token_user1)
    test_purchase("test_user2", token_user2)

 
    test_transfer("test_user", token_user1, "test_user2", 150)  
    test_transfer("test_user2", token_user2, "test_user", 150)  
