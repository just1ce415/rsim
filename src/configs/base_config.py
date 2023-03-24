
class BaseConfig:
    def __init__(self):
        self.team = []
        self.rotation = []

        # to optimize artifacts
        self.target_ers = None
        self.mv_params = None

    def _initialize_rotation(self):
        pass

    def _initialize_characters(self):
        pass

    def initialize_artifacts(self):
        pass

    def set_artifact_params(self, data):
        """
        :params:
        data - check format in src/protocol.json
        """
        self.er_info = data["er_info"]
        self.dmg_info = data["dmg_info"]