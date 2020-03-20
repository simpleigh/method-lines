from method_lines.configs.base import BaseConfig


class Composition(BaseConfig):

    def _process_data(self, file):
        composition = []

        for line in file:
            line = line.strip()

            # Skip blank lines
            if not line:
                continue

            # Check methods config SEPARATELY, BEFORE the calls config.
            # This means we don't need a calls config if our composition
            # only names methods (configs are loaded lazily as required).

            if line not in self.config_store.methods:
                if line not in self.config_store.calls:
                    raise RuntimeError(
                        'Cannot find method or call "{0}"'.format(line)
                    )

            composition.append(line)

        return composition
