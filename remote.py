"""
Remote file for multi-shot KMeans
"""

import os
import sys
import json
import numpy as np
from utils import listRecursive
from .ica.ica import ica1
import scipy.io as sio
from .display import montage_data, fill_mask
# import nibabel as nib

#CONFIG_FILE = 'config.cfg'
DEFAULT_data_file = 'data.txt'
DEFAULT_num_components = 100


def gica_remote_init_env(args):
    """
        # Description:
            Initialize the remote environment, creating the config file.

        # PREVIOUS PHASE:
            None

        # INPUT:

            |   name            |   type    |   default     |
            |   ---             |   ---     |   ---         |
            |   num_components  |   int     |   20          |
            |   data_file       |   str     |   data.txt    |

        # OUTPUT:
            - config file written to disk

        # NEXT PHASE:
            remote_ica
    """

    computation_output = dict(output=dict(
        data_file=os.path.join(args["state"]["baseDirectory"], 'data.txt'),
        computation_phase="remote_init_env"), )
    return computation_output


def gica_remote_ica(args, prev_func_output):
    """
        # Description:
            Initialize the remote environment, creating the config file.

        # PREVIOUS PHASE:
            None

        # INPUT:

            |   name            |   type    |   default     |
            |   ---             |   ---     |   ---         |
            |   num_components  |   int     |   20          |
            |   data_file       |   str     |   data.txt    |

        # OUTPUT:
            - config file written to disk

        # NEXT PHASE:
            remote_ica
    """
    X = np.loadtxt(prev_func_output["output"]["data_file"])
    A, S, W = ica1(X, DEFAULT_num_components)
    outdir = args["state"]["outputDirectory"]
    indir = args["state"]["baseDirectory"]
    mask = sio.loadmat(os.path.join(indir, 'mask.mat'))['mask']
    Sr = fill_mask(S, mask)
    Sr = np.reshape(Sr.T, (53, 63, 46, 100), order="F")
    montage_data(Sr, outdir=outdir, indir=indir)
    np.savetxt(os.path.join(args["state"]["outputDirectory"], 'A.txt'), A)
    np.savetxt(os.path.join(args["state"]["outputDirectory"], 'S.txt'), S)
    np.savetxt(os.path.join(args["state"]["outputDirectory"], 'W.txt'), W)

    computation_output = dict(
        output=dict(computation_phase="gica_remote_1"),
        success=True,
    )

    return json.dumps(computation_output)


if __name__ == '__main__':

    parsed_args = json.loads(sys.stdin.read())
    phase_key = list(listRecursive(parsed_args, 'computation_phase'))

    if 'local_noop' in phase_key:  # FIRST PHASE
        computation_output = remote_init_env(parsed_args)
        computation_output = remote_ica(parsed_args, computation_output)
        sys.stdout.write(computation_output)
    else:
        raise ValueError('Oops')
