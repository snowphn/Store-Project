version = "1.0.0"
description = "邀请码管理插件"

from models.invite_code import InviteCode
from database.db_operations import create_invite_code, get_invite_codes, use_invite_code

def get_plugin_info():
    return {
        "name": "invite_code",
        "version": version,
        "description": description
    }

def install():
    """安装插件时的操作"""
    # 这里可以添加数据库迁移、初始化等操作
    pass

def uninstall():
    """卸载插件时的操作"""
    # 这里可以添加清理操作
    pass

# 插件API
def generate_code():
    return create_invite_code()

def list_codes():
    return get_invite_codes()

def verify_code(code):
    return use_invite_code(code) 