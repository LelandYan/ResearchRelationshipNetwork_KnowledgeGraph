import logging
import os

from .backends import Backend


class Parser:
    def __init__(self, backend='grobid'):
        self.logger = logging.getLogger('pdf_parser')
        self._init_logger()

        self.backend = backend
        self.handler = self._load_handler(self.backend)
        self.handler = self.handler() if self.handler else None

    def _init_logger(self):
        self.logger.setLevel(logging.INFO)
        if not self.logger.hasHandlers():
            sh = logging.StreamHandler()
            sh.setLevel(logging.INFO)
            sh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(sh)

        backend_logger = logging.getLogger('pdf_parser.backend')
        backend_logger.setLevel(logging.INFO)

    def _load_handler(self, backend):
        for cls in Backend.__subclasses__():
            if cls.__name__.lower() == backend.lower():
                return cls
        self.logger.error(f'Backend {backend} not found')
        return None

    def _check_input_dir(self, input_path):
        if not os.path.exists(input_path):
            self.logger.error(f'Input path not found: {input_path}!')
            return False
        return True

    def _check_output_dir(self, output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except PermissionError:
            self.logger.error("Cannot make output dir. Check permission please.")
            return False
        except FileExistsError:
            self.logger.error(f"File exists with the same name of output dir: {output_dir}")
            return False

        if not os.access(output_dir, os.W_OK):
            self.logger.error("The output dir has no write permission.")
            return False
        return True

    def parse(self, typ, input_path, output_dir, num_threads=0, **kwargs):
        if self.handler is None:
            self.logger.error(f'Backend {self.backend} load failed, please try to re-construct parser.')
            return 0

        if not self._check_input_dir(input_path):
            return 0
        if not self._check_output_dir(output_dir):
            return 0

        self.logger.info(f'Start parsing {typ} of pdf files using {self.backend}.')
        num_parsed = self.handler.parse(typ, input_path, output_dir, num_threads, **kwargs)
        self.logger.info('Finish.')
        return num_parsed
