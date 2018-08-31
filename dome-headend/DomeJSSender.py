import requests
from urlparse import urljoin
import logging

log = logging.getLogger("domeviz-pusher")


class DomeJSSender(object):
    def __init__(self, sse_post_endpoint, channel="pub"):
        """Constructor

        :param sse_post_endpoint: Where should we POST data to? Omit the channel
        :param channel: Name of channel to send to.
        """
        self.sse_post_address = urljoin(sse_post_endpoint, channel)
        self.channel = channel

    def send_command(self, command):
        """Given a raw command, reformat it to match what DomeJS expects, send it

        :param command: Raw dome command packet
        """
        try:
            requests.post(
                self.sse_post_address,
                data=command.encode("base64")
            )

        except Exception as e:
            # Gotta catch 'em all
            log.warn("Push to domeviz failed: {}".format(e))
