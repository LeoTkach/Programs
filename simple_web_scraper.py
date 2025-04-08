#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import requests
from bs4 import BeautifulSoup

DEFAULT_USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

def fetch_page(url, user_agent=DEFAULT_USER_AGENT):
    try:
        headers = {'User-Agent': user_agent}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке URL {url}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при запросе: {e}", file=sys.stderr)
        return None

def parse_data(html_content, selector, extract_attribute=None):
    extracted_data = []
    try:
        soup = BeautifulSoup(html_content, 'lxml')
        elements = soup.select(selector)

        if not elements:
            print(f"Элементы по селектору '{selector}' не найдены.", file=sys.stderr)
            return []

        for element in elements:
            if extract_attribute:
                value = element.get(extract_attribute)
                if value:
                    extracted_data.append(value.strip())
            else:
                extracted_data.append(element.get_text(strip=True))

    except ImportError:
         print("Ошибка: Парсер 'lxml' не найден. Установите его: pip install lxml", file=sys.stderr)
         return []
    except Exception as e:
        print(f"Ошибка при парсинге HTML: {e}", file=sys.stderr)
        return []

    return extracted_data

def main():
    parser = argparse.ArgumentParser(description="Простой веб-скрейпер на Python.")

    parser.add_argument("url", help="URL веб-страницы для скрейпинга.")
    parser.add_argument("selector", help="CSS-селектор для поиска элементов (например, 'h2.title').")
    parser.add_argument("-a", "--attribute",
                        help="Извлечь значение указанного атрибута вместо текста (например, 'href', 'src').")
    parser.add_argument("-ua", "--user-agent", default=DEFAULT_USER_AGENT,
                        help="Установить свой User-Agent для запроса.")

    args = parser.parse_args()

    print(f"[*] Загрузка страницы: {args.url}")
    html = fetch_page(args.url, args.user_agent)

    if html:
        print(f"[*] Поиск элементов по селектору: '{args.selector}'")
        if args.attribute:
            print(f"[*] Извлечение атрибута: '{args.attribute}'")
        else:
            print(f"[*] Извлечение текста")

        data = parse_data(html, args.selector, args.attribute)

        if data:
            print("\n[+] Найденные данные:")
            for item in data:
                print(f"- {item}")
            print(f"\n[*] Найдено {len(data)} элементов.")
        else:
            print("\n[-] Данные не найдены или произошла ошибка при парсинге.")
            sys.exit(1)
    else:
        print("[-] Не удалось загрузить страницу.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
