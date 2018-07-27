"""
Remote file for multi-shot KMeans
"""

import os
import sys
import json
import numpy as np
from ancillary import list_recursive
from ica.ica import ica1

#CONFIG_FILE = 'config.cfg'
DEFAULT_data_file = 'data.txt'
DEFAULT_num_components = 20


def remote_init_env(args):
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

    computation_output = dict(
        output=dict(
            data_file=os.path.join(args["state"]["baseDirectory"], 'data.txt'),
            computation_phase="remote_init_env"),)
    return computation_output


def remote_ica(args, prev_func_output):
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
    
    np.savetxt(os.path.join(args["state"]["outputDirectory"], 'A.txt'), A)
    np.savetxt(os.path.join(args["state"]["outputDirectory"], 'S.txt'), S)
    np.savetxt(os.path.join(args["state"]["outputDirectory"], 'W.txt'), W)

    computation_output = dict(
        output=dict(computation_phase="remote_ica"),
        success=True, )

    return json.dumps(computation_output)


if __name__ == '__main__':

    parsed_args = json.loads(sys.stdin.read())
    phase_key = list(list_recursive(parsed_args, 'computation_phase'))

    if 'local_noop' in phase_key:  # FIRST PHASE
        computation_output = remote_init_env(parsed_args)
        computation_output = remote_ica(parsed_args, computation_output)
        sys.stdout.write(computation_output)
    else:
        raise ValueError('Oops')
