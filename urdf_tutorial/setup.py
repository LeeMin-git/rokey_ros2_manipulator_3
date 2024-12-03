from setuptools import find_packages, setup
from setuptools import setup
from glob import glob
import os

package_name = 'urdf_tutorial'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share',package_name,'launch'),glob('launch/*.launch.py')),
        (os.path.join('share',package_name,'urdf'),glob('urdf/*.xacro'))
        #('shara/'+ package_name+'/launch',['launch/robot_1.launch.py']),
        #('share/'+package_name+'/urdf',['urdf/robot_1.xacro'])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='aaa',
    maintainer_email='leemin6487@gamil.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
