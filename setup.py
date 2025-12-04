from setuptools import setup, find_packages

setup(
    name="CS_Aimbot_Pro",
    version="2.0.0",
    author="Elite Developer",
    description="Advanced Counter-Strike Assistant Tool",
    packages=find_packages(),
    install_requires=[
        'opencv-python>=4.8.0',
        'numpy>=1.24.0',
        'pyautogui>=0.9.54',
        'pillow>=10.0.0',
        'pywin32>=306',
        'mss>=9.0.0',
        'keyboard>=0.13.5'
    ],
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
    ],
)
