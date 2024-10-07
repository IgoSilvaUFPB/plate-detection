from roboflow import Roboflow

def get_config(config: dict) -> tuple:
    rf= Roboflow(api_key=config["API_KEY"])
    project = rf.workspace(config["WORKSPACE"]).project(config["PROJECT"])
    version = project.version(int(config["VERSION"]))
    return project, version

def get_dataset(version):
    dataset = version.dataset()
    return dataset