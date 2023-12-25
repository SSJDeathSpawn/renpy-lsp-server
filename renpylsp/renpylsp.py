import json
import sys
from pylsp_jsonrpc.dispatchers import MethodDispatcher
from pylsp_jsonrpc.endpoint import Endpoint
from pylsp_jsonrpc.streams import JsonRpcStreamReader, JsonRpcStreamWriter
from loguru import logger


class RenpyLanguageServer(MethodDispatcher):
    """Implementation of JSON RPC method dispatcher for Renpy"""

    def __init__(self):
        self.readfile = JsonRpcStreamReader(sys.stdin.buffer)
        self.writefile = JsonRpcStreamWriter(sys.stdout.buffer)
        self.endpoint = Endpoint(self, self.writefile.write)

    def start(self):
        logger.info("Listening to endpoint")
        self.readfile.listen(self.endpoint.consume)

    def m_exit(self):
        self.endpoint.shutdown()
        self.readfile.close()
        self.writefile.close()

    def m_initialize(self, rootUri=None, **kwargs):
        logger.info("Got initialize params: {}".format(kwargs))
        return {"capabilities": {
            "textDocumentSync": {
                "openClose": True,
            }
        }}

    def m_text_document__did_open(self, textDocument=None, **_kwargs):
        logger.info("Opened text document {}".format(textDocument))
        self.endpoint.notify('textDocument/publishDiagnostics', {
            'uri': textDocument['uri'],
            'diagnostics': [{
                'range': {
                    'start': {'line': 0, 'character': 0},
                    'end': {'line': 1, 'character': 0},
                },
                'message': 'Some very bad Python code',
                'severity': 1  # DiagnosticSeverity.Error
            }]
        })

    def __getitem__(self, item):
        logger.info("Asking for {}".format(item))
        return super().__getitem__(item)
