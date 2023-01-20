import codecs
import pickle
import urllib.parse
from .cmd import Cmd


class Payload:
    """
    Object for Payload Management
    """

    def __init__(self, payload, **kwargs) -> None:
        """
        Object for Payload Management
        """
        self.payload = payload
        self.data = kwargs

    def __str__(self):
        return Payload.trt_payload_out(self)

    @staticmethod
    def trt_payload_in(payload0):
        """
        processing of payloads received in a sequence of structured parameters

        @params: payload [String]
        @return: payload [String] , structured parameters Dict
        """

        payload = urllib.parse.unquote(payload0)

        res = {}
        while "{{" in payload:
            start = payload.index("{{")
            end = payload.index("}}")
            items = payload[start + 2 : end].split("===")
            # result string to object
            res[items[0]] = pickle.loads(codecs.decode(items[1].encode(), "base64"))
            payload = payload.replace(payload[start : end + 2], "").strip()
        return (
            payload0.copy(payload) if isinstance(payload0, Cmd) else payload,
            res,
        )

    @staticmethod
    def trt_payload_out(payload):
        """
        Processing of a Payload type as a character string

        @params: payload [ Payload | String ]
        @return: String
        """
        if isinstance(payload, Payload):
            tmp = ""
            for key_data, val_data in payload.data.items():
                # object to string
                val_data = codecs.encode(pickle.dumps(val_data), "base64").decode()
                tmp += f"{{{{{key_data}==={val_data}}}}} "

            final_pl = payload.payload + (" " + tmp if tmp else "")
            if len(final_pl) >= 2000:
                raise Exception("Payload data is too large")
            return urllib.parse.quote(final_pl)
        return urllib.parse.quote(payload)
