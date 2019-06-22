import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Permission:
    PERSONAL_INFO=0b0
    COURSE_INFO=0b1
    STUDENT_INFO=0b10
    SOURCE_INFO=0b100
    TEACHER_INFO=0b1000
    ADMIN_INFO=0b10000

class RolePermission:
    STUDENT = Permission.PERSONAL_INFO | Permission.COURSE_INFO
    TEACHER = Permission.PERSONAL_INFO | Permission.COURSE_INFO | Permission.STUDENT_INFO | Permission.SOURCE_INFO
    ADMIN = Permission.PERSONAL_INFO | Permission.COURSE_INFO | Permission.STUDENT_INFO | Permission.SOURCE_INFO | Permission.TEACHER_INFO
    ROOT = Permission.PERSONAL_INFO | Permission.COURSE_INFO | Permission.STUDENT_INFO | Permission.SOURCE_INFO | Permission.TEACHER_INFO | Permission.ADMIN_INFO



class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    POSTS_PER_PAGE = 10
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'StuInfoMange.sqlite')
    SQLALCHEMY_DATABASE_URI = "mysql://root:maizhiling456@127.0.0.1/StuInfoMange"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'



class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
