"""
Remote file for multi-shot KMeans
"""

import os
import sys
import json
import logging
import configparser
import numpy as np
from ancillary import list_recursive
from .ica.ica import ica1

CONFIG_FILE = 'config.cfg'
DEFAULT_data_file = 'data.txt'
DEFAULT_num_components = 20


def remote_init_env(data_file=DEFAULT_data_file,
                    num_components=DEFAULT_num_components,
                    config_file=CONFIG_FILE):
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

    logging.info('REMOTE: Initializing remote environment')
    if not os.path.exists(config_file):
        config = configparser.ConfigParser()
        config['REMOTE'] = dict(data_file=data_file)
        with open(config_path, 'w') as file:
            config.write(file)
    # output
    computation_output = dict(
        output=dict(
            config_file=config_file,
            data_file=os.path.join(args["state"]["baseDirectory"], data_file),
            computation_phase="remote_init_env"),
        success=True, )
    return json.dumps(computation_output)


def remote_ica(data_file=DEFAULT_data_file,
               num_components=DEFAULT_num_components):
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

    logging.info('REMOTE: Running ICA')
    X = np.loadtxt(data_file)
    A, S, W = ica1(X, num_components)
    computation_output = dict(
        output=dict(A=A, S=S, W=W, computation_phase="remote_ica"),
        success=True, )
    return json.dumps(computation_output)


if __name__ == '__main__':

    parsed_args = json.loads(sys.stdin.read())
    phase_key = list(list_recursive(parsed_args, 'computation_phase'))

    if 'local_noop' in phase_key:  # FIRST PHASE
        computation_output = remote_init_env(**parsed_args['input'])
        computation_output = remote_ica(**computation_output['output'])
        sys.stdout.write(computation_output)
    else:
        raise ValueError('Oops')
