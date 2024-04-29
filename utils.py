from io import StringIO
from typing import List
import csv
import os

from dotenv import load_dotenv


def list_to_csv(lst: List[str], strip=True, **kw):
    with StringIO() as sio:
        csv_writer_kws = {}
        if 'quotechar' in kw: csv_writer_kws['quotechar'] = kw['quotechar']
        if 'delimiter' in kw: csv_writer_kws['delimiter'] = kw['delimiter']
        writer = csv.writer(sio, quoting=kw.get('quoting', csv.QUOTE_MINIMAL), **csv_writer_kws)
        writer.writerow(lst)
        ret = sio.getvalue()
    if strip:
        ret = ret.strip()
    return ret


def csv_to_list(s: str):
    if not s:
        return []
    with StringIO(s) as sio:
        reader = csv.reader(sio)
        return next(reader)


def getenv(k, default_val):
    load_dotenv()
    return os.getenv(k, default_val)

