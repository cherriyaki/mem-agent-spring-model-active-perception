from .run import SensRunner
import sys

def main():
    id_ = sys.argv[1]
    runner = SensRunner(id_)
    runner.run()

if __name__ == "__main__":
    main()