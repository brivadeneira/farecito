""" Contains misc scrapers utilities """
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


def requests_retry_session(
    retries: int = 3,
    backoff: float = 0.3,  # TODO verify if it is the best value
    status_forcelist: tuple = (500, 502, 503, 504),
):
    session = Session()
    retries = Retry(
        total=retries,
        backoff_factor=backoff,
        status_forcelist=status_forcelist,
        allowed_methods={"GET", "POST"},
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session
