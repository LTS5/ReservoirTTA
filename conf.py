# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""Configuration file (powered by YACS)."""

import argparse
import os
import sys
import logging
import random
import torch
import numpy as np
from datetime import datetime
from iopath.common.file_io import g_pathmgr
from yacs.config import CfgNode as CfgNode

# Global config object (example usage: from core.config import cfg)
_C = CfgNode()
cfg = _C

# ---------------------------------- Misc options --------------------------- #

_C.SAVE_CKPT = True
_C.RESUME_PATH = ""
# Setting - see README.md for more information
_C.SETTING = "continual"

# Data directory
_C.DATA_DIR = "./data"

# Weight directory
_C.CKPT_DIR = "./ckpt"
# Output directory

_C.SAVE_DIR = "./output"
# Log destination (in SAVE_DIR)
_C.LOG_DEST = "log.txt"

# Log datetime
_C.LOG_TIME = ''

# Enables printing intermediate results every x batches.
# Default -1 corresponds to no intermediate results
_C.PRINT_EVERY = 100

# Seed to use. If None, seed is not set!
# Note that non-determinism is still present due to non-deterministic GPU ops.
_C.RNG_SEED = 1

# Deterministic experiments.
_C.DETERMINISM = False

# Precision
_C.MIXED_PRECISION = False

# Optional description of a config
_C.DESC = ""

# # Config destination (in SAVE_DIR)
# _C.CFG_DEST = "cfg.yaml"


# ----------------------------- Model options ------------------------------- #
_C.MODEL = CfgNode()

# Some of the available models can be found here:
# Torchvision: https://pytorch.org/vision/0.14/models.html
# timm: https://github.com/huggingface/pytorch-image-models/tree/v0.6.13
# RobustBench: https://github.com/RobustBench/robustbench
# OpenCLIP: https://github.com/mlfoundations/open_clip
_C.MODEL.ARCH = 'Standard'

# Type of pre-trained weights
# For torchvision models see: https://pytorch.org/vision/0.14/models.html
# For OpenClip models, use either 'openai' (for the original OpenAI weights) or see https://github.com/mlfoundations/open_clip/blob/main/docs/openclip_results.csv
_C.MODEL.WEIGHTS = "IMAGENET1K_V1"

# Whether to use a CLIP based architecture
_C.MODEL.USE_CLIP = False

# Path to a specific checkpoint
_C.MODEL.CKPT_PATH = ""

# Inspect the cfgs directory to see all possibilities
_C.MODEL.ADAPTATION = 'source'

# Reset the model before every new batch
_C.MODEL.EPISODIC = False

# Reset the model after a certain amount of update steps (e.g., used in RDumb)
_C.MODEL.RESET_AFTER_NUM_UPDATES = 0

# ----------------------------- Corruption options -------------------------- #
_C.CORRUPTION = CfgNode()

# Dataset for evaluation
_C.CORRUPTION.DATASET = 'cifar10_c'

# Check https://github.com/hendrycks/robustness for corruption details
_C.CORRUPTION.TYPE = ['gaussian_noise', 'shot_noise', 'impulse_noise',
                      'defocus_blur', 'glass_blur', 'motion_blur', 'zoom_blur',
                      'snow', 'frost', 'fog', 'brightness', 'contrast',
                      'elastic_transform', 'pixelate', 'jpeg_compression']
_C.CORRUPTION.SEVERITY = [5, 4, 3, 2, 1]

# Number of examples to evaluate. If num_ex != -1, each sequence is sub-sampled to the specified amount
# For ImageNet-C, RobustBench loads a list containing 5000 samples.
_C.CORRUPTION.NUM_EX = -1

_C.CORRUPTION.RECUR = 20

# ------------------------------- Batch norm options ------------------------ #
_C.BN = CfgNode()

# BN alpha (1-alpha) * src_stats + alpha * test_stats
_C.BN.ALPHA = 0.1

# ------------------------------- Optimizer options ------------------------- #
_C.OPTIM = CfgNode()

# Number of updates per batch
_C.OPTIM.STEPS = 1

# Learning rate
_C.OPTIM.LR = 1e-3

# Optimizer choices: Adam, AdamW, SGD
_C.OPTIM.METHOD = 'Adam'

# Beta1 for Adam based optimizers
_C.OPTIM.BETA = 0.9

# Momentum
_C.OPTIM.MOMENTUM = 0.9

# Momentum dampening
_C.OPTIM.DAMPENING = 0.0

# Nesterov momentum
_C.OPTIM.NESTEROV = True

# L2 regularization
_C.OPTIM.WD = 0.0

# --------------------------------- EATA options ---------------------------- #
_C.EATA = CfgNode()

# Fisher alpha. If set to 0.0, EATA becomes ETA and no EWC regularization is used
_C.EATA.FISHER_ALPHA = 2000.0

# Diversity margin
_C.EATA.D_MARGIN = 0.05
_C.EATA.MARGIN_E0 = 0.4             # Will be multiplied by: EATA.MARGIN_E0 * math.log(num_classes)
_C.EATA.MOMENTUM_SRC = 1.0

# --------------------------------- SAR options ---------------------------- #
_C.SAR = CfgNode()

# Threshold e_m for model recovery scheme
_C.SAR.RESET_CONSTANT_EM = 0.2

# --------------------------------- ROID options --------------------------- #
_C.ROID = CfgNode()

_C.ROID.USE_WEIGHTING = True        # Whether to use loss weighting
_C.ROID.USE_PRIOR_CORRECTION = True # Whether to use prior correction
_C.ROID.USE_CONSISTENCY = True      # Whether to use consistency loss
_C.ROID.MOMENTUM_SRC = 0.99         # Momentum for weight ensembling (param * model + (1-param) * model_src)
_C.ROID.MOMENTUM_PROBS = 0.9        # Momentum for diversity weighting
_C.ROID.TEMPERATURE = 1/3           # Temperature for weights

# --------------------------------- DPcore options --------------------------- #
_C.DPCORE = CfgNode()

# loss = lamda * std_loss + mean_loss

_C.DPCORE.EMA_ALPHA = 0.999
_C.DPCORE.E_ID = 1
_C.DPCORE.E_OOD = 50
_C.DPCORE.LAMDA = 1.0
_C.DPCORE.MAX_PROTOTYPES = 2000
_C.DPCORE.NUM_PROMPTS = 8
_C.DPCORE.SRC_NUM_SAMPLES = 300
_C.DPCORE.TEMP_TAU = 3.0
_C.DPCORE.THR_RHO = 0.8

# ------------------------------- Source options -------------------------- #
_C.SOURCE = CfgNode()

# Number of workers for source data loading
_C.SOURCE.NUM_WORKERS = 8

# Percentage of source samples used
_C.SOURCE.PERCENTAGE = 1.0   # (0, 1] Possibility to reduce the number of source samples

# Possibility to define the number of source samples. The default setting corresponds to all source samples
_C.SOURCE.NUM_SAMPLES = -1

# ------------------------------- ReservoirTTA options -------------------------- #
_C.RESERVOIRTTA = CfgNode()
_C.RESERVOIRTTA.MAX_NUM_MODELS = 16
_C.RESERVOIRTTA.SIZE_OF_BUFFER = 64
_C.RESERVOIRTTA.QUANTILE_THR = 0.999

# ablation study
_C.RESERVOIRTTA.ENSEMBLING = True
_C.RESERVOIRTTA.SAMPLING = 'reservoir' # {0: "fifo", 1: "replace", 2:"reservoir"}
_C.RESERVOIRTTA.INIT = 'mi' #{0: "mi", 2: "source"}
_C.RESERVOIRTTA.PROGRESSIVE_UPDATE = False
_C.RESERVOIRTTA.SOURCE_BUFFER = False

_C.RESERVOIRTTA.STYLE_IDX = [2, 5, 7]
_C.RESERVOIRTTA.STYLE_FORMAT = "LOGVAR"

# ------------------------------- Testing options ------------------------- #
_C.TEST = CfgNode()

# Number of workers for test data loading
_C.TEST.NUM_WORKERS = 4

# Batch size for evaluation (and updates)
_C.TEST.BATCH_SIZE = 64

# If the batch size is 1, a sliding window approach can be applied by setting window length > 1
_C.TEST.WINDOW_LENGTH = 1

# Number of augmentations for methods relying on TTA (test time augmentation)
_C.TEST.N_AUGMENTATIONS = 32

# The value of the Dirichlet distribution used for sorting the class labels.
_C.TEST.DELTA_DIRICHLET = 0.0

# Debuging mode
_C.TEST.DEBUG = False

# --------------------------------- CUDNN options --------------------------- #
_C.CUDNN = CfgNode()

# Benchmark to select fastest CUDNN algorithms (best for fixed input sizes)
_C.CUDNN.BENCHMARK = True

# --------------------------------- Default config -------------------------- #
_CFG_DEFAULT = _C.clone()
_CFG_DEFAULT.freeze()


def assert_and_infer_cfg():
    """Checks config values invariants."""
    err_str = "Unknown adaptation method."
    assert _C.MODEL.ADAPTATION in ["source", "norm", "tent"]
    err_str = "Log destination '{}' not supported"
    assert _C.LOG_DEST in ["stdout", "file"], err_str.format(_C.LOG_DEST)


def merge_from_file(cfg_file):
    with g_pathmgr.open(cfg_file, "r") as f:
        cfg = _C.load_cfg(f)
    _C.merge_from_other_cfg(cfg)


def dump_cfg():
    """Dumps the config to the output directory."""
    cfg_file = os.path.join(_C.SAVE_DIR, _C.CFG_DEST)
    with g_pathmgr.open(cfg_file, "w") as f:
        _C.dump(stream=f)


def load_cfg(out_dir, cfg_dest="config.yaml"):
    """Loads config from specified output directory."""
    cfg_file = os.path.join(out_dir, cfg_dest)
    merge_from_file(cfg_file)


def reset_cfg():
    """Reset config to initial state."""
    cfg.merge_from_other_cfg(_CFG_DEFAULT)


def load_cfg_from_args(description="Config options."):
    """Load config from command line args and set any specified options."""
    current_time = datetime.now().strftime("%y%m%d_%H%M%S")
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--cfg", dest="cfg_file", type=str, required=True,
                        help="Config file location")
    parser.add_argument("opts", default=None, nargs=argparse.REMAINDER,
                        help="See conf.py for all options")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    merge_from_file(args.cfg_file)
    cfg.merge_from_list(args.opts)

    log_dest = os.path.basename(args.cfg_file)
    real_method_name = log_dest.split('.yaml')[0]
    log_dest = log_dest.replace('.yaml', '_{}.txt'.format(current_time))
   
    cfg.METHOD_DIR = os.path.join(cfg.SAVE_DIR, cfg.CORRUPTION.DATASET, cfg.MODEL.ARCH, real_method_name)
    cfg.SAVE_DIR = os.path.join(cfg.METHOD_DIR, f"{cfg.SETTING}_delta={cfg.TEST.DELTA_DIRICHLET}_bs={cfg.TEST.BATCH_SIZE}", f"seed={cfg.RNG_SEED}")
    
    g_pathmgr.mkdirs(cfg.SAVE_DIR)
    cfg.LOG_TIME, cfg.LOG_DEST = current_time, log_dest
    cfg.freeze()

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(filename)s: %(lineno)4d]: %(message)s",
        datefmt="%y/%m/%d %H:%M:%S",
        handlers=[
            logging.FileHandler(os.path.join(cfg.SAVE_DIR, cfg.LOG_DEST)),
            logging.StreamHandler()
        ])

    if cfg.RNG_SEED:
        torch.manual_seed(cfg.RNG_SEED)
        torch.cuda.manual_seed(cfg.RNG_SEED)
        np.random.seed(cfg.RNG_SEED)
        random.seed(cfg.RNG_SEED)
        torch.backends.cudnn.benchmark = cfg.CUDNN.BENCHMARK

        if cfg.DETERMINISM:
            # enforce determinism
            if hasattr(torch, "set_deterministic"):
                torch.set_deterministic(True)
            torch.backends.cudnn.benchmark = False
            torch.backends.cudnn.deterministic = True

    logger = logging.getLogger(__name__)
    version = [torch.__version__, torch.version.cuda,
               torch.backends.cudnn.version()]
    logger.info("PyTorch Version: torch={}, cuda={}, cudnn={}".format(*version))
    logger.info(cfg)


def complete_data_dir_path(data_root_dir: str, dataset_name: str):
    # map dataset name to data directory name
    mapping = {"imagenet": os.path.join("imagenet", "images"),
               "imagenet_c": "ImageNet-C",
               "imagenet_r": "imagenet-r",
               "imagenet_a": "imagenet-a",
               "imagenet_k": os.path.join("ImageNet-Sketch", "sketch"),
               "imagenet_v2": os.path.join("imagenet-v2", "imagenetv2-matched-frequency-format-val"),
               "imagenet_d": "imagenet-d",      # do not change
               "imagenet_d109": "imagenet-d",   # do not change
               "domainnet126": "DomainNet-126", # directory containing the 6 splits of "cleaned versions" from http://ai.bu.edu/M3SDA/#dataset
               "cifar10": "",       # do not change
               "cifar10_c": "",     # do not change
               "cifar100": "",      # do not change
               "cifar100_c": "",    # do not change
               "caltech101": os.path.join("caltech101", "101_ObjectCategories"),
               "dtd": os.path.join("dtd", "dtd", "images"),
               "eurosat": os.path.join("eurosat", "2750"),                      # automatic download fails
               "fgvc_aircraft": os.path.join("fgvc-aircraft-2013b", "data"),    # do not add 'images' in path
               "flowers102": os.path.join("flowers-102", "jpg"),
               "food101": os.path.join("food-101", "images"),
               "oxford_pets": os.path.join("oxford-iiit-pet", "images"),
               "stanford_cars": os.path.join("stanford_cars"),                  # automatic download fails
               "sun397": os.path.join("sun397"),                                # automatic download fails
               "ucf101": os.path.join("ucf101", "UCF-101-midframes"),           # automatic download fails
               "ccc": "",
               }
    assert dataset_name in mapping.keys(),\
        f"Dataset '{dataset_name}' is not supported! Choose from: {list(mapping.keys())}"
    return os.path.join(data_root_dir, mapping[dataset_name])


generalization_dataset_names = [
    "flowers102", "dtd", "oxford_pets", "stanford_cars", "ucf101",
    "caltech101", "food101", "sun397", "fgvc_aircraft", "eurosat"
]


def ds_name2pytorch_ds_name(ds_name: str):
    # converts the dataset name into the pytorch name convention (see: https://pytorch.org/vision/stable/datasets.html)
    lookup_table = {
        "flowers102": "Flowers102",
        "dtd": "DTD",
        "oxford_pets": "OxfordIIITPet",
        "stanford_cars": "StanfordCars",
        "ucf101": "UCF101",
        "caltech101": "Caltech101",
        "food101": "Food101",
        "sun397": "SUN397",
        "fgvc_aircraft": "FGVCAircraft",
        "eurosat": "EuroSAT",
    }
    assert ds_name in lookup_table.keys(), \
        f"There is no mapping for dataset name '{ds_name}'! Supported dataset names are: {list(lookup_table.keys())}"
    return lookup_table[ds_name]


def get_num_classes(dataset_name: str):
    dataset_name2num_classes = {"cifar10": 10, "cifar10_c": 10, "cifar100": 100,  "cifar100_c": 100,
                                "imagenet": 1000, "imagenet_v2": 1000, "imagenet_c": 1000, "ccc": 1000,
                                "imagenet_k": 1000, "imagenet_r": 200, "imagenet_a": 200,
                                "imagenet_d": 164, "imagenet_d109": 109, "imagenet200": 200,
                                "domainnet126": 126,
                                "eurosat": 10, "flowers102": 102, "oxford_pets": 37,
                                "dtd": 47, "food101": 101, "sun397": 397, "caltech101": 100,
                                "ucf101": 101, "stanford_cars": 196, "fgvc_aircraft": 100
                                }
    assert dataset_name in dataset_name2num_classes.keys(), \
        f"Dataset '{dataset_name}' is not supported! Choose from: {list(dataset_name2num_classes.keys())}"
    return dataset_name2num_classes[dataset_name]


def ckpt_path_to_domain_seq(ckpt_path: str):
    assert ckpt_path.endswith('.pth') or ckpt_path.endswith('.pt')
    domain = ckpt_path.replace('.pth', '').split(os.sep)[-1].split('_')[1]
    mapping = {"real": ["clipart", "painting", "sketch"],
               "clipart": ["sketch", "real", "painting"],
               "painting": ["real", "sketch", "clipart"],
               "sketch": ["painting", "clipart", "real"],
               }
    return mapping[domain]
