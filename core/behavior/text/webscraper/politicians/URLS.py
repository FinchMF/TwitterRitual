"""
Contains urls and page parameters for Politician Crawler

author@matthewfinch
"""

class URLS:
    """object that contains links and page amount"""
    pages: int = 150
    root: str = 'https://millercenter.org'
    speeches_page: str = 'https://millercenter.org/the-presidency/presidential-speeches'
    page_url: str = '?field_speech_date_value%5Bmin%5D=&field_speech_date_value%5Bmax%5D=&field_full_node_value=&page='