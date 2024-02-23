import requests
from bs4 import BeautifulSoup


def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching HTML content: {e}")
        return None


def extract_poem_urls(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    poem_urls = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith("/shiwenv_"):
            full_url = f"https://so.gushiwen.cn{href}"
            poem_urls.append(full_url)

    return poem_urls


def fetch_poem_details(url):
    poem_details = {
        "name": "",
        "author": "",
        "dynasty": "",
        "content": "",
        "trans": "",
        "annotation": "",
        "appreciation": "",
        "background": ""
    }
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        title_tag = soup.find('h1')
        if title_tag:
            poem_details["name"] = title_tag.text.strip().replace("\n", "")

        source_tag = soup.find('p', class_='source')
        if source_tag:
            source_info = source_tag.find_all('a')
            if len(source_info) > 0:
                poem_details["author"] = source_info[0].text.strip().replace("\n", "")
                poem_details["dynasty"] = source_info[1].text.strip().replace("\n", "").replace("〔", "").replace("〕",
                                                                                                                 "")

        content_tag = soup.find('div', class_='contson')
        if content_tag:
            poem_details["content"] = content_tag.get_text().strip().replace("\n", "")

        # 提取译文和注释
        trans_annotation_tag = soup.find('div', class_='contyishang')
        if trans_annotation_tag:
            p_tags = trans_annotation_tag.find_all('p')
            for p_tag in p_tags:
                if '译文' in p_tag.text:
                    poem_details["trans"] = p_tag.get_text().strip().replace("译文", "").replace("展开阅读全文 ∨", "")
                elif '注释' in p_tag.text:
                    poem_details["annotation"] = p_tag.get_text().strip().replace("注释", "").replace("展开阅读全文 ∨", "")

        appreciation_divs = soup.find_all('div', class_='contyishang')
        for div in appreciation_divs:
            if div.find('h2') and ('赏析' in div.find('h2').text or '鉴赏' in div.find('h2').text):
                appreciation_paragraphs = div.find_all('p')
                appreciation_text = "".join(p.get_text().strip() for p in appreciation_paragraphs).replace("\n", "").replace("展开阅读全文 ∨", "")
                poem_details["appreciation"] += "。"+appreciation_text

        # 提取创作背景
        background_divs = soup.find_all('div', class_='contyishang')
        for div in background_divs:
            if div.find('h2') and '创作背景' in div.find('h2').text:
                background_paragraphs = div.find_all('p')
                background_text = "".join(p.get_text().strip() for p in background_paragraphs).replace("\n", "").replace("展开阅读全文 ∨", "")
                poem_details["background"] = background_text

    return poem_details


if __name__ == "__main__":
    urls = [
        "https://so.gushiwen.cn/gushi/tangshi.aspx",
        "https://so.gushiwen.cn/gushi/sanbai.aspx",
        "https://so.gushiwen.cn/gushi/songsan.aspx"
    ]

    poem_urls = []
    for url in urls:
        html_content = fetch_html(url)
        if html_content:
            poem_urls.extend(extract_poem_urls(html_content))
        else:
            print("Failed to fetch or parse HTML content.")

    for url in poem_urls:
        details = fetch_poem_details(url)
        print(details)
