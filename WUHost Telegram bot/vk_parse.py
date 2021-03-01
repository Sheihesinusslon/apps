import vk
import config


class VkParser:
    ''' Class for parsing last post about the event from VK group. Uses VK api '''
    host = 'https://vk.com/wakeup_spb'
    token = config.VK_API
    session = vk.Session(access_token=token)
    vk_api = vk.API(session)


    def __init__(self):
        ''' When initializing the parser, it's empty. We cache last post id and data after
        first request from the user or bot '''
        self.last_post_id = ''
        self.data = None


    def last_post(self):
        ''' Function parses event's last post data and caches it '''
        request = self.vk_api.wall.search(domain='wakeup_spb', count=1, query="Разговорный клуб", v=5.58)
        post_id = request['items'][0]['id']

        # if cached post id is equal to parsed post id, then we return False to the bot, saying that
        # no updates from VK group
        if self.last_post_id == post_id:
            return False

        # if new post published, then cache its id and data and return True to the bot, saying that
        # there is an update from VK group
        self.last_post_id = post_id

        text = request['items'][0]['text']
        owner_id = request['items'][0]['owner_id']
        att = request['items'][0]['attachments'][0]
        if 'doc' in att.keys():
            url_att = att['doc']['url']
        elif 'photo' in att.keys():
            url_att = att['photo']['photo_1280']

        # serialize data in dict
        data = {
            'text': text,
            'post_id': post_id,
            'link': f'{self.host}?w=wall{owner_id}_{post_id}',
            'url_att': url_att
            }

        self.data = data
        return True

