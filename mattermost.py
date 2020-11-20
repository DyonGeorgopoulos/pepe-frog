import json
import logging
import ssl
import requests
import socket
import websocket
import settings
# import websocket._exceptions

logger = logging.getLogger(__name__)

class MattermostAPI(object):
    def __init__(self, url, ssl_verify, token):
        print(token)
        self.url = url
        self.token = token
        self.initial = None
        self.default_team_id = None
        self.teams_channels_ids = None
        self.ssl_verify = ssl_verify
        if not ssl_verify:
            requests.packages.urllib3.disable_warnings(
            requests.packages.urllib3.exceptions.InsecureRequestWarning)
    
    def _get_headers(self):
        return {"Authorization": "Bearer " + self.token}
    
    def channel(self, channel_id):
        channel = {'channel': self.get('/channels/{}'.format(channel_id))}
        return channel

    def get(self, request):
        return json.loads(
            requests.get(
                self.url + request,
                headers=self._get_headers(),
                verify=self.ssl_verify
            ).text)
    
    def get_channel_by_name(self, channel_name, team_id=None):
        return self.get('/teams/{}/channels/name/{}'.format(
            team_id, channel_name))

    def get_channels(self, team_id=None):
        if team_id is None:
            team_id = self.default_team_id
        return self.get('/users/me/teams/{}/channels'.format(team_id))

    def post(self, request, data):
        return json.loads(requests.post(
            self.url + request,
            headers=self._get_headers(),
            data=json.dumps(data),
            verify=self.ssl_verify
        ).text)
    def search_team(self,team_id, special_terms):
        print(team_id)
        req = "/teams/" + settings.TEAM_ID + "/posts/search"
        return self.post(
            req,
            {
                "terms":"!remindme" + special_terms,
                "include_deleted_channels":True,
                "is_or_search": True,
                "time_zone_offset":37800,
                "page":0,
                "per_page":20
            })
    def create_direct(self, userData):
        req = "/channels/direct"
        users = [settings.BOT_ID, "{}".format(userData["user_id"])]
        print("printing users to create new channel")
        print(users)
        return self.post(req,users) 
    def create_post(self, channel_id, userData):
        print(channel_id)
        created_channel = self.create_direct(userData)
        print(created_channel)
        message = "@{} this is a reminder for [This!]({}/{}/pl/{})".format(userData["user_name"],settings.BASE_URL, settings.TEAM_NAME,userData["post_id"]) 
        req = "/posts"
        return self.post(req,
                {
                    "channel_id": created_channel["id"],
                    "message": message
                })
