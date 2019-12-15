import contextlib
import sys
from tqdm import tqdm
from tqdm.contrib import DummyTqdmFile


def create_bar(length, prefix, postfix):
    @contextlib.contextmanager
    def std_out_err_redirect_tqdm():
        orig_out_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = map(DummyTqdmFile, orig_out_err)
            yield orig_out_err[0]
        # Relay exceptions
        except Exception as exc:
            raise exc
        # Always restore sys.stdout/err if necessary
        finally:
            sys.stdout, sys.stderr = orig_out_err

    with std_out_err_redirect_tqdm() as orig_stdout:
        pbar = tqdm(total=length, file=orig_stdout, dynamic_ncols=True, desc=prefix, postfix=postfix)
    return pbar