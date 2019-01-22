import logging

from .client import q_db

LOGGER = logging.getLogger(__name__)

WEB_SITES = 'WebSites'


def mark_url_as_fetched(index_id, url):
    web_sites = q_db.collection(WEB_SITES)
    db_cur = web_sites.find({'url': url})
    if db_cur.count() > 1:
        LOGGER.error(f'Found more than one instance of url in database: {url}')
        return False
    data = db_cur.batch()[0]
    if 'cc_index_ids_polled' not in data:
        LOGGER.debug(f'{url} dataset does not have any cc_index_ids_polled')
        data['cc_index_ids_polled'] = []
    LOGGER.info(f'Adding {index_id} to {url} as fetched')
    data['cc_index_ids_polled'].append(index_id)
    web_sites.update(data)


def get_all_websites():
    LOGGER.info('Getting all websites...')
    web_sites = q_db.collection(WEB_SITES)
    for web_site in web_sites.all():
        LOGGER.debug(f'Emitting {web_site}')
        yield web_site
