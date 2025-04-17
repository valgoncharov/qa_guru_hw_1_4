import pytest
from http import HTTPStatus
from typing import Dict, Any
import math
from random import randint


def test_default_page_size(users_api) -> None:
    """
    Проверить, что размер страницы по возвращает ожидаемое
    количество элементов и соответствует общему количеству.
    """
    response = users_api.get_users()
    assert response.status_code == HTTPStatus.OK

    result: Dict[str, Any] = response.json()
    total: int = result["total"]
    items_count: int = len(result["items"])

    assert total == items_count, "Общее количество должно соответствовать количеству элементов"


@pytest.mark.parametrize('size', [1, 3, 5])
def test_custom_page_size(users_api, size: int) -> None:
    """
    Проверить пагинацию с разными размерами страниц.
        size: Количество элементов на странице
    """
    response = users_api.get_users(params={'page': 1, 'size': size})
    assert response.status_code == HTTPStatus.OK

    result: Dict[str, Any] = response.json()
    items: list = result['items']

    assert len(items) == size, f"На странице присутствует {size} элементов"
    assert result['size'] == size, "Размер страницы соответствует запрошенному размеру"
    assert result['page'] == 1, "Должен быть на первой странице"
    assert result['total'] > 0, "Общее количество элементов должно быть больше 0"


def test_random_page_size(users_api) -> None:
    """
    Проверить пагинацию с различным указанием страниц
    """
    size: int = randint(1, 13)
    response = users_api.get_users(params={"size": size})
    assert response.status_code == HTTPStatus.OK

    result: Dict[str, Any] = response.json()
    assert len(result["items"]
               ) == size, f"На странице присутствует {size} элементов"


@pytest.mark.parametrize('size', [1, 3, 5])
def test_total_pages_count(users_api, size: int) -> None:
    """
    Проверить правильное количество страниц при разных значениях size.
        size: Количество элементов на странице
    """
    # Получаем общее количество элементов
    response = users_api.get_users(params={'size': size})
    assert response.status_code == HTTPStatus.OK

    result: Dict[str, Any] = response.json()
    total_items: int = result['total']

    # Вычисляем ожидаемое количество страниц
    expected_pages: int = math.ceil(total_items / size)

    # Проверяем, что количество страниц соответствует ожидаемому
    assert result['pages'] == expected_pages, \
        f"Количество страниц должно быть {expected_pages} при размере страницы {size}"


@pytest.mark.parametrize('page', [1, 2, 3])
def test_page_navigation(users_api, page: int) -> None:
    """
    Проверить навигацию по разным страницам.
        page: Номер страницы
    """
    # Получаем данные для текущей страницы
    response = users_api.get_users(params={"page": page, "size": 5})
    assert response.status_code == HTTPStatus.OK

    result: Dict[str, Any] = response.json()

    # Проверяем номер страницы и наличие элементов
    assert result['page'] == page, f"Должна быть страница {page}"
    assert len(result['items']) > 0, "На странице должны быть элементы"

    # Проверяем, что total соответствует общему количеству элементов
    assert result['total'] > 0, "Общее количество элементов должно быть больше 0"

    # Проверяем, что количество страниц корректно
    expected_pages: int = math.ceil(result['total'] / result['size'])
    assert result['pages'] == expected_pages, \
        f"Количество страниц должно быть {expected_pages}"


def test_different_data_on_different_pages(users_api) -> None:
    """
    Проверить, что на разных страницах возвращаются разные данные.
    """
    # Получаем данные первой страницы
    response_page1 = users_api.get_users(params={"page": 1, "size": 5})
    assert response_page1.status_code == HTTPStatus.OK

    # Получаем данные второй страницы
    response_page2 = users_api.get_users(params={"page": 2, "size": 5})
    assert response_page2.status_code == HTTPStatus.OK

    page1_data: Dict[str, Any] = response_page1.json()
    page2_data: Dict[str, Any] = response_page2.json()

    # Получаем списки ID элементов с обеих страниц
    page1_ids = [item['id'] for item in page1_data['items']]
    page2_ids = [item['id'] for item in page2_data['items']]

    # Проверяем, что на страницах нет пересекающихся элементов
    common_ids = set(page1_ids) & set(page2_ids)
    assert len(
        common_ids) == 0, "На разных страницах не должно быть одинаковых элементов"
