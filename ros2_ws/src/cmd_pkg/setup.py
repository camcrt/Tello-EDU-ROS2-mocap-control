from setuptools import setup

package_name = 'cmd_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
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
            'circle = cmd_pkg.do_circle:main',
            'print_Z = cmd_pkg.print_Z:main',
            'regul_Z = cmd_pkg.regul_Z:main',
            'regul_X = cmd_pkg.regul_X:main',
            'regul_Y = cmd_pkg.regul_Y:main',
            'regul_Z_PID = cmd_pkg.regul_Z_PID:main',
            'regul_X_PID = cmd_pkg.regul_X_PID:main',
            'regul_Y_PID = cmd_pkg.regul_Y_PID:main',
            'drone_suiveur = cmd_pkg.drone_suiveur:main',
            'create_topic = cmd_pkg.create_topic:main',
            'drone_suiveur_PID = cmd_pkg.drone_suiveur_PID:main',
            'regul_Z_fixe_PID = cmd_pkg.regul_Z_fixe_PID:main',
            'regul_Y_fixe_PID = cmd_pkg.regul_Y_fixe_PID:main',
            'regul_X_fixe_PID = cmd_pkg.regul_X_fixe_PID:main',
            'regul_pos = cmd_pkg.regul_pos:main',
            'ref_input = cmd_pkg.ref_input:main'

        ],
    },
)
