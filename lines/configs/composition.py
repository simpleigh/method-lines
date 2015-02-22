from lines.configs import BaseConfig


class Config(BaseConfig):

    def load_data(self):

        composition = []
        with open(self.get_config_filename()) as file:
            for line in file:
                method_name = line.strip()

                if method_name not in self.job.configs.methods:
                    raise RuntimeError(
                        'Cannot find method "{}"'.format(method_name)
                    )

                composition.append(method_name)

        return composition
