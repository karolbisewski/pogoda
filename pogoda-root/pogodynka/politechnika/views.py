from django.http import JsonResponse
from time import time
from multiprocessing.pool import ThreadPool

try:
    from .reader import (
        odczyt_predkosci_wiatru,
        odczyt_kierunku_wiatru,
        odczyt_promieniowania,
    )
except ModuleNotFoundError:
    from .fake_reader import (
        odczyt_predkosci_wiatru,
        odczyt_kierunku_wiatru,
        odczyt_promieniowania,
    )

def readings_view(request):
    pool = ThreadPool(processes=3)
    async_wind_speed = pool.apply_async(odczyt_predkosci_wiatru, [1])
    async_wind_dir = pool.apply_async(odczyt_kierunku_wiatru, [1])
    async_flux = pool.apply_async(odczyt_promieniowania, [1])
    start = time()
    response = {
        'wind_speed': async_wind_speed.get(),
        'wind_dir': async_wind_dir.get(),
        'flux':async_flux.get(),
    }
    print("TOOK:", time() - start)
    return JsonResponse(response, safe=True)
