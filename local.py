import json
import sys
from ancillary import list_recursive


def local_noop(**kwargs):
    """
        # Description:
            Nooperation

        # PREVIOUS PHASE:
            NA

        # INPUT:

        # OUTPUT:

        # NEXT PHASE:
            remote_init_env
    """
    computation_output = dict(
        output=dict(
            computation_phase="local_noop"
            ),
    )
    
    return json.dumps(computation_output)


if __name__ == '__main__':

    parsed_args = json.loads(sys.stdin.read())
    phase_key = list(list_recursive(parsed_args, 'computation_phase'))
    if not phase_key:  # FIRST PHASE
        computation_output = local_noop(**parsed_args['input'])
        sys.stdout.write(computation_output)
    else:
        raise ValueError('Phase error occurred at LOCAL')
