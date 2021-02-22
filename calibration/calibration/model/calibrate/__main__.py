import sys
from .calibrator import Calibrator

def main():
    id_ = sys.argv[1]
    calibrator = Calibrator(id_)
    calibrator.run()
    # print("__main__.py in calibrate")

if __name__ == "__main__":
    main()