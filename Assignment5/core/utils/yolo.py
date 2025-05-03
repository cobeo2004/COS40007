from typing import Optional


class YOLOYamlConfig:
    path: str  # Dataset root dir
    root_dir_path: str
    train_path: str  # Train images path (relative to 'path')
    val_path: str  # Val images path (relative to 'path')
    test_path: Optional[str] = None  # Test images path (optional)
    names: Optional[dict] = None  # Class names dictionary

    def __init__(
        self,
        path: str,
        root_dir_path: str,
        train_path: str,
        val_path: str,
        test_path: Optional[str] = None,
        names: Optional[dict] = None,
    ):
        self.path = path
        self.root_dir_path = root_dir_path
        self.train_path = train_path
        self.val_path = val_path
        self.names = names
        self.test_path = test_path


def create_yolo_yaml_config(config: YOLOYamlConfig) -> None:
    if config.path is None or not config.path.endswith(".yaml"):
        raise ValueError("path must end with .yaml")

    with open(config.path, "w") as f:
        # Write dataset paths
        f.write(f"path: {config.root_dir_path}  # dataset root dir\n")
        f.write(f"train: {config.train_path}  # train images\n")
        f.write(f"val: {config.val_path}  # val images\n")

        if config.test_path:
            f.write(f"test: {config.test_path}  # test images\n")
        else:
            f.write("test:  # test images (optional)\n")

        # Write class names
        f.write("\n# Classes\n")
        f.write("names:\n")
        if config.names:
            for class_id, class_name in config.names.items():
                f.write(f"  {class_id}: {class_name}\n")
