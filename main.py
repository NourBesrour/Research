"""
main.py

Entrypoint script that runs the MBTI data cleaning pipeline.
"""

from src.data_cleaner import MBTICleaner

def main():
    """
    Main function that initializes MBTICleaner and runs the pipeline.
    """
    cleaner = MBTICleaner()
    cleaner.run()

if __name__ == "__main__":
    main()


