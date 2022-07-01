from setuptools import setup
import os
from glob import glob

package_name = 'my_tello'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='camille',
    maintainer_email='camille.cariat@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'create_tello = my_tello.create_tello:main',
            'test_param = my_tello.test_param:main',
            'tello_node = my_tello.tello_node:main'
        ],
    },
)
