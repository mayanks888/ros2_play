from setuptools import setup

package_name = 'py_pubsub'

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
    maintainer='mayank_s',
    maintainer_email='mayank.sati@gwmidc.in',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'talker = py_pubsub.publisher_member_function:main',
                'myrun = py_pubsub.checkmsg:main',
                'play_run = py_pubsub.play_ros:main',
                'play_may= py_pubsub.mayank_process:main',
                'temp_datasets=py_pubsub.template_data_create:main',
                'read_image=py_pubsub.reading_and_display_ros_images:main',
                'read_img_loc=py_pubsub.reading_image_location_ros2:main',
        ],
},
)
