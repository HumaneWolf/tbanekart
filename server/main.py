from multiprocessing import Process

import api
import reisapi

if __name__ == '__main__':
    # Start API
    api = Process(target=api.run)
    api.start()

    reis = Process(target=reisapi.run)
    reis.start()

    api.join()
    reis.join()
