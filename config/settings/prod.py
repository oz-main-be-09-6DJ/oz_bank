from .base import *

# DEBUG 설정 (배포 환경에서는 보통 False로 설정)
DEBUG = env.bool("DEBUG", default=False)